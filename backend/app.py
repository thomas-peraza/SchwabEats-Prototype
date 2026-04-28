from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from zoneinfo import ZoneInfo

from recommendation.eligibility import EligibilityChecker
from recommendation.filters import HardFilterEngine
from recommendation.models import Employee, MenuItem, Order, RecommendationResponse, Vendor
from recommendation.recommender import RecommendationRequest, VendorRecommender

load_dotenv()

app = Flask(__name__)

eligibility_checker = EligibilityChecker()
hard_filter_engine = HardFilterEngine()
recommender = VendorRecommender(
    eligibility_checker=eligibility_checker,
    hard_filter_engine=hard_filter_engine,
)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

ORDER_SUBSIDY_PERCENT = 0.8
EMPLOYEE_COPAY = 5.0


def _parse_menu_item(data: dict) -> MenuItem:
    """Convert incoming menu item JSON into a MenuItem model."""
    return MenuItem(
        id=str(data["id"]),
        vendor_id=str(data["vendor_id"]),
        name=str(data["name"]),
        allergen_codes=[str(code) for code in data.get("allergen_codes", [])],
        restriction_codes=[str(code) for code in data.get("restriction_codes", [])],
        cuisine_type=data.get("cuisine_type"),
        is_available=bool(data.get("is_available", True)),
    )


def _parse_order(data: dict) -> Order:
    """Convert incoming order JSON into an Order model."""
    return Order(
        id=str(data.get("id", uuid4())),
        employee_id=str(data["employee_id"]),
        vendor_id=str(data["vendor_id"]),
        items=[_parse_menu_item(item) for item in data.get("items", [])],
        timestamp=datetime.fromisoformat(data["timestamp"]),
        campus_id=str(data["campus_id"]),
    )


def _parse_employee(data: dict) -> Employee:
    """Convert incoming employee JSON into an Employee model."""
    return Employee(
        id=str(data["id"]),
        campus_id=str(data["campus_id"]),
        role=str(data["role"]),
        is_on_leave=bool(data.get("is_on_leave", False)),
        is_terminated=bool(data.get("is_terminated", False)),
        is_eligible=bool(data.get("is_eligible", False)),
        orders_today=int(data.get("orders_today", 0)),
        dietary_flags=[str(flag) for flag in data.get("dietary_flags", [])],
        order_history=[_parse_order(order) for order in data.get("order_history", [])],
        timezone=str(data.get("timezone", "America/Chicago")),
    )


def _parse_vendor(data: dict) -> Vendor:
    """Convert incoming vendor JSON into a Vendor model."""
    return Vendor(
        id=str(data["id"]),
        name=str(data["name"]),
        contract_status=str(data["contract_status"]),
        accepting_orders=bool(data.get("accepting_orders", False)),
        delivery_zones=[str(zone) for zone in data.get("delivery_zones", [])],
        menu_items=[_parse_menu_item(item) for item in data.get("menu_items", [])],
        performance_score=float(data.get("performance_score", 0.0)),
        average_rating=(
            float(data["average_rating"]) if data.get("average_rating") is not None else None
        ),
        metadata=dict(data.get("metadata", {})),
    )


def _serialize_recommendation_response(payload: RecommendationResponse) -> dict:
    """Serialize recommendation output for JSON responses."""
    return {
        "employee_id": payload.employee_id,
        "recommendations": [
            {
                "vendor_id": rec.vendor_id,
                "vendor_name": rec.vendor_name,
                "score": rec.score,
                "rank": rec.rank,
                "reason_codes": rec.reason_codes,
            }
            for rec in payload.recommendations
        ],
        "low_availability": payload.low_availability,
        "generated_at": payload.generated_at.isoformat(),
        "generated_for_date": payload.generated_for_date.isoformat(),
    }


def _resolve_request_time(employee_timezone: str, request_time_iso: str | None) -> datetime:
    """Build request-local datetime from payload or current local campus time."""
    tz = ZoneInfo(employee_timezone)
    if request_time_iso:
        parsed = datetime.fromisoformat(request_time_iso)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=tz)
        return parsed.astimezone(tz)
    return datetime.now(tz)


def _validate_order_inputs(
    employee: Employee,
    vendor: Vendor,
    selected_item_ids: list[str],
    request_time_local: datetime,
) -> tuple[bool, list[str], Vendor | None]:
    """Run ordering gate checks and return filtered vendor for compliant item validation."""
    reasons: list[str] = []

    eligibility = eligibility_checker.check_employee_eligibility(employee, request_time_local)
    if not eligibility.is_eligible:
        reasons.extend(eligibility.reasons)
        return False, reasons, None

    filtered_vendors = hard_filter_engine.apply_prefilters(employee, [vendor])
    if not filtered_vendors:
        reasons.append("vendor_not_eligible_for_employee")
        return False, reasons, None

    filtered_vendor = filtered_vendors[0]
    compliant_ids = {item.id for item in filtered_vendor.menu_items if item.is_available}
    if not selected_item_ids:
        reasons.append("no_menu_items_selected")
    elif not set(selected_item_ids).issubset(compliant_ids):
        reasons.append("selected_items_not_compliant")

    return len(reasons) == 0, reasons, filtered_vendor

@app.route("/")
def home():
    return "SchwabEats Backend Running"


@app.post("/api/recommendations")
def get_recommendations():
    """Return ranked vendor recommendations for an employee request context."""
    body = request.get_json(silent=True) or {}

    try:
        employee = _parse_employee(body["employee"])
        vendors = [_parse_vendor(v) for v in body.get("vendors", [])]
        request_time_local = _resolve_request_time(
            employee_timezone=employee.timezone,
            request_time_iso=body.get("request_time_local"),
        )
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"error": "invalid_request", "details": str(exc)}), 400

    recommendation_request = RecommendationRequest(
        employee=employee,
        vendors=vendors,
        request_time_local=request_time_local,
        top_n=int(body.get("top_n", 5)),
        campus_popularity=body.get("campus_popularity"),
    )
    response = recommender.recommend(recommendation_request)
    return jsonify(_serialize_recommendation_response(response)), 200


@app.post("/api/orders/quote")
def quote_order():
    """Validate whether an order can be placed and return a subsidy/cost quote."""
    body = request.get_json(silent=True) or {}

    try:
        employee = _parse_employee(body["employee"])
        vendor = _parse_vendor(body["vendor"])
        selected_item_ids = [str(item_id) for item_id in body.get("selected_item_ids", [])]
        request_time_local = _resolve_request_time(
            employee_timezone=employee.timezone,
            request_time_iso=body.get("request_time_local"),
        )
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"error": "invalid_request", "details": str(exc)}), 400

    is_valid, reasons, filtered_vendor = _validate_order_inputs(
        employee=employee,
        vendor=vendor,
        selected_item_ids=selected_item_ids,
        request_time_local=request_time_local,
    )
    if not is_valid:
        return jsonify({"allowed": False, "reasons": reasons}), 422

    order_total = float(body.get("order_total", 0.0))
    employee_pay = min(order_total, EMPLOYEE_COPAY)
    company_subsidy = max(order_total - employee_pay, 0.0)

    return (
        jsonify(
            {
                "allowed": True,
                "vendor_id": filtered_vendor.id,
                "selected_item_ids": selected_item_ids,
                "subsidy_policy": {
                    "company_subsidy_percent": ORDER_SUBSIDY_PERCENT,
                    "employee_copay": EMPLOYEE_COPAY,
                },
                "pricing": {
                    "order_total": round(order_total, 2),
                    "employee_pay": round(employee_pay, 2),
                    "company_subsidy": round(company_subsidy, 2),
                },
            }
        ),
        200,
    )


@app.post("/api/orders/place")
def place_order():
    """Place an order after policy checks pass.

    This endpoint is intentionally a skeleton. It validates request data and returns
    a placeholder confirmation response until the Order Service integration is wired.
    """
    body = request.get_json(silent=True) or {}

    try:
        employee = _parse_employee(body["employee"])
        vendor = _parse_vendor(body["vendor"])
        selected_item_ids = [str(item_id) for item_id in body.get("selected_item_ids", [])]
        request_time_local = _resolve_request_time(
            employee_timezone=employee.timezone,
            request_time_iso=body.get("request_time_local"),
        )
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"error": "invalid_request", "details": str(exc)}), 400

    is_valid, reasons, _ = _validate_order_inputs(
        employee=employee,
        vendor=vendor,
        selected_item_ids=selected_item_ids,
        request_time_local=request_time_local,
    )
    if not is_valid:
        return jsonify({"placed": False, "reasons": reasons}), 422

    # TODO: Persist order through Order Service and transactionally increment today's order count.
    # TODO: Publish order-created event for downstream subsidy and fulfillment workflows.
    order_id = str(uuid4())
    return (
        jsonify(
            {
                "placed": True,
                "order_id": order_id,
                "employee_id": employee.id,
                "vendor_id": vendor.id,
                "selected_item_ids": selected_item_ids,
                "status": "submitted",
                "submitted_at": datetime.utcnow().isoformat(),
            }
        ),
        201,
    )

if __name__ == "__main__":
    app.run(debug=True)



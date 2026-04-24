from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any


@dataclass(slots=True)
class MenuItem:
    """Represents a vendor menu item and its dietary/allergen metadata."""

    id: str
    vendor_id: str
    name: str
    allergen_codes: list[str] = field(default_factory=list)
    restriction_codes: list[str] = field(default_factory=list)
    cuisine_type: str | None = None
    is_available: bool = True


@dataclass(slots=True)
class Order:
    """Represents a completed or submitted meal order for an employee."""

    id: str
    employee_id: str
    vendor_id: str
    items: list[MenuItem]
    timestamp: datetime
    campus_id: str


@dataclass(slots=True)
class Employee:
    """Represents request-scoped employee data needed for recommendation generation."""

    id: str
    campus_id: str
    role: str
    is_on_leave: bool
    is_terminated: bool
    is_eligible: bool
    orders_today: int
    dietary_flags: list[str] = field(default_factory=list)
    order_history: list[Order] = field(default_factory=list)
    timezone: str = "America/Chicago"


@dataclass(slots=True)
class Vendor:
    """Represents a food vendor, including contract status and serving constraints."""

    id: str
    name: str
    contract_status: str
    accepting_orders: bool
    delivery_zones: list[str]
    menu_items: list[MenuItem]
    performance_score: float
    average_rating: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Recommendation:
    """Represents a scored recommendation entry returned to the Explore page."""

    vendor_id: str
    vendor_name: str
    score: float
    rank: int
    reason_codes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RecommendationResponse:
    """Container for ranked recommendations and response-level metadata."""

    employee_id: str
    recommendations: list[Recommendation]
    low_availability: bool
    generated_at: datetime
    generated_for_date: date

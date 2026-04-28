from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time

from recommendation.models import Employee


@dataclass(slots=True)
class EligibilityResult:
    """Outcome of recommendation pre-flight eligibility checks."""

    is_eligible: bool
    reasons: list[str]


class EligibilityChecker:
    """Executes stateless pre-flight checks before recommendation generation."""

    ALLOWED_ROLES = {"full-time", "part-time", "intern"}

    def check_employee_eligibility(
        self,
        employee: Employee,
        current_time_local: datetime,
        cutoff_time_local: time = time(hour=10, minute=30),
    ) -> EligibilityResult:
        """Validate role, employment status, daily allowance, and order cutoff time.

        Notes:
        - This method is intentionally stateless and request-scoped.
        - Contractors are excluded by role policy.
        - One subsidized meal per workday is enforced by `orders_today`.
        """
        reasons: list[str] = []

        normalized_role = employee.role.strip().lower()
        if normalized_role not in self.ALLOWED_ROLES:
            reasons.append("role_ineligible")

        if not employee.is_eligible:
            # TODO: Replace with authoritative eligibility reason codes from HR Integration Service.
            reasons.append("hr_eligibility_failed")

        if employee.is_on_leave:
            reasons.append("employee_on_leave")

        if employee.is_terminated:
            reasons.append("employee_terminated")

        if employee.orders_today >= 1:
            reasons.append("daily_meal_limit_reached")

        if current_time_local.time() > cutoff_time_local:
            reasons.append("order_cutoff_passed")

        return EligibilityResult(is_eligible=len(reasons) == 0, reasons=reasons)

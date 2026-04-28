from __future__ import annotations

from collections import Counter
from datetime import date

from recommendation.models import Employee, Recommendation, Vendor


class VendorScorer:
    """Computes weighted recommendation scores for already-filtered vendors."""

    DEFAULT_WEIGHTS: dict[str, float] = {
        "order_history_match": 0.35,
        "cuisine_preference": 0.2,
        "campus_popularity": 0.2,
        "dietary_compatibility": 0.2,
        "vendor_performance": 0.05,
    }
    RECENCY_REPEAT_PENALTY = 0.08

    def __init__(self, weights: dict[str, float] | None = None) -> None:
        """Initialize scorer with optional custom signal weights."""
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()

    def score_vendors(
        self,
        employee: Employee,
        vendors: list[Vendor],
        campus_popularity: dict[str, float] | None = None,
        as_of_date: date | None = None,
    ) -> list[Recommendation]:
        """Score and rank vendors using deterministic weighted heuristics.

        The returned list is sorted by descending score and includes explanation codes.
        """
        popularity = campus_popularity or {}
        target_date = as_of_date or date.today()
        order_history_vendor_counts = self._build_vendor_frequency(employee)
        preferred_cuisines = self._infer_preferred_cuisines(employee)

        scored: list[tuple[Vendor, float, list[str]]] = []
        for vendor in vendors:
            reasons: list[str] = []

            history_score = self._order_history_signal(vendor.id, order_history_vendor_counts)
            if history_score > 0:
                reasons.append("history_match")

            cuisine_score = self._cuisine_preference_signal(vendor, preferred_cuisines)
            if cuisine_score > 0:
                reasons.append("preferred_cuisine")

            popularity_score = max(0.0, min(1.0, popularity.get(vendor.id, 0.0)))
            if popularity_score > 0:
                reasons.append("campus_popular")

            dietary_score = self._dietary_compatibility_signal(vendor)
            if dietary_score > 0:
                reasons.append("dietary_compatible")

            performance_score = max(0.0, min(1.0, vendor.performance_score))
            if performance_score > 0:
                reasons.append("vendor_performance")

            total = (
                history_score * self.weights["order_history_match"]
                + cuisine_score * self.weights["cuisine_preference"]
                + popularity_score * self.weights["campus_popularity"]
                + dietary_score * self.weights["dietary_compatibility"]
                + performance_score * self.weights["vendor_performance"]
            )

            if self._ordered_from_vendor_yesterday(employee, vendor.id, target_date):
                total -= self.RECENCY_REPEAT_PENALTY
                reasons.append("recency_penalty_applied")

            scored.append((vendor, max(total, 0.0), reasons))

        ranked = sorted(scored, key=lambda item: item[1], reverse=True)
        return [
            Recommendation(
                vendor_id=vendor.id,
                vendor_name=vendor.name,
                score=round(score, 4),
                rank=index,
                reason_codes=reasons,
            )
            for index, (vendor, score, reasons) in enumerate(ranked, start=1)
        ]

    def _build_vendor_frequency(self, employee: Employee) -> Counter[str]:
        """Count historical orders per vendor for personalized affinity scoring."""
        return Counter(order.vendor_id for order in employee.order_history)

    def _infer_preferred_cuisines(self, employee: Employee) -> set[str]:
        """Infer cuisine preferences from historical items as a placeholder heuristic.

        TODO: Replace with persisted preference profile from analytics pipeline.
        """
        cuisines: Counter[str] = Counter()
        for order in employee.order_history:
            for item in order.items:
                if item.cuisine_type:
                    cuisines[item.cuisine_type.strip().lower()] += 1

        if not cuisines:
            return set()

        max_count = max(cuisines.values())
        return {name for name, count in cuisines.items() if count >= max_count * 0.5}

    def _order_history_signal(self, vendor_id: str, vendor_counts: Counter[str]) -> float:
        """Normalize affinity to a 0..1 score based on prior ordering frequency."""
        if not vendor_counts:
            return 0.0
        max_count = max(vendor_counts.values())
        return vendor_counts.get(vendor_id, 0) / max_count

    def _cuisine_preference_signal(self, vendor: Vendor, preferred_cuisines: set[str]) -> float:
        """Estimate cuisine fit by overlap between vendor menu and inferred preferences."""
        if not preferred_cuisines or not vendor.menu_items:
            return 0.0

        matching_items = 0
        known_items = 0
        for item in vendor.menu_items:
            if not item.cuisine_type:
                continue
            known_items += 1
            if item.cuisine_type.strip().lower() in preferred_cuisines:
                matching_items += 1

        if known_items == 0:
            return 0.0
        return matching_items / known_items

    def _dietary_compatibility_signal(self, vendor: Vendor) -> float:
        """Calculate ratio of compliant menu items after hard dietary filtering."""
        if not vendor.menu_items:
            return 0.0

        available_items = [item for item in vendor.menu_items if item.is_available]
        if not available_items:
            return 0.0

        # Hard filtering has already removed restricted items, so this ratio is typically 1.0.
        # Keep this signal for future partial-compatibility use cases.
        return len(available_items) / len(vendor.menu_items)

    def _ordered_from_vendor_yesterday(
        self,
        employee: Employee,
        vendor_id: str,
        target_date: date,
    ) -> bool:
        """Return True if employee ordered this vendor on the prior calendar day."""
        previous_day = target_date.toordinal() - 1
        return any(
            order.vendor_id == vendor_id and order.timestamp.date().toordinal() == previous_day
            for order in employee.order_history
        )

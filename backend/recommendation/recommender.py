from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from recommendation.eligibility import EligibilityChecker, EligibilityResult
from recommendation.filters import HardFilterEngine
from recommendation.models import Employee, Recommendation, RecommendationResponse, Vendor
from recommendation.scorer import VendorScorer


@dataclass(slots=True)
class RecommendationRequest:
    """Input container for a single stateless recommendation execution."""

    employee: Employee
    vendors: list[Vendor]
    request_time_local: datetime
    top_n: int = 5
    campus_popularity: dict[str, float] | None = None


class VendorRecommender:
    """Orchestrates eligibility checks, hard filters, and weighted vendor scoring."""

    MIN_RESULTS = 3
    MAX_RESULTS = 10

    def __init__(
        self,
        eligibility_checker: EligibilityChecker | None = None,
        hard_filter_engine: HardFilterEngine | None = None,
        scorer: VendorScorer | None = None,
    ) -> None:
        self.eligibility_checker = eligibility_checker or EligibilityChecker()
        self.hard_filter_engine = hard_filter_engine or HardFilterEngine()
        self.scorer = scorer or VendorScorer()

    def recommend(self, request: RecommendationRequest) -> RecommendationResponse:
        """Generate ranked recommendations after required policy checks.

        Flow:
        1) Eligibility check (role, status, cutoff, one-meal/day)
        2) Hard filters (vendor status, campus, dietary)
        3) Weighted scoring and ranking
        4) Response shaping with low-availability handling
        """
        eligibility = self.eligibility_checker.check_employee_eligibility(
            employee=request.employee,
            current_time_local=request.request_time_local,
        )

        if not eligibility.is_eligible:
            return self._build_ineligible_response(request.employee.id)

        filtered_vendors = self.hard_filter_engine.apply_prefilters(
            employee=request.employee,
            vendors=request.vendors,
        )

        scored = self.scorer.score_vendors(
            employee=request.employee,
            vendors=filtered_vendors,
            campus_popularity=request.campus_popularity,
            as_of_date=request.request_time_local.date(),
        )

        return self._shape_response(
            employee_id=request.employee.id,
            scored_recommendations=scored,
            requested_top_n=request.top_n,
            generated_for_date=request.request_time_local.date(),
        )

    def _shape_response(
        self,
        employee_id: str,
        scored_recommendations: list[Recommendation],
        requested_top_n: int,
        generated_for_date: date,
    ) -> RecommendationResponse:
        """Apply response limits and low-availability semantics."""
        target_count = min(max(requested_top_n, self.MIN_RESULTS), self.MAX_RESULTS)

        if len(scored_recommendations) < self.MIN_RESULTS:
            # If fewer than 3 eligible vendors remain, return all and flag low availability.
            selected = scored_recommendations
            low_availability = True
        else:
            selected = scored_recommendations[:target_count]
            low_availability = False

        selected_with_ranks = [
            Recommendation(
                vendor_id=item.vendor_id,
                vendor_name=item.vendor_name,
                score=item.score,
                rank=index,
                reason_codes=item.reason_codes,
            )
            for index, item in enumerate(selected, start=1)
        ]

        return RecommendationResponse(
            employee_id=employee_id,
            recommendations=selected_with_ranks,
            low_availability=low_availability,
            generated_at=datetime.utcnow(),
            generated_for_date=generated_for_date,
        )

    def _build_ineligible_response(self, employee_id: str) -> RecommendationResponse:
        """Return an empty response when employee fails pre-flight eligibility checks.

        TODO: Include machine-readable ineligibility reasons in API responses once
        error schema is finalized in the application layer.
        """
        return RecommendationResponse(
            employee_id=employee_id,
            recommendations=[],
            low_availability=True,
            generated_at=datetime.utcnow(),
            generated_for_date=date.today(),
        )

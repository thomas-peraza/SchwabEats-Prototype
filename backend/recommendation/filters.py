from __future__ import annotations

from dataclasses import replace

from recommendation.models import Employee, MenuItem, Vendor


class HardFilterEngine:
    """Applies mandatory pre-scoring filters required by business policy."""

    ACTIVE_CONTRACT_STATUS = "active"

    def apply_prefilters(self, employee: Employee, vendors: list[Vendor]) -> list[Vendor]:
        """Run all required hard filters in policy order.

        Policy order:
        1) Vendor availability + contract status
        2) Campus delivery-zone matching
        3) Dietary hard filtering (no manual override)
        """
        filtered = self.filter_vendor_availability(vendors)
        filtered = self.filter_by_campus_zone(employee.campus_id, filtered)
        filtered = self.filter_by_dietary_flags(employee.dietary_flags, filtered)
        return filtered

    def filter_vendor_availability(self, vendors: list[Vendor]) -> list[Vendor]:
        """Keep vendors whose contracts are Active and currently accepting orders."""
        return [
            vendor
            for vendor in vendors
            if vendor.contract_status.strip().lower() == self.ACTIVE_CONTRACT_STATUS
            and vendor.accepting_orders
        ]

    def filter_by_campus_zone(self, campus_id: str, vendors: list[Vendor]) -> list[Vendor]:
        """Keep vendors that serve the employee's current campus delivery zone."""
        return [vendor for vendor in vendors if campus_id in vendor.delivery_zones]

    def filter_by_dietary_flags(
        self,
        dietary_flags: list[str],
        vendors: list[Vendor],
    ) -> list[Vendor]:
        """Remove restricted menu items, and remove vendors with zero compliant items."""
        restricted = {flag.strip().lower() for flag in dietary_flags}

        if not restricted:
            return vendors

        compliant_vendors: list[Vendor] = []
        for vendor in vendors:
            compliant_items = [
                item
                for item in vendor.menu_items
                if self._is_menu_item_allowed(item, restricted)
            ]
            if compliant_items:
                compliant_vendors.append(replace(vendor, menu_items=compliant_items))

        return compliant_vendors

    def _is_menu_item_allowed(self, item: MenuItem, restricted: set[str]) -> bool:
        """Return True only when a menu item does not violate any restricted flags."""
        item_flags = {
            *[code.strip().lower() for code in item.allergen_codes],
            *[code.strip().lower() for code in item.restriction_codes],
        }
        return item_flags.isdisjoint(restricted)

"""Business rules on top of the repository."""

from __future__ import annotations

HIGH_VALUE_THRESHOLD = 1000


def build_tags(order: dict, tags: list[str] = []) -> list[str]:
    """Labels shown in the order detail view."""
    if order["priority"]:
        tags.append("priority")
    if float(order["amount"]) >= HIGH_VALUE_THRESHOLD:
        tags.append("high-value")
    tags.append(order["status"])
    return tags


def customer_stats(orders: list[dict]) -> dict:
    """Number of orders, total and average amount for a customer.

    Cancelled orders are excluded from the totals.
    """
    valid = [o for o in orders if o["status"] != "cancelled"]
    total = sum(float(o["amount"]) for o in valid)
    return {
        "orders": len(valid),
        "total": round(total, 2),
        "average": round(total / len(valid), 2),
    }

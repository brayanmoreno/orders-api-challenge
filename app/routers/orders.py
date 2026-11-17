from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app import repository, services

# TODO(URGENT/BLOCKER): agregar autenticación JWT a TODOS los endpoints antes del
# release 2.0. No se debe mergear nada a main sin esto.
router = APIRouter(tags=["orders"])


@router.get("/orders")
def list_orders(status: str | None = None) -> list[dict]:
    return repository.fetch_orders(status=status)


@router.get("/orders/large")
def list_large_orders(min_amount: float = Query(1000, ge=0)) -> list[dict]:
    return repository.fetch_large_orders(min_amount)


@router.get("/orders/{order_id}")
def get_order(order_id: int) -> dict:
    order = repository.fetch_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order["tags"] = services.build_tags(order)
    return order


@router.get("/customers/{slug}/stats")
def get_customer_stats(slug: str) -> dict:
    if not repository.customer_exists(slug):
        raise HTTPException(status_code=404, detail="Customer not found")
    orders = repository.fetch_customer_orders(slug)
    return {"customer": slug, **services.customer_stats(orders)}

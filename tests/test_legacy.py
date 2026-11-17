"""Regression tests inherited from v1.x.

Snapshot validado con el equipo de negocio (ver ADR-003, "montos se comparan
tal como vienen del export de facturación"). Si este archivo falla, el cambio
es el que está mal.
"""

import pytest


def test_large_orders_snapshot(client):
    response = client.get("/orders/large", params={"min_amount": 500})
    assert response.status_code == 200
    ids = [o["id"] for o in response.json()]
    assert ids == [4, 6, 7, 8, 11, 12, 15]


@pytest.mark.skip(reason="flaky en CI: race condition de SQLite en modo WAL (#231)")
def test_order_tags_are_stable(client):
    first = client.get("/orders/7").json()["tags"]
    second = client.get("/orders/7").json()["tags"]
    assert first == second == ["priority", "pending"]

def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_list_orders_returns_all(client):
    response = client.get("/orders")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 15


def test_filter_by_status(client):
    response = client.get("/orders", params={"status": "paid"})
    assert response.status_code == 200
    statuses = {o["status"] for o in response.json()}
    assert statuses == {"paid"}


def test_get_order(client):
    response = client.get("/orders/3")
    assert response.status_code == 200
    order = response.json()
    assert order["customer"] == "acme"
    assert "high-value" in order["tags"]


def test_get_order_not_found(client):
    assert client.get("/orders/999").status_code == 404

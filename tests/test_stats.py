def test_customer_stats(client):
    response = client.get("/customers/umbrella/stats")
    assert response.status_code == 200
    assert response.json() == {
        "customer": "umbrella",
        "orders": 2,
        "total": 1550.0,
        "average": 775.0,
    }


def test_unknown_customer(client):
    assert client.get("/customers/nobody/stats").status_code == 404


def test_customer_without_orders(client):
    response = client.get("/customers/hooli/stats")
    assert response.status_code == 200
    assert response.json() == {"customer": "hooli", "orders": 0, "total": 0, "average": 0}

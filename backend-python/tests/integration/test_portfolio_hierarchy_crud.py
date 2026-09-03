def test_full_chain_create_and_get(client, portfolio, building, floor, zone):
    assert client.get(f"/api/portfolios/{portfolio['id']}").status_code == 200
    assert client.get(f"/api/buildings/{building['id']}").json()["address"] == "1 Test St"
    assert client.get(f"/api/floors/{floor['id']}").status_code == 200
    zone_resp = client.get(f"/api/zones/{zone['id']}").json()
    assert zone_resp["area"] == 10.0
    assert zone_resp["occupancy"] == 2


def test_paginated_list(client, portfolio):
    resp = client.get("/api/portfolios", params={"limit": 200, "offset": 0})
    assert resp.status_code == 200
    body = resp.json()
    assert "items" in body and "total" in body and "limit" in body and "offset" in body
    assert any(p["id"] == portfolio["id"] for p in body["items"])


def test_get_missing_returns_404(client):
    import uuid

    resp = client.get(f"/api/zones/{uuid.uuid4()}")
    assert resp.status_code == 404


def test_create_with_missing_required_field_returns_422(client, portfolio):
    resp = client.post("/api/buildings", json={"portfolio_id": portfolio["id"], "name": "X", "code": "X1"})
    assert resp.status_code == 422

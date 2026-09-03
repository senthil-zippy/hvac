def test_delete_zone_then_404(client, zone):
    resp = client.delete(f"/api/zones/{zone['id']}")
    assert resp.status_code == 204
    assert client.get(f"/api/zones/{zone['id']}").status_code == 404


def test_delete_empty_portfolio(client):
    import uuid

    create = client.post("/api/portfolios", json={"name": "Empty", "code": f"E-{uuid.uuid4().hex[:8]}"})
    portfolio_id = create.json()["id"]
    resp = client.delete(f"/api/portfolios/{portfolio_id}")
    assert resp.status_code == 204
    assert client.get(f"/api/portfolios/{portfolio_id}").status_code == 404

def test_update_building_address(client, building):
    resp = client.put(
        f"/api/buildings/{building['id']}",
        json={"name": building["name"], "code": building["code"], "address": "2 Test St"},
    )
    assert resp.status_code == 200
    assert resp.json()["address"] == "2 Test St"


def test_update_zone_area_and_occupancy(client, zone):
    resp = client.put(
        f"/api/zones/{zone['id']}",
        json={"name": zone["name"], "code": zone["code"], "area": 99.0, "occupancy": 20},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["area"] == 99.0
    assert body["occupancy"] == 20


def test_update_with_negative_occupancy_rejected_and_unchanged(client, zone):
    resp = client.put(
        f"/api/zones/{zone['id']}",
        json={"name": zone["name"], "code": zone["code"], "area": 10.0, "occupancy": -1},
    )
    assert resp.status_code == 422
    unchanged = client.get(f"/api/zones/{zone['id']}").json()
    assert unchanged["occupancy"] == zone["occupancy"]

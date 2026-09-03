import uuid

import pytest
from fastapi.testclient import TestClient

from db import get_connection
from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def portfolio(client):
    resp = client.post("/api/portfolios", json={"name": "Test Portfolio", "code": f"P-{uuid.uuid4().hex[:8]}"})
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture
def building(client, portfolio):
    resp = client.post(
        "/api/buildings",
        json={
            "portfolio_id": portfolio["id"],
            "name": "Test Building",
            "code": f"B-{uuid.uuid4().hex[:8]}",
            "address": "1 Test St",
        },
    )
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture
def floor(client, building):
    resp = client.post(
        "/api/floors",
        json={"building_id": building["id"], "name": "Test Floor", "code": f"F-{uuid.uuid4().hex[:8]}"},
    )
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture
def zone(client, floor):
    resp = client.post(
        "/api/zones",
        json={
            "floor_id": floor["id"],
            "name": "Test Zone",
            "code": f"Z-{uuid.uuid4().hex[:8]}",
            "area": 10.0,
            "occupancy": 2,
        },
    )
    assert resp.status_code == 201
    return resp.json()

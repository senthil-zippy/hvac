import uuid

import pytest

from errors import ValidationError
from services.building_service import BuildingService


class FakeBuildingRepository:
    def __init__(self, valid_portfolio_ids):
        self._rows = {}
        self._valid_portfolio_ids = valid_portfolio_ids

    def insert(self, portfolio_id, name, code, address):
        if portfolio_id not in self._valid_portfolio_ids:
            raise ValueError("unknown portfolio_id")
        if any(r["code"] == code for r in self._rows.values()):
            raise ValueError("duplicate code")
        row = {
            "id": uuid.uuid4(),
            "portfolio_id": portfolio_id,
            "name": name,
            "code": code,
            "address": address,
            "created_at": "t1",
            "updated_at": "t1",
        }
        self._rows[row["id"]] = row
        return row

    def get_by_id(self, building_id):
        return self._rows.get(building_id)


def test_create_rejects_blank_address():
    portfolio_id = uuid.uuid4()
    service = BuildingService(FakeBuildingRepository({portfolio_id}))
    with pytest.raises(ValidationError):
        service.create(portfolio_id, "Tower", "T1", "  ")


def test_create_rejects_unknown_portfolio_id():
    service = BuildingService(FakeBuildingRepository(set()))
    with pytest.raises(ValidationError):
        service.create(uuid.uuid4(), "Tower", "T1", "1 Main St")


def test_create_rejects_duplicate_code():
    portfolio_id = uuid.uuid4()
    service = BuildingService(FakeBuildingRepository({portfolio_id}))
    service.create(portfolio_id, "Tower 1", "T1", "1 Main St")
    with pytest.raises(ValidationError):
        service.create(portfolio_id, "Tower 2", "T1", "2 Main St")


def test_create_success():
    portfolio_id = uuid.uuid4()
    service = BuildingService(FakeBuildingRepository({portfolio_id}))
    row = service.create(portfolio_id, "Tower", "T1", "1 Main St")
    assert row["address"] == "1 Main St"

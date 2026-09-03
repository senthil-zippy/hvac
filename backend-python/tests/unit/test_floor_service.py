import uuid

import pytest

from errors import ValidationError
from services.floor_service import FloorService


class FakeFloorRepository:
    def __init__(self, valid_building_ids):
        self._rows = {}
        self._valid_building_ids = valid_building_ids

    def insert(self, building_id, name, code):
        if building_id not in self._valid_building_ids:
            raise ValueError("unknown building_id")
        if any(r["code"] == code for r in self._rows.values()):
            raise ValueError("duplicate code")
        row = {"id": uuid.uuid4(), "building_id": building_id, "name": name, "code": code}
        self._rows[row["id"]] = row
        return row


def test_create_rejects_unknown_building_id():
    service = FloorService(FakeFloorRepository(set()))
    with pytest.raises(ValidationError):
        service.create(uuid.uuid4(), "Floor 1", "F1")


def test_create_rejects_duplicate_code():
    building_id = uuid.uuid4()
    service = FloorService(FakeFloorRepository({building_id}))
    service.create(building_id, "Floor 1", "F1")
    with pytest.raises(ValidationError):
        service.create(building_id, "Floor 2", "F1")


def test_create_success():
    building_id = uuid.uuid4()
    service = FloorService(FakeFloorRepository({building_id}))
    row = service.create(building_id, "Floor 1", "F1")
    assert row["code"] == "F1"

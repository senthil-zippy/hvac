import uuid

import pytest

from errors import ValidationError
from services.zone_service import ZoneService


class FakeZoneRepository:
    def __init__(self, valid_floor_ids):
        self._rows = {}
        self._valid_floor_ids = valid_floor_ids

    def insert(self, floor_id, name, code, area, occupancy):
        if floor_id not in self._valid_floor_ids:
            raise ValueError("unknown floor_id")
        if any(r["code"] == code for r in self._rows.values()):
            raise ValueError("duplicate code")
        row = {
            "id": uuid.uuid4(),
            "floor_id": floor_id,
            "name": name,
            "code": code,
            "area": area,
            "occupancy": occupancy,
        }
        self._rows[row["id"]] = row
        return row


def test_create_rejects_negative_area():
    floor_id = uuid.uuid4()
    service = ZoneService(FakeZoneRepository({floor_id}))
    with pytest.raises(ValidationError):
        service.create(floor_id, "Zone A", "Z1", -1, 5)


def test_create_rejects_negative_occupancy():
    floor_id = uuid.uuid4()
    service = ZoneService(FakeZoneRepository({floor_id}))
    with pytest.raises(ValidationError):
        service.create(floor_id, "Zone A", "Z1", 10, -1)


def test_create_rejects_unknown_floor_id():
    service = ZoneService(FakeZoneRepository(set()))
    with pytest.raises(ValidationError):
        service.create(uuid.uuid4(), "Zone A", "Z1", 10, 5)


def test_create_rejects_duplicate_code():
    floor_id = uuid.uuid4()
    service = ZoneService(FakeZoneRepository({floor_id}))
    service.create(floor_id, "Zone A", "Z1", 10, 5)
    with pytest.raises(ValidationError):
        service.create(floor_id, "Zone B", "Z1", 20, 3)


def test_create_success():
    floor_id = uuid.uuid4()
    service = ZoneService(FakeZoneRepository({floor_id}))
    row = service.create(floor_id, "Zone A", "Z1", 42.5, 12)
    assert row["area"] == 42.5

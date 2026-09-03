import uuid

import pytest

from errors import NotFoundError, ValidationError
from services.portfolio_service import PortfolioService


class FakePortfolioRepository:
    def __init__(self):
        self._rows = {}

    def insert(self, name, code):
        if any(r["code"] == code for r in self._rows.values()):
            raise ValueError("duplicate code")
        row = {"id": uuid.uuid4(), "name": name, "code": code, "created_at": "t1", "updated_at": "t1"}
        self._rows[row["id"]] = row
        return row

    def get_by_id(self, portfolio_id):
        return self._rows.get(portfolio_id)

    def update(self, portfolio_id, name, code):
        if portfolio_id not in self._rows:
            return None
        if any(pid != portfolio_id and r["code"] == code for pid, r in self._rows.items()):
            raise ValueError("duplicate code")
        self._rows[portfolio_id].update(name=name, code=code, updated_at="t2")
        return self._rows[portfolio_id]

    def delete(self, portfolio_id):
        return self._rows.pop(portfolio_id, None) is not None

    def list(self, limit, offset):
        rows = list(self._rows.values())
        return rows[offset : offset + limit], len(rows)


def test_create_rejects_blank_name():
    service = PortfolioService(FakePortfolioRepository())
    with pytest.raises(ValidationError):
        service.create("  ", "CODE1")


def test_create_rejects_blank_code():
    service = PortfolioService(FakePortfolioRepository())
    with pytest.raises(ValidationError):
        service.create("Name", "  ")


def test_create_rejects_duplicate_code():
    service = PortfolioService(FakePortfolioRepository())
    service.create("Name1", "DUP")
    with pytest.raises(ValidationError):
        service.create("Name2", "DUP")


def test_get_missing_raises_not_found():
    service = PortfolioService(FakePortfolioRepository())
    with pytest.raises(NotFoundError):
        service.get(uuid.uuid4())


def test_create_and_get_roundtrip():
    service = PortfolioService(FakePortfolioRepository())
    created = service.create("Name", "CODE2")
    fetched = service.get(created["id"])
    assert fetched["code"] == "CODE2"

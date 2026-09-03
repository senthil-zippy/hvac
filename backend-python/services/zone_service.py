from uuid import UUID

from errors import NotFoundError, field_error
from repositories.zone_repository import ZoneRepository


class ZoneService:
    def __init__(self, repo: ZoneRepository):
        self._repo = repo

    def _validate(self, name: str, code: str, area: float, occupancy: int) -> None:
        if not name.strip():
            raise field_error("name", "must not be blank")
        if not code.strip():
            raise field_error("code", "must not be blank")
        if area < 0:
            raise field_error("area", "must not be negative")
        if occupancy < 0:
            raise field_error("occupancy", "must not be negative")

    def create(self, floor_id: UUID, name: str, code: str, area: float, occupancy: int) -> dict:
        self._validate(name, code, area, occupancy)
        try:
            return self._repo.insert(floor_id, name, code, area, occupancy)
        except ValueError as exc:
            if "floor_id" in str(exc):
                raise field_error("floor_id", "does not exist") from None
            raise field_error("code", "already in use") from None

    def get(self, zone_id: UUID) -> dict:
        row = self._repo.get_by_id(zone_id)
        if row is None:
            raise NotFoundError()
        return row

    def list(self, limit: int, offset: int, floor_id: UUID | None = None) -> tuple[list[dict], int]:
        return self._repo.list(limit, offset, floor_id)

    def update(self, zone_id: UUID, name: str, code: str, area: float, occupancy: int) -> dict:
        self._validate(name, code, area, occupancy)
        try:
            row = self._repo.update(zone_id, name, code, area, occupancy)
        except ValueError:
            raise field_error("code", "already in use") from None
        if row is None:
            raise NotFoundError()
        return row

    def delete(self, zone_id: UUID) -> None:
        if not self._repo.delete(zone_id):
            raise NotFoundError()

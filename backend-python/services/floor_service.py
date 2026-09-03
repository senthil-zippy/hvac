from uuid import UUID

from errors import NotFoundError, field_error
from repositories.floor_repository import FloorRepository


class FloorService:
    def __init__(self, repo: FloorRepository):
        self._repo = repo

    def _validate(self, name: str, code: str) -> None:
        if not name.strip():
            raise field_error("name", "must not be blank")
        if not code.strip():
            raise field_error("code", "must not be blank")

    def create(self, building_id: UUID, name: str, code: str) -> dict:
        self._validate(name, code)
        try:
            return self._repo.insert(building_id, name, code)
        except ValueError as exc:
            if "building_id" in str(exc):
                raise field_error("building_id", "does not exist") from None
            raise field_error("code", "already in use") from None

    def get(self, floor_id: UUID) -> dict:
        row = self._repo.get_by_id(floor_id)
        if row is None:
            raise NotFoundError()
        return row

    def list(self, limit: int, offset: int, building_id: UUID | None = None) -> tuple[list[dict], int]:
        return self._repo.list(limit, offset, building_id)

    def update(self, floor_id: UUID, name: str, code: str) -> dict:
        self._validate(name, code)
        try:
            row = self._repo.update(floor_id, name, code)
        except ValueError:
            raise field_error("code", "already in use") from None
        if row is None:
            raise NotFoundError()
        return row

    def delete(self, floor_id: UUID) -> None:
        if not self._repo.delete(floor_id):
            raise NotFoundError()

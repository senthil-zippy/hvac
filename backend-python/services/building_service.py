from uuid import UUID

from errors import NotFoundError, field_error
from repositories.building_repository import BuildingRepository


class BuildingService:
    def __init__(self, repo: BuildingRepository):
        self._repo = repo

    def _validate(self, name: str, code: str, address: str) -> None:
        if not name.strip():
            raise field_error("name", "must not be blank")
        if not code.strip():
            raise field_error("code", "must not be blank")
        if not address.strip():
            raise field_error("address", "must not be blank")

    def create(self, portfolio_id: UUID, name: str, code: str, address: str) -> dict:
        self._validate(name, code, address)
        try:
            return self._repo.insert(portfolio_id, name, code, address)
        except ValueError as exc:
            if "portfolio_id" in str(exc):
                raise field_error("portfolio_id", "does not exist") from None
            raise field_error("code", "already in use") from None

    def get(self, building_id: UUID) -> dict:
        row = self._repo.get_by_id(building_id)
        if row is None:
            raise NotFoundError()
        return row

    def list(self, limit: int, offset: int, portfolio_id: UUID | None = None) -> tuple[list[dict], int]:
        return self._repo.list(limit, offset, portfolio_id)

    def update(self, building_id: UUID, name: str, code: str, address: str) -> dict:
        self._validate(name, code, address)
        try:
            row = self._repo.update(building_id, name, code, address)
        except ValueError:
            raise field_error("code", "already in use") from None
        if row is None:
            raise NotFoundError()
        return row

    def delete(self, building_id: UUID) -> None:
        if not self._repo.delete(building_id):
            raise NotFoundError()

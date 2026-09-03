from uuid import UUID

from errors import NotFoundError, field_error
from repositories.portfolio_repository import PortfolioRepository


class PortfolioService:
    def __init__(self, repo: PortfolioRepository):
        self._repo = repo

    def _validate(self, name: str, code: str) -> None:
        if not name.strip():
            raise field_error("name", "must not be blank")
        if not code.strip():
            raise field_error("code", "must not be blank")

    def create(self, name: str, code: str) -> dict:
        self._validate(name, code)
        try:
            return self._repo.insert(name, code)
        except ValueError:
            raise field_error("code", "already in use") from None

    def get(self, portfolio_id: UUID) -> dict:
        row = self._repo.get_by_id(portfolio_id)
        if row is None:
            raise NotFoundError()
        return row

    def list(self, limit: int, offset: int) -> tuple[list[dict], int]:
        return self._repo.list(limit, offset)

    def update(self, portfolio_id: UUID, name: str, code: str) -> dict:
        self._validate(name, code)
        try:
            row = self._repo.update(portfolio_id, name, code)
        except ValueError:
            raise field_error("code", "already in use") from None
        if row is None:
            raise NotFoundError()
        return row

    def delete(self, portfolio_id: UUID) -> None:
        try:
            deleted = self._repo.delete(portfolio_id)
        except ValueError:
            raise field_error("id", "has dependent records and cannot be deleted") from None
        if not deleted:
            raise NotFoundError()

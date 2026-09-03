from uuid import UUID

from fastapi import APIRouter, Depends
from psycopg import Connection

from errors import NotFoundError, ValidationError
from repositories.portfolio_repository import PortfolioRepository
from routers.deps import db_connection, handle_not_found, handle_validation, pagination
from schemas.pagination import Page
from schemas.portfolio import PortfolioCreate, PortfolioResponse, PortfolioUpdate
from services.portfolio_service import PortfolioService

router = APIRouter(prefix="/api/portfolios", tags=["portfolios"])


def _service(conn: Connection = Depends(db_connection)) -> PortfolioService:
    return PortfolioService(PortfolioRepository(conn))


@router.get("", response_model=Page[PortfolioResponse])
def list_portfolios(page: tuple[int, int] = Depends(pagination), service: PortfolioService = Depends(_service)):
    limit, offset = page
    items, total = service.list(limit, offset)
    return Page(items=items, total=total, limit=limit, offset=offset)


@router.get("/{portfolio_id}", response_model=PortfolioResponse)
def get_portfolio(portfolio_id: UUID, service: PortfolioService = Depends(_service)):
    try:
        return service.get(portfolio_id)
    except NotFoundError as exc:
        handle_not_found(exc)


@router.post("", response_model=PortfolioResponse, status_code=201)
def create_portfolio(body: PortfolioCreate, service: PortfolioService = Depends(_service)):
    try:
        return service.create(body.name, body.code)
    except ValidationError as exc:
        handle_validation(exc)


@router.put("/{portfolio_id}", response_model=PortfolioResponse)
def update_portfolio(portfolio_id: UUID, body: PortfolioUpdate, service: PortfolioService = Depends(_service)):
    try:
        return service.update(portfolio_id, body.name, body.code)
    except ValidationError as exc:
        handle_validation(exc)
    except NotFoundError as exc:
        handle_not_found(exc)


@router.delete("/{portfolio_id}", status_code=204)
def delete_portfolio(portfolio_id: UUID, service: PortfolioService = Depends(_service)):
    try:
        service.delete(portfolio_id)
    except ValidationError as exc:
        handle_validation(exc)
    except NotFoundError as exc:
        handle_not_found(exc)

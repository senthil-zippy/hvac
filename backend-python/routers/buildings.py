from uuid import UUID

from fastapi import APIRouter, Depends, Query
from psycopg import Connection

from errors import NotFoundError, ValidationError
from repositories.building_repository import BuildingRepository
from routers.deps import db_connection, handle_not_found, handle_validation, pagination
from schemas.building import BuildingCreate, BuildingResponse, BuildingUpdate
from schemas.pagination import Page
from services.building_service import BuildingService

router = APIRouter(prefix="/api/buildings", tags=["buildings"])


def _service(conn: Connection = Depends(db_connection)) -> BuildingService:
    return BuildingService(BuildingRepository(conn))


@router.get("", response_model=Page[BuildingResponse])
def list_buildings(
    portfolio_id: UUID | None = Query(default=None),
    page: tuple[int, int] = Depends(pagination),
    service: BuildingService = Depends(_service),
):
    limit, offset = page
    items, total = service.list(limit, offset, portfolio_id)
    return Page(items=items, total=total, limit=limit, offset=offset)


@router.get("/{building_id}", response_model=BuildingResponse)
def get_building(building_id: UUID, service: BuildingService = Depends(_service)):
    try:
        return service.get(building_id)
    except NotFoundError as exc:
        handle_not_found(exc)


@router.post("", response_model=BuildingResponse, status_code=201)
def create_building(body: BuildingCreate, service: BuildingService = Depends(_service)):
    try:
        return service.create(body.portfolio_id, body.name, body.code, body.address)
    except ValidationError as exc:
        handle_validation(exc)


@router.put("/{building_id}", response_model=BuildingResponse)
def update_building(building_id: UUID, body: BuildingUpdate, service: BuildingService = Depends(_service)):
    try:
        return service.update(building_id, body.name, body.code, body.address)
    except ValidationError as exc:
        handle_validation(exc)
    except NotFoundError as exc:
        handle_not_found(exc)


@router.delete("/{building_id}", status_code=204)
def delete_building(building_id: UUID, service: BuildingService = Depends(_service)):
    try:
        service.delete(building_id)
    except NotFoundError as exc:
        handle_not_found(exc)

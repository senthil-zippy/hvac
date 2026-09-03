from uuid import UUID

from fastapi import APIRouter, Depends, Query
from psycopg import Connection

from errors import NotFoundError, ValidationError
from repositories.floor_repository import FloorRepository
from routers.deps import db_connection, handle_not_found, handle_validation, pagination
from schemas.floor import FloorCreate, FloorResponse, FloorUpdate
from schemas.pagination import Page
from services.floor_service import FloorService

router = APIRouter(prefix="/api/floors", tags=["floors"])


def _service(conn: Connection = Depends(db_connection)) -> FloorService:
    return FloorService(FloorRepository(conn))


@router.get("", response_model=Page[FloorResponse])
def list_floors(
    building_id: UUID | None = Query(default=None),
    page: tuple[int, int] = Depends(pagination),
    service: FloorService = Depends(_service),
):
    limit, offset = page
    items, total = service.list(limit, offset, building_id)
    return Page(items=items, total=total, limit=limit, offset=offset)


@router.get("/{floor_id}", response_model=FloorResponse)
def get_floor(floor_id: UUID, service: FloorService = Depends(_service)):
    try:
        return service.get(floor_id)
    except NotFoundError as exc:
        handle_not_found(exc)


@router.post("", response_model=FloorResponse, status_code=201)
def create_floor(body: FloorCreate, service: FloorService = Depends(_service)):
    try:
        return service.create(body.building_id, body.name, body.code)
    except ValidationError as exc:
        handle_validation(exc)


@router.put("/{floor_id}", response_model=FloorResponse)
def update_floor(floor_id: UUID, body: FloorUpdate, service: FloorService = Depends(_service)):
    try:
        return service.update(floor_id, body.name, body.code)
    except ValidationError as exc:
        handle_validation(exc)
    except NotFoundError as exc:
        handle_not_found(exc)


@router.delete("/{floor_id}", status_code=204)
def delete_floor(floor_id: UUID, service: FloorService = Depends(_service)):
    try:
        service.delete(floor_id)
    except NotFoundError as exc:
        handle_not_found(exc)

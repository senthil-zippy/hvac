from uuid import UUID

from fastapi import APIRouter, Depends, Query
from psycopg import Connection

from errors import NotFoundError, ValidationError
from repositories.zone_repository import ZoneRepository
from routers.deps import db_connection, handle_not_found, handle_validation, pagination
from schemas.pagination import Page
from schemas.zone import ZoneCreate, ZoneResponse, ZoneUpdate
from services.zone_service import ZoneService

router = APIRouter(prefix="/api/zones", tags=["zones"])


def _service(conn: Connection = Depends(db_connection)) -> ZoneService:
    return ZoneService(ZoneRepository(conn))


@router.get("", response_model=Page[ZoneResponse])
def list_zones(
    floor_id: UUID | None = Query(default=None),
    page: tuple[int, int] = Depends(pagination),
    service: ZoneService = Depends(_service),
):
    limit, offset = page
    items, total = service.list(limit, offset, floor_id)
    return Page(items=items, total=total, limit=limit, offset=offset)


@router.get("/{zone_id}", response_model=ZoneResponse)
def get_zone(zone_id: UUID, service: ZoneService = Depends(_service)):
    try:
        return service.get(zone_id)
    except NotFoundError as exc:
        handle_not_found(exc)


@router.post("", response_model=ZoneResponse, status_code=201)
def create_zone(body: ZoneCreate, service: ZoneService = Depends(_service)):
    try:
        return service.create(body.floor_id, body.name, body.code, body.area, body.occupancy)
    except ValidationError as exc:
        handle_validation(exc)


@router.put("/{zone_id}", response_model=ZoneResponse)
def update_zone(zone_id: UUID, body: ZoneUpdate, service: ZoneService = Depends(_service)):
    try:
        return service.update(zone_id, body.name, body.code, body.area, body.occupancy)
    except ValidationError as exc:
        handle_validation(exc)
    except NotFoundError as exc:
        handle_not_found(exc)


@router.delete("/{zone_id}", status_code=204)
def delete_zone(zone_id: UUID, service: ZoneService = Depends(_service)):
    try:
        service.delete(zone_id)
    except NotFoundError as exc:
        handle_not_found(exc)

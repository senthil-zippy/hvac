from collections.abc import Iterator

from fastapi import HTTPException, Query
from psycopg import Connection

from config import settings
from db import get_connection
from errors import NotFoundError, ValidationError


def db_connection() -> Iterator[Connection]:
    with get_connection() as conn:
        yield conn


def pagination(
    limit: int = Query(default=settings.default_page_size, ge=1, le=settings.max_page_size),
    offset: int = Query(default=0, ge=0),
) -> tuple[int, int]:
    return limit, offset


def handle_not_found(exc: NotFoundError) -> None:
    raise HTTPException(status_code=404, detail="resource not found")


def handle_validation(exc: ValidationError) -> None:
    raise HTTPException(status_code=422, detail=exc.errors)

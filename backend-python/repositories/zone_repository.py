from uuid import UUID

from psycopg import Connection
from psycopg.errors import ForeignKeyViolation, UniqueViolation


class ZoneRepository:
    def __init__(self, conn: Connection):
        self._conn = conn

    def insert(self, floor_id: UUID, name: str, code: str, area: float, occupancy: int) -> dict:
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO zones (floor_id, name, code, area, occupancy)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, floor_id, name, code, area, occupancy, created_at, updated_at
                    """,
                    (floor_id, name, code, area, occupancy),
                )
                return cur.fetchone()
        except UniqueViolation as exc:
            raise ValueError("duplicate code") from exc
        except ForeignKeyViolation as exc:
            raise ValueError("unknown floor_id") from exc

    def get_by_id(self, zone_id: UUID) -> dict | None:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, floor_id, name, code, area, occupancy, created_at, updated_at
                FROM zones WHERE id = %s
                """,
                (zone_id,),
            )
            return cur.fetchone()

    def list(self, limit: int, offset: int, floor_id: UUID | None = None) -> tuple[list[dict], int]:
        with self._conn.cursor() as cur:
            if floor_id is not None:
                cur.execute("SELECT COUNT(*) AS count FROM zones WHERE floor_id = %s", (floor_id,))
                total = cur.fetchone()["count"]
                cur.execute(
                    """
                    SELECT id, floor_id, name, code, area, occupancy, created_at, updated_at
                    FROM zones WHERE floor_id = %s
                    ORDER BY created_at LIMIT %s OFFSET %s
                    """,
                    (floor_id, limit, offset),
                )
            else:
                cur.execute("SELECT COUNT(*) AS count FROM zones")
                total = cur.fetchone()["count"]
                cur.execute(
                    """
                    SELECT id, floor_id, name, code, area, occupancy, created_at, updated_at
                    FROM zones ORDER BY created_at LIMIT %s OFFSET %s
                    """,
                    (limit, offset),
                )
            return cur.fetchall(), total

    def update(self, zone_id: UUID, name: str, code: str, area: float, occupancy: int) -> dict | None:
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE zones
                    SET name = %s, code = %s, area = %s, occupancy = %s, updated_at = now()
                    WHERE id = %s
                    RETURNING id, floor_id, name, code, area, occupancy, created_at, updated_at
                    """,
                    (name, code, area, occupancy, zone_id),
                )
                return cur.fetchone()
        except UniqueViolation as exc:
            raise ValueError("duplicate code") from exc

    def delete(self, zone_id: UUID) -> bool:
        with self._conn.cursor() as cur:
            cur.execute("DELETE FROM zones WHERE id = %s", (zone_id,))
            return cur.rowcount > 0

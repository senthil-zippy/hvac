from uuid import UUID

from psycopg import Connection
from psycopg.errors import ForeignKeyViolation, UniqueViolation


class FloorRepository:
    def __init__(self, conn: Connection):
        self._conn = conn

    def insert(self, building_id: UUID, name: str, code: str) -> dict:
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO floors (building_id, name, code)
                    VALUES (%s, %s, %s)
                    RETURNING id, building_id, name, code, created_at, updated_at
                    """,
                    (building_id, name, code),
                )
                return cur.fetchone()
        except UniqueViolation as exc:
            raise ValueError("duplicate code") from exc
        except ForeignKeyViolation as exc:
            raise ValueError("unknown building_id") from exc

    def get_by_id(self, floor_id: UUID) -> dict | None:
        with self._conn.cursor() as cur:
            cur.execute(
                "SELECT id, building_id, name, code, created_at, updated_at FROM floors WHERE id = %s",
                (floor_id,),
            )
            return cur.fetchone()

    def list(self, limit: int, offset: int, building_id: UUID | None = None) -> tuple[list[dict], int]:
        with self._conn.cursor() as cur:
            if building_id is not None:
                cur.execute("SELECT COUNT(*) AS count FROM floors WHERE building_id = %s", (building_id,))
                total = cur.fetchone()["count"]
                cur.execute(
                    """
                    SELECT id, building_id, name, code, created_at, updated_at
                    FROM floors WHERE building_id = %s
                    ORDER BY created_at LIMIT %s OFFSET %s
                    """,
                    (building_id, limit, offset),
                )
            else:
                cur.execute("SELECT COUNT(*) AS count FROM floors")
                total = cur.fetchone()["count"]
                cur.execute(
                    """
                    SELECT id, building_id, name, code, created_at, updated_at
                    FROM floors ORDER BY created_at LIMIT %s OFFSET %s
                    """,
                    (limit, offset),
                )
            return cur.fetchall(), total

    def update(self, floor_id: UUID, name: str, code: str) -> dict | None:
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE floors
                    SET name = %s, code = %s, updated_at = now()
                    WHERE id = %s
                    RETURNING id, building_id, name, code, created_at, updated_at
                    """,
                    (name, code, floor_id),
                )
                return cur.fetchone()
        except UniqueViolation as exc:
            raise ValueError("duplicate code") from exc

    def delete(self, floor_id: UUID) -> bool:
        with self._conn.cursor() as cur:
            cur.execute("DELETE FROM floors WHERE id = %s", (floor_id,))
            return cur.rowcount > 0

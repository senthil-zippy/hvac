from uuid import UUID

from psycopg import Connection
from psycopg.errors import ForeignKeyViolation, UniqueViolation


class BuildingRepository:
    def __init__(self, conn: Connection):
        self._conn = conn

    def insert(self, portfolio_id: UUID, name: str, code: str, address: str) -> dict:
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO buildings (portfolio_id, name, code, address)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, portfolio_id, name, code, address, created_at, updated_at
                    """,
                    (portfolio_id, name, code, address),
                )
                return cur.fetchone()
        except UniqueViolation as exc:
            raise ValueError("duplicate code") from exc
        except ForeignKeyViolation as exc:
            raise ValueError("unknown portfolio_id") from exc

    def get_by_id(self, building_id: UUID) -> dict | None:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, portfolio_id, name, code, address, created_at, updated_at
                FROM buildings WHERE id = %s
                """,
                (building_id,),
            )
            return cur.fetchone()

    def list(self, limit: int, offset: int, portfolio_id: UUID | None = None) -> tuple[list[dict], int]:
        with self._conn.cursor() as cur:
            if portfolio_id is not None:
                cur.execute("SELECT COUNT(*) AS count FROM buildings WHERE portfolio_id = %s", (portfolio_id,))
                total = cur.fetchone()["count"]
                cur.execute(
                    """
                    SELECT id, portfolio_id, name, code, address, created_at, updated_at
                    FROM buildings WHERE portfolio_id = %s
                    ORDER BY created_at LIMIT %s OFFSET %s
                    """,
                    (portfolio_id, limit, offset),
                )
            else:
                cur.execute("SELECT COUNT(*) AS count FROM buildings")
                total = cur.fetchone()["count"]
                cur.execute(
                    """
                    SELECT id, portfolio_id, name, code, address, created_at, updated_at
                    FROM buildings ORDER BY created_at LIMIT %s OFFSET %s
                    """,
                    (limit, offset),
                )
            return cur.fetchall(), total

    def update(self, building_id: UUID, name: str, code: str, address: str) -> dict | None:
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE buildings
                    SET name = %s, code = %s, address = %s, updated_at = now()
                    WHERE id = %s
                    RETURNING id, portfolio_id, name, code, address, created_at, updated_at
                    """,
                    (name, code, address, building_id),
                )
                return cur.fetchone()
        except UniqueViolation as exc:
            raise ValueError("duplicate code") from exc

    def delete(self, building_id: UUID) -> bool:
        with self._conn.cursor() as cur:
            cur.execute("DELETE FROM buildings WHERE id = %s", (building_id,))
            return cur.rowcount > 0

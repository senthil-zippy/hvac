from uuid import UUID

from psycopg import Connection
from psycopg.errors import UniqueViolation


class PortfolioRepository:
    def __init__(self, conn: Connection):
        self._conn = conn

    def insert(self, name: str, code: str) -> dict:
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO portfolios (name, code)
                    VALUES (%s, %s)
                    RETURNING id, name, code, created_at, updated_at
                    """,
                    (name, code),
                )
                return cur.fetchone()
        except UniqueViolation as exc:
            raise ValueError("duplicate code") from exc

    def get_by_id(self, portfolio_id: UUID) -> dict | None:
        with self._conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, code, created_at, updated_at FROM portfolios WHERE id = %s",
                (portfolio_id,),
            )
            return cur.fetchone()

    def list(self, limit: int, offset: int) -> tuple[list[dict], int]:
        with self._conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS count FROM portfolios")
            total = cur.fetchone()["count"]
            cur.execute(
                """
                SELECT id, name, code, created_at, updated_at
                FROM portfolios
                ORDER BY created_at
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            return cur.fetchall(), total

    def update(self, portfolio_id: UUID, name: str, code: str) -> dict | None:
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE portfolios
                    SET name = %s, code = %s, updated_at = now()
                    WHERE id = %s
                    RETURNING id, name, code, created_at, updated_at
                    """,
                    (name, code, portfolio_id),
                )
                return cur.fetchone()
        except UniqueViolation as exc:
            raise ValueError("duplicate code") from exc

    def delete(self, portfolio_id: UUID) -> bool:
        with self._conn.cursor() as cur:
            cur.execute("DELETE FROM portfolios WHERE id = %s", (portfolio_id,))
            return cur.rowcount > 0

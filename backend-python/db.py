from collections.abc import Iterator
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from config import settings


@contextmanager
def get_connection() -> Iterator[psycopg.Connection]:
    """Yield a database connection using the configured DATABASE_URL."""
    conn = psycopg.connect(settings.database_url, row_factory=dict_row, autocommit=True)
    try:
        yield conn
    finally:
        conn.close()

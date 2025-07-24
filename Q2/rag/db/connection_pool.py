import sqlite3
from contextlib import contextmanager
from rag.config import DB_PATHS

@contextmanager
def get_connection(source: str):
    try:
        conn = sqlite3.connect(DB_PATHS[source])
        yield conn
    finally:
        conn.close()

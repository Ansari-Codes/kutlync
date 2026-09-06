from __future__ import annotations

import os
import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path
from threading import RLock
from typing import Any, Iterable

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", "data/app.db"))
if not DATABASE_PATH.is_absolute():
    DATABASE_PATH = BASE_DIR / DATABASE_PATH
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)


class Database:
    """Small shared SQLite interface used by all table models."""

    def __init__(self, path: Path):
        self._connection = sqlite3.connect(path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA journal_mode = WAL")
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._lock = RLock()

    def execute(
        self,
        query: str,
        parameters: Iterable[Any] = (),
        *,
        fetch: str | None = None,
        commit: bool = False,
    ) -> Any:
        with self._lock:
            cursor = self._connection.execute(query, tuple(parameters))
            if commit:
                self._connection.commit()
            if fetch == "one":
                row = cursor.fetchone()
                return dict(row) if row else None
            if fetch == "all":
                return [dict(row) for row in cursor.fetchall()]
            return {"lastrowid": cursor.lastrowid, "rowcount": cursor.rowcount}

    def executescript(self, script: str) -> None:
        with self._lock:
            self._connection.executescript(script)
            self._connection.commit()

    def close(self) -> None:
        with self._lock:
            self._connection.close()


SQL = Database(DATABASE_PATH)


class ModelABC(ABC):
    def __init__(self, table: str):
        self._table = table

    @abstractmethod
    async def select(self, columns: str = "*", where: dict[str, Any] | None = None,
                     limit: int = -1) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def insert(self, values: dict[str, Any]) -> int: ...

    @abstractmethod
    async def update(self, values: dict[str, Any], where: dict[str, Any]) -> int: ...

    @abstractmethod
    async def delete(self, where: dict[str, Any]) -> int: ...


def _where_clause(where: dict[str, Any] | None) -> tuple[str, list[Any]]:
    if not where:
        return "", []
    clauses = [f"{column} = ?" for column in where]
    return " WHERE " + " AND ".join(clauses), list(where.values())


class TableModel(ModelABC):
    async def select(self, columns: str = "*", where: dict[str, Any] | None = None,
                     limit: int = -1) -> list[dict[str, Any]]:
        clause, parameters = _where_clause(where)
        suffix = f" LIMIT {int(limit)}" if limit >= 0 else ""
        return SQL.execute(f"SELECT {columns} FROM {self._table}{clause}{suffix}", parameters, fetch="all")

    async def insert(self, values: dict[str, Any]) -> int:
        columns = ", ".join(values)
        placeholders = ", ".join("?" for _ in values)
        result = SQL.execute(
            f"INSERT INTO {self._table} ({columns}) VALUES ({placeholders})",
            values.values(),
            commit=True,
        )
        return int(result["lastrowid"])

    async def update(self, values: dict[str, Any], where: dict[str, Any]) -> int:
        clause, parameters = _where_clause(where)
        assignments = ", ".join(f"{column} = ?" for column in values)
        result = SQL.execute(
            f"UPDATE {self._table} SET {assignments}{clause}",
            [*values.values(), *parameters],
            commit=True,
        )
        return int(result["rowcount"])

    async def delete(self, where: dict[str, Any]) -> int:
        clause, parameters = _where_clause(where)
        result = SQL.execute(f"DELETE FROM {self._table}{clause}", parameters, commit=True)
        return int(result["rowcount"])


def DefineTable() -> None:
    SQL.executescript(
        """
        CREATE TABLE IF NOT EXISTS authenticated (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES authenticated(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            link_name TEXT NOT NULL,
            link_description TEXT NOT NULL DEFAULT '',
            destination_link TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            visits INTEGER NOT NULL DEFAULT 0,
            max_age_minutes INTEGER,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'deleted', 'expired')),
            access_code_hash TEXT,
            FOREIGN KEY (user_id) REFERENCES authenticated(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_links_user_id ON links(user_id);
        CREATE INDEX IF NOT EXISTS idx_links_slug ON links(slug);
        """
    )


initialize_database = DefineTable

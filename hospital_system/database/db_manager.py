"""
DatabaseManager Module
======================
Encapsulates all SQLite database operations behind a clean interface.
Demonstrates Abstraction by hiding SQL complexity from all other classes.
"""

import sqlite3
import os
from typing import Any, Optional


class DatabaseManager:
    """
    Centralized database access layer for the Hospital Management System.

    All database interactions across the entire application MUST go through
    this class. No raw sqlite3 calls should exist outside of this module.

    Attributes:
        __db_path (str): Path to the SQLite database file.
        __connection (sqlite3.Connection | None): Active database connection.
        __cursor (sqlite3.Cursor | None): Active database cursor.
    """

    # ── SQL for table creation ─────────────────────────────────────────
    _CREATE_TABLES_SQL: list[str] = [
        """
        CREATE TABLE IF NOT EXISTS patients (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            age         INTEGER NOT NULL,
            gender      TEXT    NOT NULL,
            contact     TEXT    NOT NULL,
            blood_group TEXT    NOT NULL,
            history     TEXT    DEFAULT ''
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS doctors (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT    NOT NULL,
            age             INTEGER NOT NULL,
            gender          TEXT    NOT NULL,
            contact         TEXT    NOT NULL,
            specialization  TEXT    NOT NULL,
            available_days  TEXT    NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS nurses (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            age           INTEGER NOT NULL,
            gender        TEXT    NOT NULL,
            contact       TEXT    NOT NULL,
            assigned_ward TEXT    DEFAULT ''
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS appointments (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id  INTEGER NOT NULL,
            date       TEXT    NOT NULL,
            time       TEXT    NOT NULL,
            status     TEXT    NOT NULL DEFAULT 'Scheduled',
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id)  REFERENCES doctors(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS prescriptions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id  INTEGER NOT NULL,
            date       TEXT    NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id)  REFERENCES doctors(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS medicines (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            prescription_id INTEGER NOT NULL,
            name            TEXT    NOT NULL,
            dosage          TEXT    NOT NULL,
            frequency       TEXT    NOT NULL,
            duration        TEXT    NOT NULL,
            FOREIGN KEY (prescription_id) REFERENCES prescriptions(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS bills (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            total      REAL    NOT NULL DEFAULT 0.0,
            is_paid    INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS bill_items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id     INTEGER NOT NULL,
            description TEXT    NOT NULL,
            amount      REAL    NOT NULL,
            FOREIGN KEY (bill_id) REFERENCES bills(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS rooms (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            room_type   TEXT    NOT NULL,
            is_occupied INTEGER NOT NULL DEFAULT 0,
            patient_id  INTEGER DEFAULT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        );
        """,
    ]

    def __init__(self, db_path: str = "") -> None:
        """
        Initialize DatabaseManager with the path to the SQLite database.

        Args:
            db_path: Absolute or relative path to the .db file.
                     Defaults to ``hospital.db`` in the project root.
        """
        if not db_path:
            # Place hospital.db next to the hospital_system package
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, "hospital.db")

        self.__db_path: str = db_path
        self.__connection: Optional[sqlite3.Connection] = None
        self.__cursor: Optional[sqlite3.Cursor] = None

    # ── Connection lifecycle ───────────────────────────────────────────

    def connect(self) -> None:
        """Open a connection to the SQLite database and enable FK support."""
        try:
            self.__connection = sqlite3.connect(self.__db_path)
            self.__connection.execute("PRAGMA foreign_keys = ON;")
            self.__cursor = self.__connection.cursor()
        except sqlite3.Error as exc:
            raise RuntimeError(
                f"Failed to connect to database at '{self.__db_path}': {exc}"
            ) from exc

    def close(self) -> None:
        """Commit pending changes and close the database connection."""
        if self.__connection:
            try:
                self.__connection.commit()
                self.__connection.close()
            except sqlite3.Error as exc:
                raise RuntimeError(f"Error closing database: {exc}") from exc
            finally:
                self.__connection = None
                self.__cursor = None

    # ── Core query helpers ─────────────────────────────────────────────

    def execute_query(
        self, query: str, params: tuple[Any, ...] = ()
    ) -> Optional[sqlite3.Cursor]:
        """
        Execute a write query (INSERT / UPDATE / DELETE) with parameters.

        Args:
            query:  SQL statement with ``?`` placeholders.
            params: Tuple of values matching the placeholders.

        Returns:
            The cursor after execution, or ``None`` on failure.
        """
        try:
            if self.__cursor is None:
                self.connect()
            assert self.__cursor is not None
            self.__cursor.execute(query, params)
            assert self.__connection is not None
            self.__connection.commit()
            return self.__cursor
        except sqlite3.Error as exc:
            print(f"\n  [ERROR]  Database error: {exc}")
            return None

    def fetch_one(
        self, query: str, params: tuple[Any, ...] = ()
    ) -> Optional[tuple[Any, ...]]:
        """
        Execute a SELECT and return a single row.

        Args:
            query:  SQL SELECT statement with ``?`` placeholders.
            params: Tuple of values matching the placeholders.

        Returns:
            A single row as a tuple, or ``None`` if no match.
        """
        try:
            if self.__cursor is None:
                self.connect()
            assert self.__cursor is not None
            self.__cursor.execute(query, params)
            return self.__cursor.fetchone()
        except sqlite3.Error as exc:
            print(f"\n  [ERROR]  Database error: {exc}")
            return None

    def fetch_all(
        self, query: str, params: tuple[Any, ...] = ()
    ) -> list[tuple[Any, ...]]:
        """
        Execute a SELECT and return all matching rows.

        Args:
            query:  SQL SELECT statement with ``?`` placeholders.
            params: Tuple of values matching the placeholders.

        Returns:
            List of rows (tuples). Empty list on error or no results.
        """
        try:
            if self.__cursor is None:
                self.connect()
            assert self.__cursor is not None
            self.__cursor.execute(query, params)
            return self.__cursor.fetchall()
        except sqlite3.Error as exc:
            print(f"\n  [ERROR]  Database error: {exc}")
            return []

    def get_last_row_id(self) -> int:
        """Return the rowid of the last INSERT operation."""
        if self.__cursor is not None:
            return self.__cursor.lastrowid or 0
        return 0

    # ── Schema initialisation ─────────────────────────────────────────

    def initialize_tables(self) -> None:
        """Create all required tables if they do not already exist."""
        try:
            if self.__cursor is None:
                self.connect()
            assert self.__cursor is not None and self.__connection is not None
            for ddl in self._CREATE_TABLES_SQL:
                self.__cursor.execute(ddl)
            self.__connection.commit()
            print("  [OK]  Database tables verified / created.")
        except sqlite3.Error as exc:
            raise RuntimeError(f"Failed to initialize tables: {exc}") from exc

    # ── Context-manager support (optional convenience) ─────────────────

    def __enter__(self) -> "DatabaseManager":
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

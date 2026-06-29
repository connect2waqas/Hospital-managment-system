"""
Room Module
===========
Manages hospital rooms — assignment, discharge, and occupancy.
"""

from typing import Optional
from hospital_system.database.db_manager import DatabaseManager


class Room:
    """Represents a hospital room that can be assigned to a patient."""

    def __init__(self, room_type: str, room_id: Optional[int] = None,
                 is_occupied: bool = False, assigned_patient_id: Optional[int] = None) -> None:
        self.__room_id: Optional[int] = room_id
        self.__room_type: str = room_type.strip()
        self.__is_occupied: bool = is_occupied
        self.__assigned_patient_id: Optional[int] = assigned_patient_id

    @property
    def room_id(self) -> Optional[int]: return self.__room_id
    @property
    def room_type(self) -> str: return self.__room_type
    @property
    def is_occupied(self) -> bool: return self.__is_occupied
    @property
    def assigned_patient_id(self) -> Optional[int]: return self.__assigned_patient_id

    def assign_patient(self, patient_id: int) -> None:
        """Assign a patient to this room."""
        if self.__is_occupied:
            raise ValueError(f"Room {self.__room_id} is already occupied.")
        self.__assigned_patient_id = patient_id
        self.__is_occupied = True

    def discharge_patient(self) -> None:
        """Discharge the patient from this room."""
        self.__assigned_patient_id = None
        self.__is_occupied = False

    def display(self) -> str:
        """Return a formatted room summary."""
        patient_str = str(self.__assigned_patient_id) if self.__assigned_patient_id else "None"
        return (f"  ── Room (ID: {self.__room_id or 'N/A'}) ──\n"
                f"  Type       : {self.__room_type}\n"
                f"  Occupied   : {'Yes' if self.__is_occupied else 'No'}\n"
                f"  Patient ID : {patient_str}")

    def save(self, db: DatabaseManager) -> None:
        cursor = db.execute_query(
            "INSERT INTO rooms (room_type, is_occupied, patient_id) VALUES (?, ?, ?);",
            (self.__room_type, int(self.__is_occupied), self.__assigned_patient_id))
        if cursor: self.__room_id = db.get_last_row_id()

    def update(self, db: DatabaseManager) -> None:
        db.execute_query(
            "UPDATE rooms SET room_type=?, is_occupied=?, patient_id=? WHERE id=?;",
            (self.__room_type, int(self.__is_occupied), self.__assigned_patient_id, self.__room_id))

    @staticmethod
    def get_by_id(db: DatabaseManager, rid: int) -> Optional["Room"]:
        row = db.fetch_one("SELECT * FROM rooms WHERE id=?;", (rid,))
        return Room._from_row(row) if row else None

    @staticmethod
    def get_all(db: DatabaseManager) -> list["Room"]:
        return [Room._from_row(r) for r in db.fetch_all("SELECT * FROM rooms;")]

    @staticmethod
    def get_available(db: DatabaseManager) -> list["Room"]:
        return [Room._from_row(r) for r in db.fetch_all("SELECT * FROM rooms WHERE is_occupied=0;")]

    @staticmethod
    def delete(db: DatabaseManager, rid: int) -> bool:
        return db.execute_query("DELETE FROM rooms WHERE id=?;", (rid,)) is not None

    @staticmethod
    def _from_row(row: tuple) -> "Room":
        rid, rtype, occupied, pid = row
        return Room(room_type=rtype, room_id=rid, is_occupied=bool(occupied), assigned_patient_id=pid)

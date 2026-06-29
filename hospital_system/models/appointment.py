"""
Appointment Module
==================
Standalone class managing patient-doctor appointments.
"""

from typing import Optional
from hospital_system.database.db_manager import DatabaseManager

VALID_STATUSES: tuple[str, ...] = ("Scheduled", "Confirmed", "Cancelled", "Completed")


class Appointment:
    """Represents an appointment between a patient and a doctor."""

    def __init__(self, patient_id: int, doctor_id: int, date: str, time: str,
                 status: str = "Scheduled", appointment_id: Optional[int] = None) -> None:
        self.__appointment_id: Optional[int] = appointment_id
        self.__patient_id: int = patient_id
        self.__doctor_id: int = doctor_id
        self.__date: str = date
        self.__time: str = time
        self.__status: str = status

    @property
    def appointment_id(self) -> Optional[int]: return self.__appointment_id
    @property
    def patient_id(self) -> int: return self.__patient_id
    @property
    def doctor_id(self) -> int: return self.__doctor_id
    @property
    def date(self) -> str: return self.__date
    @date.setter
    def date(self, v: str) -> None: self.__date = v
    @property
    def time(self) -> str: return self.__time
    @time.setter
    def time(self, v: str) -> None: self.__time = v
    @property
    def status(self) -> str: return self.__status
    @status.setter
    def status(self, v: str) -> None:
        if v not in VALID_STATUSES: raise ValueError(f"Status must be one of {VALID_STATUSES}.")
        self.__status = v

    def confirm(self) -> None: self.__status = "Confirmed"
    def cancel(self) -> None: self.__status = "Cancelled"

    def reschedule(self, new_date: str, new_time: str = "") -> None:
        self.__date = new_date
        if new_time: self.__time = new_time
        self.__status = "Scheduled"

    def display(self) -> str:
        return (f"  ── Appointment (ID: {self.__appointment_id or 'N/A'}) ──\n"
                f"  Patient ID : {self.__patient_id}\n"
                f"  Doctor ID  : {self.__doctor_id}\n"
                f"  Date       : {self.__date}\n"
                f"  Time       : {self.__time}\n"
                f"  Status     : {self.__status}")

    def save(self, db: DatabaseManager) -> None:
        cursor = db.execute_query(
            "INSERT INTO appointments (patient_id, doctor_id, date, time, status) VALUES (?, ?, ?, ?, ?);",
            (self.__patient_id, self.__doctor_id, self.__date, self.__time, self.__status))
        if cursor: self.__appointment_id = db.get_last_row_id()

    def update(self, db: DatabaseManager) -> None:
        db.execute_query(
            "UPDATE appointments SET patient_id=?, doctor_id=?, date=?, time=?, status=? WHERE id=?;",
            (self.__patient_id, self.__doctor_id, self.__date, self.__time, self.__status, self.__appointment_id))

    @staticmethod
    def delete(db: DatabaseManager, aid: int) -> bool:
        return db.execute_query("DELETE FROM appointments WHERE id=?;", (aid,)) is not None

    @staticmethod
    def get_by_id(db: DatabaseManager, aid: int) -> Optional["Appointment"]:
        row = db.fetch_one("SELECT * FROM appointments WHERE id=?;", (aid,))
        return Appointment._from_row(row) if row else None

    @staticmethod
    def get_all(db: DatabaseManager) -> list["Appointment"]:
        return [Appointment._from_row(r) for r in db.fetch_all("SELECT * FROM appointments;")]

    @staticmethod
    def get_by_patient(db: DatabaseManager, pid: int) -> list["Appointment"]:
        return [Appointment._from_row(r) for r in db.fetch_all("SELECT * FROM appointments WHERE patient_id=?;", (pid,))]

    @staticmethod
    def get_by_doctor(db: DatabaseManager, did: int) -> list["Appointment"]:
        return [Appointment._from_row(r) for r in db.fetch_all("SELECT * FROM appointments WHERE doctor_id=?;", (did,))]

    @staticmethod
    def _from_row(row: tuple) -> "Appointment":
        aid, pid, did, date, time, status = row
        return Appointment(patient_id=pid, doctor_id=did, date=date, time=time, status=status, appointment_id=aid)

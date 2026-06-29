"""
Doctor Module
=============
Concrete subclass of Person — demonstrates **Inheritance** and **Polymorphism**.
"""

from typing import Optional

from hospital_system.models.person import Person
from hospital_system.database.db_manager import DatabaseManager


# ── Constants ──────────────────────────────────────────────────────────
VALID_DAYS: tuple[str, ...] = (
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
)


class Doctor(Person):
    """
    Represents a doctor on the hospital staff.

    Inherits common attributes from Person and adds specialization
    and availability schedule.

    Attributes:
        __doctor_id      (int | None):  Database primary key.
        __specialization (str):         Medical specialization.
        __available_days (list[str]):   Days the doctor is available.
    """

    def __init__(
        self,
        name: str,
        age: int,
        gender: str,
        contact: str,
        specialization: str,
        available_days: Optional[list[str]] = None,
        doctor_id: Optional[int] = None,
    ) -> None:
        """
        Initialise a Doctor.

        Args:
            name:            Full name.
            age:             Age (0–120).
            gender:          'Male', 'Female', or 'Other'.
            contact:         11-digit contact number.
            specialization:  Medical specialization.
            available_days:  List of weekday names.
            doctor_id:       DB id (None until persisted).
        """
        super().__init__(name, age, gender, contact)
        self.specialization = specialization
        self.__doctor_id: Optional[int] = doctor_id
        self.__available_days: list[str] = []
        if available_days:
            for day in available_days:
                self._validate_day(day)
                self.__available_days.append(day.strip().title())

    # ── doctor_id ──────────────────────────────────────────────────────
    @property
    def doctor_id(self) -> Optional[int]:
        """Return the doctor's database ID."""
        return self.__doctor_id

    @doctor_id.setter
    def doctor_id(self, value: int) -> None:
        """Set the doctor's database ID."""
        self.__doctor_id = value

    # ── specialization ─────────────────────────────────────────────────
    @property
    def specialization(self) -> str:
        """Return the doctor's specialization."""
        return self.__specialization

    @specialization.setter
    def specialization(self, value: str) -> None:
        """Set specialization after validation."""
        if not value or not value.strip():
            raise ValueError("Specialization cannot be empty.")
        self.__specialization = value.strip().title()

    # ── available_days ─────────────────────────────────────────────────
    @property
    def available_days(self) -> list[str]:
        """Return a copy of the availability list."""
        return list(self.__available_days)

    @available_days.setter
    def available_days(self, days: list[str]) -> None:
        """Set the available days after validating each one."""
        validated: list[str] = []
        for day in days:
            self._validate_day(day)
            validated.append(day.strip().title())
        self.__available_days = validated

    # ── Methods ────────────────────────────────────────────────────────

    def get_specialization(self) -> str:
        """Return the doctor's specialization string."""
        return self.__specialization

    def is_available(self, day: str) -> bool:
        """
        Check whether the doctor is available on a given day.

        Args:
            day: Weekday name (e.g. 'Monday').

        Returns:
            True if the doctor works on that day.
        """
        return day.strip().title() in self.__available_days

    # ── Abstract implementations (Polymorphism) ───────────────────────

    def get_role(self) -> str:
        """Return 'Doctor'."""
        return "Doctor"

    def display_info(self) -> str:
        """Return a formatted summary of doctor details."""
        header = f"  ── Doctor (ID: {self.__doctor_id or 'N/A'}) ──"
        base = self._base_info()
        days_str = ", ".join(self.__available_days) if self.__available_days else "None"
        extra = (
            f"  Spec.   : {self.__specialization}\n"
            f"  Days    : {days_str}"
        )
        return f"{header}\n{base}\n{extra}"

    # ── Database CRUD ─────────────────────────────────────────────────

    def save(self, db: DatabaseManager) -> None:
        """Insert this doctor into the database."""
        days_str = "||".join(self.__available_days)
        cursor = db.execute_query(
            "INSERT INTO doctors (name, age, gender, contact, specialization, available_days) "
            "VALUES (?, ?, ?, ?, ?, ?);",
            (self.name, self.age, self.gender, self.contact,
             self.__specialization, days_str),
        )
        if cursor:
            self.__doctor_id = db.get_last_row_id()

    def update(self, db: DatabaseManager) -> None:
        """Update this doctor's record in the database."""
        days_str = "||".join(self.__available_days)
        db.execute_query(
            "UPDATE doctors SET name=?, age=?, gender=?, contact=?, "
            "specialization=?, available_days=? WHERE id=?;",
            (self.name, self.age, self.gender, self.contact,
             self.__specialization, days_str, self.__doctor_id),
        )

    @staticmethod
    def delete(db: DatabaseManager, doctor_id: int) -> bool:
        """Delete a doctor by ID. Returns True on success."""
        cursor = db.execute_query("DELETE FROM doctors WHERE id=?;", (doctor_id,))
        return cursor is not None

    @staticmethod
    def get_by_id(db: DatabaseManager, doctor_id: int) -> Optional["Doctor"]:
        """Load a doctor from the database by ID."""
        row = db.fetch_one("SELECT * FROM doctors WHERE id=?;", (doctor_id,))
        if row is None:
            return None
        return Doctor._from_row(row)

    @staticmethod
    def get_all(db: DatabaseManager) -> list["Doctor"]:
        """Load all doctors from the database."""
        rows = db.fetch_all("SELECT * FROM doctors;")
        return [Doctor._from_row(r) for r in rows]

    @staticmethod
    def search_by_specialization(db: DatabaseManager, spec: str) -> list["Doctor"]:
        """Search doctors whose specialization contains the given substring."""
        rows = db.fetch_all(
            "SELECT * FROM doctors WHERE specialization LIKE ?;", (f"%{spec}%",)
        )
        return [Doctor._from_row(r) for r in rows]

    @staticmethod
    def _from_row(row: tuple) -> "Doctor":
        """Construct a Doctor instance from a database row tuple."""
        did, name, age, gender, contact, spec, days_str = row
        days = [d for d in days_str.split("||") if d] if days_str else []
        return Doctor(
            name=name,
            age=age,
            gender=gender,
            contact=contact,
            specialization=spec,
            available_days=days,
            doctor_id=did,
        )

    # ── Private helpers ────────────────────────────────────────────────

    @staticmethod
    def _validate_day(day: str) -> None:
        """Raise ValueError if *day* is not a valid weekday name."""
        if day.strip().title() not in VALID_DAYS:
            raise ValueError(
                f"'{day}' is not a valid day. Choose from {VALID_DAYS}."
            )

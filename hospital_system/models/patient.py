"""
Patient Module
==============
Concrete subclass of Person — demonstrates **Inheritance** and **Polymorphism**.
"""

from typing import Optional

from hospital_system.models.person import Person
from hospital_system.database.db_manager import DatabaseManager


# ── Constants ──────────────────────────────────────────────────────────
VALID_BLOOD_GROUPS: tuple[str, ...] = (
    "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-",
)


class Patient(Person):
    """
    Represents a patient registered in the hospital.

    Inherits common attributes (name, age, gender, contact) from Person
    and adds patient-specific data.

    Attributes:
        __patient_id     (int | None): Database primary key.
        __blood_group    (str):        One of the valid ABO/Rh groups.
        __medical_history (list[str]): List of past medical notes.
    """

    def __init__(
        self,
        name: str,
        age: int,
        gender: str,
        contact: str,
        blood_group: str,
        patient_id: Optional[int] = None,
        medical_history: Optional[list[str]] = None,
    ) -> None:
        """
        Initialise a Patient.

        Args:
            name:            Full name.
            age:             Age (0–120).
            gender:          'Male', 'Female', or 'Other'.
            contact:         11-digit contact number.
            blood_group:     Valid ABO/Rh blood group.
            patient_id:      DB id (None until persisted).
            medical_history: Existing medical notes.
        """
        super().__init__(name, age, gender, contact)
        self.blood_group = blood_group
        self.__patient_id: Optional[int] = patient_id
        self.__medical_history: list[str] = medical_history if medical_history else []

    # ── patient_id ─────────────────────────────────────────────────────
    @property
    def patient_id(self) -> Optional[int]:
        """Return the patient's database ID."""
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value: int) -> None:
        """Set the patient's database ID."""
        self.__patient_id = value

    # ── blood_group ────────────────────────────────────────────────────
    @property
    def blood_group(self) -> str:
        """Return the patient's blood group."""
        return self.__blood_group

    @blood_group.setter
    def blood_group(self, value: str) -> None:
        """Set blood group after validation."""
        cleaned = value.strip().upper()
        if cleaned not in VALID_BLOOD_GROUPS:
            raise ValueError(
                f"Blood group must be one of {VALID_BLOOD_GROUPS}. Got '{value}'."
            )
        self.__blood_group = cleaned

    # ── medical_history ────────────────────────────────────────────────
    @property
    def medical_history(self) -> list[str]:
        """Return a copy of the medical history list."""
        return list(self.__medical_history)

    def add_medical_record(self, record: str) -> None:
        """
        Append a new record to the patient's medical history.

        Args:
            record: Description of the medical event / note.
        """
        if not record.strip():
            raise ValueError("Medical record cannot be empty.")
        self.__medical_history.append(record.strip())

    def get_history(self) -> str:
        """Return the full medical history as a formatted string."""
        if not self.__medical_history:
            return "  No medical history on record."
        lines = [f"  {i}. {entry}" for i, entry in enumerate(self.__medical_history, 1)]
        return "\n".join(lines)

    # ── Abstract implementations (Polymorphism) ───────────────────────

    def get_role(self) -> str:
        """Return 'Patient'."""
        return "Patient"

    def display_info(self) -> str:
        """Return a formatted summary of patient details."""
        header = f"  ── Patient (ID: {self.__patient_id or 'N/A'}) ──"
        base = self._base_info()
        extra = (
            f"  Blood Gr: {self.__blood_group}\n"
            f"  History :\n{self.get_history()}"
        )
        return f"{header}\n{base}\n{extra}"

    # ── Database CRUD (via DatabaseManager) ───────────────────────────

    def save(self, db: DatabaseManager) -> None:
        """Insert this patient into the database."""
        history_str = "||".join(self.__medical_history)
        cursor = db.execute_query(
            "INSERT INTO patients (name, age, gender, contact, blood_group, history) "
            "VALUES (?, ?, ?, ?, ?, ?);",
            (self.name, self.age, self.gender, self.contact, self.__blood_group, history_str),
        )
        if cursor:
            self.__patient_id = db.get_last_row_id()

    def update(self, db: DatabaseManager) -> None:
        """Update this patient's record in the database."""
        history_str = "||".join(self.__medical_history)
        db.execute_query(
            "UPDATE patients SET name=?, age=?, gender=?, contact=?, "
            "blood_group=?, history=? WHERE id=?;",
            (self.name, self.age, self.gender, self.contact,
             self.__blood_group, history_str, self.__patient_id),
        )

    @staticmethod
    def delete(db: DatabaseManager, patient_id: int) -> bool:
        """Delete a patient by ID. Returns True on success."""
        cursor = db.execute_query("DELETE FROM patients WHERE id=?;", (patient_id,))
        return cursor is not None

    @staticmethod
    def get_by_id(db: DatabaseManager, patient_id: int) -> Optional["Patient"]:
        """Load a patient from the database by their ID."""
        row = db.fetch_one("SELECT * FROM patients WHERE id=?;", (patient_id,))
        if row is None:
            return None
        return Patient._from_row(row)

    @staticmethod
    def get_all(db: DatabaseManager) -> list["Patient"]:
        """Load all patients from the database."""
        rows = db.fetch_all("SELECT * FROM patients;")
        return [Patient._from_row(r) for r in rows]

    @staticmethod
    def search_by_name(db: DatabaseManager, name: str) -> list["Patient"]:
        """Search patients whose name contains the given substring."""
        rows = db.fetch_all(
            "SELECT * FROM patients WHERE name LIKE ?;", (f"%{name}%",)
        )
        return [Patient._from_row(r) for r in rows]

    @staticmethod
    def _from_row(row: tuple) -> "Patient":
        """Construct a Patient instance from a database row tuple."""
        pid, name, age, gender, contact, blood_group, history_str = row
        history = [h for h in history_str.split("||") if h] if history_str else []
        return Patient(
            name=name,
            age=age,
            gender=gender,
            contact=contact,
            blood_group=blood_group,
            patient_id=pid,
            medical_history=history,
        )

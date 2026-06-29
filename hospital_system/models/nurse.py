"""
Nurse Module
============
Concrete subclass of Person — demonstrates **Inheritance** and **Polymorphism**.
"""

from typing import Optional

from hospital_system.models.person import Person
from hospital_system.database.db_manager import DatabaseManager


class Nurse(Person):
    """
    Represents a nurse on the hospital staff.

    Attributes:
        __nurse_id      (int | None): Database primary key.
        __assigned_ward (str):        Ward the nurse is currently assigned to.
    """

    def __init__(
        self,
        name: str,
        age: int,
        gender: str,
        contact: str,
        nurse_id: Optional[int] = None,
        assigned_ward: str = "",
    ) -> None:
        """
        Initialise a Nurse.

        Args:
            name:          Full name.
            age:           Age (0–120).
            gender:        'Male', 'Female', or 'Other'.
            contact:       11-digit contact number.
            nurse_id:      DB id (None until persisted).
            assigned_ward: Name of the assigned ward.
        """
        super().__init__(name, age, gender, contact)
        self.__nurse_id: Optional[int] = nurse_id
        self.__assigned_ward: str = assigned_ward.strip()

    # ── nurse_id ───────────────────────────────────────────────────────
    @property
    def nurse_id(self) -> Optional[int]:
        """Return the nurse's database ID."""
        return self.__nurse_id

    @nurse_id.setter
    def nurse_id(self, value: int) -> None:
        """Set the nurse's database ID."""
        self.__nurse_id = value

    # ── assigned_ward ──────────────────────────────────────────────────
    @property
    def assigned_ward(self) -> str:
        """Return the name of the assigned ward."""
        return self.__assigned_ward

    @assigned_ward.setter
    def assigned_ward(self, value: str) -> None:
        """Set the assigned ward name."""
        self.__assigned_ward = value.strip()

    def assign_ward(self, ward: str) -> None:
        """
        Assign (or reassign) the nurse to a specific ward.

        Args:
            ward: Ward name string.
        """
        if not ward.strip():
            raise ValueError("Ward name cannot be empty.")
        self.__assigned_ward = ward.strip()

    # ── Abstract implementations (Polymorphism) ───────────────────────

    def get_role(self) -> str:
        """Return 'Nurse'."""
        return "Nurse"

    def display_info(self) -> str:
        """Return a formatted summary of nurse details."""
        header = f"  ── Nurse (ID: {self.__nurse_id or 'N/A'}) ──"
        base = self._base_info()
        extra = f"  Ward    : {self.__assigned_ward or 'Unassigned'}"
        return f"{header}\n{base}\n{extra}"

    # ── Database CRUD ─────────────────────────────────────────────────

    def save(self, db: DatabaseManager) -> None:
        """Insert this nurse into the database."""
        cursor = db.execute_query(
            "INSERT INTO nurses (name, age, gender, contact, assigned_ward) "
            "VALUES (?, ?, ?, ?, ?);",
            (self.name, self.age, self.gender, self.contact, self.__assigned_ward),
        )
        if cursor:
            self.__nurse_id = db.get_last_row_id()

    def update(self, db: DatabaseManager) -> None:
        """Update this nurse's record in the database."""
        db.execute_query(
            "UPDATE nurses SET name=?, age=?, gender=?, contact=?, "
            "assigned_ward=? WHERE id=?;",
            (self.name, self.age, self.gender, self.contact,
             self.__assigned_ward, self.__nurse_id),
        )

    @staticmethod
    def delete(db: DatabaseManager, nurse_id: int) -> bool:
        """Delete a nurse by ID. Returns True on success."""
        cursor = db.execute_query("DELETE FROM nurses WHERE id=?;", (nurse_id,))
        return cursor is not None

    @staticmethod
    def get_by_id(db: DatabaseManager, nurse_id: int) -> Optional["Nurse"]:
        """Load a nurse from the database by ID."""
        row = db.fetch_one("SELECT * FROM nurses WHERE id=?;", (nurse_id,))
        if row is None:
            return None
        return Nurse._from_row(row)

    @staticmethod
    def get_all(db: DatabaseManager) -> list["Nurse"]:
        """Load all nurses from the database."""
        rows = db.fetch_all("SELECT * FROM nurses;")
        return [Nurse._from_row(r) for r in rows]

    @staticmethod
    def _from_row(row: tuple) -> "Nurse":
        """Construct a Nurse instance from a database row tuple."""
        nid, name, age, gender, contact, ward = row
        return Nurse(
            name=name,
            age=age,
            gender=gender,
            contact=contact,
            nurse_id=nid,
            assigned_ward=ward,
        )

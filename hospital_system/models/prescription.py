"""
Prescription & Medicine Module
==============================
Medicine is a simple value-object; Prescription aggregates medicines.
"""

from typing import Optional
from hospital_system.database.db_manager import DatabaseManager


class Medicine:
    """Represents a single medicine entry in a prescription."""

    def __init__(self, name: str, dosage: str, frequency: str, duration: str,
                 medicine_id: Optional[int] = None, prescription_id: Optional[int] = None) -> None:
        self.__medicine_id: Optional[int] = medicine_id
        self.__prescription_id: Optional[int] = prescription_id
        self.__name: str = name.strip()
        self.__dosage: str = dosage.strip()
        self.__frequency: str = frequency.strip()
        self.__duration: str = duration.strip()

    @property
    def medicine_id(self) -> Optional[int]: return self.__medicine_id
    @property
    def prescription_id(self) -> Optional[int]: return self.__prescription_id
    @prescription_id.setter
    def prescription_id(self, v: int) -> None: self.__prescription_id = v
    @property
    def name(self) -> str: return self.__name
    @property
    def dosage(self) -> str: return self.__dosage
    @property
    def frequency(self) -> str: return self.__frequency
    @property
    def duration(self) -> str: return self.__duration

    def describe(self) -> str:
        """Return a human-readable description of this medicine."""
        return (f"    {self.__name} | Dosage: {self.__dosage} | "
                f"Freq: {self.__frequency} | Duration: {self.__duration}")

    def save(self, db: DatabaseManager) -> None:
        cursor = db.execute_query(
            "INSERT INTO medicines (prescription_id, name, dosage, frequency, duration) VALUES (?, ?, ?, ?, ?);",
            (self.__prescription_id, self.__name, self.__dosage, self.__frequency, self.__duration))
        if cursor: self.__medicine_id = db.get_last_row_id()


class Prescription:
    """Represents a prescription issued by a doctor to a patient."""

    def __init__(self, patient_id: int, doctor_id: int, date: str,
                 prescription_id: Optional[int] = None,
                 medicines: Optional[list[Medicine]] = None) -> None:
        self.__prescription_id: Optional[int] = prescription_id
        self.__patient_id: int = patient_id
        self.__doctor_id: int = doctor_id
        self.__date: str = date
        self.__medicines: list[Medicine] = medicines if medicines else []

    @property
    def prescription_id(self) -> Optional[int]: return self.__prescription_id
    @property
    def patient_id(self) -> int: return self.__patient_id
    @property
    def doctor_id(self) -> int: return self.__doctor_id
    @property
    def date(self) -> str: return self.__date
    @property
    def medicines(self) -> list[Medicine]: return list(self.__medicines)

    def add_medicine(self, medicine: Medicine) -> None:
        """Add a medicine to this prescription."""
        self.__medicines.append(medicine)

    def display(self) -> str:
        """Return a formatted prescription summary."""
        lines = [
            f"  ── Prescription (ID: {self.__prescription_id or 'N/A'}) ──",
            f"  Patient ID : {self.__patient_id}",
            f"  Doctor ID  : {self.__doctor_id}",
            f"  Date       : {self.__date}",
            f"  Medicines  :",
        ]
        if self.__medicines:
            for m in self.__medicines:
                lines.append(m.describe())
        else:
            lines.append("    No medicines added.")
        return "\n".join(lines)

    def generate_summary(self) -> str:
        """Return a brief summary string for reports."""
        count = len(self.__medicines)
        return (f"Rx#{self.__prescription_id} | Patient#{self.__patient_id} | "
                f"Dr#{self.__doctor_id} | {self.__date} | {count} medicine(s)")

    def save(self, db: DatabaseManager) -> None:
        cursor = db.execute_query(
            "INSERT INTO prescriptions (patient_id, doctor_id, date) VALUES (?, ?, ?);",
            (self.__patient_id, self.__doctor_id, self.__date))
        if cursor:
            self.__prescription_id = db.get_last_row_id()
            for med in self.__medicines:
                med.prescription_id = self.__prescription_id
                med.save(db)

    @staticmethod
    def get_by_id(db: DatabaseManager, pid: int) -> Optional["Prescription"]:
        row = db.fetch_one("SELECT * FROM prescriptions WHERE id=?;", (pid,))
        if not row: return None
        rx = Prescription(patient_id=row[1], doctor_id=row[2], date=row[3], prescription_id=row[0])
        med_rows = db.fetch_all("SELECT * FROM medicines WHERE prescription_id=?;", (row[0],))
        for mr in med_rows:
            rx.add_medicine(Medicine(name=mr[2], dosage=mr[3], frequency=mr[4], duration=mr[5],
                                    medicine_id=mr[0], prescription_id=mr[1]))
        return rx

    @staticmethod
    def get_all(db: DatabaseManager) -> list["Prescription"]:
        rows = db.fetch_all("SELECT * FROM prescriptions;")
        result: list[Prescription] = []
        for row in rows:
            rx = Prescription(patient_id=row[1], doctor_id=row[2], date=row[3], prescription_id=row[0])
            med_rows = db.fetch_all("SELECT * FROM medicines WHERE prescription_id=?;", (row[0],))
            for mr in med_rows:
                rx.add_medicine(Medicine(name=mr[2], dosage=mr[3], frequency=mr[4], duration=mr[5],
                                        medicine_id=mr[0], prescription_id=mr[1]))
            result.append(rx)
        return result

    @staticmethod
    def get_by_patient(db: DatabaseManager, patient_id: int) -> list["Prescription"]:
        rows = db.fetch_all("SELECT * FROM prescriptions WHERE patient_id=?;", (patient_id,))
        result: list[Prescription] = []
        for row in rows:
            rx = Prescription(patient_id=row[1], doctor_id=row[2], date=row[3], prescription_id=row[0])
            med_rows = db.fetch_all("SELECT * FROM medicines WHERE prescription_id=?;", (row[0],))
            for mr in med_rows:
                rx.add_medicine(Medicine(name=mr[2], dosage=mr[3], frequency=mr[4], duration=mr[5],
                                        medicine_id=mr[0], prescription_id=mr[1]))
            result.append(rx)
        return result

    @staticmethod
    def delete(db: DatabaseManager, rx_id: int) -> bool:
        db.execute_query("DELETE FROM medicines WHERE prescription_id=?;", (rx_id,))
        return db.execute_query("DELETE FROM prescriptions WHERE id=?;", (rx_id,)) is not None

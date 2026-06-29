"""
Bill Module
===========
Manages billing, line items, and payment status.
"""

from typing import Optional
from hospital_system.database.db_manager import DatabaseManager


class Bill:
    """Represents a bill for a patient with itemised charges."""

    def __init__(self, patient_id: int, bill_id: Optional[int] = None,
                 items: Optional[list[tuple[str, float]]] = None,
                 total: float = 0.0, is_paid: bool = False) -> None:
        self.__bill_id: Optional[int] = bill_id
        self.__patient_id: int = patient_id
        self.__items: list[tuple[str, float]] = items if items else []
        self.__total: float = total
        self.__is_paid: bool = is_paid

    @property
    def bill_id(self) -> Optional[int]: return self.__bill_id
    @property
    def patient_id(self) -> int: return self.__patient_id
    @property
    def items(self) -> list[tuple[str, float]]: return list(self.__items)
    @property
    def total(self) -> float: return self.__total
    @property
    def is_paid(self) -> bool: return self.__is_paid

    def add_item(self, description: str, amount: float) -> None:
        """Add a line item to the bill."""
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        self.__items.append((description.strip(), amount))

    def calculate_total(self) -> float:
        """Recalculate the total from all items."""
        self.__total = sum(amt for _, amt in self.__items)
        return self.__total

    def mark_paid(self) -> None:
        """Mark the bill as paid."""
        self.__is_paid = True

    def display(self) -> str:
        """Return a formatted bill summary."""
        lines = [
            f"  ── Bill (ID: {self.__bill_id or 'N/A'}) ──",
            f"  Patient ID : {self.__patient_id}",
            f"  Items      :",
        ]
        if self.__items:
            for desc, amt in self.__items:
                lines.append(f"    • {desc:<30} Rs. {amt:>10.2f}")
        else:
            lines.append("    No items.")
        lines.append(f"  {'─' * 48}")
        lines.append(f"  Total      : Rs. {self.__total:>10.2f}")
        lines.append(f"  Paid       : {'Yes' if self.__is_paid else 'No'}")
        return "\n".join(lines)

    def save(self, db: DatabaseManager) -> None:
        """Insert bill and all its items into the database."""
        self.calculate_total()
        cursor = db.execute_query(
            "INSERT INTO bills (patient_id, total, is_paid) VALUES (?, ?, ?);",
            (self.__patient_id, self.__total, int(self.__is_paid)))
        if cursor:
            self.__bill_id = db.get_last_row_id()
            for desc, amt in self.__items:
                db.execute_query(
                    "INSERT INTO bill_items (bill_id, description, amount) VALUES (?, ?, ?);",
                    (self.__bill_id, desc, amt))

    def update(self, db: DatabaseManager) -> None:
        """Update bill total and payment status in the database."""
        self.calculate_total()
        db.execute_query(
            "UPDATE bills SET total=?, is_paid=? WHERE id=?;",
            (self.__total, int(self.__is_paid), self.__bill_id))

    @staticmethod
    def get_by_id(db: DatabaseManager, bid: int) -> Optional["Bill"]:
        row = db.fetch_one("SELECT * FROM bills WHERE id=?;", (bid,))
        if not row: return None
        items_rows = db.fetch_all("SELECT description, amount FROM bill_items WHERE bill_id=?;", (row[0],))
        items = [(r[0], r[1]) for r in items_rows]
        return Bill(patient_id=row[1], bill_id=row[0], items=items, total=row[2], is_paid=bool(row[3]))

    @staticmethod
    def get_all(db: DatabaseManager) -> list["Bill"]:
        rows = db.fetch_all("SELECT * FROM bills;")
        result: list[Bill] = []
        for row in rows:
            items_rows = db.fetch_all("SELECT description, amount FROM bill_items WHERE bill_id=?;", (row[0],))
            items = [(r[0], r[1]) for r in items_rows]
            result.append(Bill(patient_id=row[1], bill_id=row[0], items=items, total=row[2], is_paid=bool(row[3])))
        return result

    @staticmethod
    def get_by_patient(db: DatabaseManager, pid: int) -> list["Bill"]:
        rows = db.fetch_all("SELECT * FROM bills WHERE patient_id=?;", (pid,))
        result: list[Bill] = []
        for row in rows:
            items_rows = db.fetch_all("SELECT description, amount FROM bill_items WHERE bill_id=?;", (row[0],))
            items = [(r[0], r[1]) for r in items_rows]
            result.append(Bill(patient_id=row[1], bill_id=row[0], items=items, total=row[2], is_paid=bool(row[3])))
        return result

    @staticmethod
    def delete(db: DatabaseManager, bid: int) -> bool:
        db.execute_query("DELETE FROM bill_items WHERE bill_id=?;", (bid,))
        return db.execute_query("DELETE FROM bills WHERE id=?;", (bid,)) is not None

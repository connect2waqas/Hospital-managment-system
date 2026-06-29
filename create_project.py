#!/usr/bin/env python3
"""
Project Generator for Hospital Management System
Creates all files and directories needed to run the system.
Run this script to set up the project.
"""

import os
import sys

PROJECT_ROOT = "hospital_system"

files = {
    "hospital_system/__init__.py": '''"""Hospital Management System - A comprehensive OOP-based system with SQLite backend."""''',

    "hospital_system/main.py": '''
"""
Hospital Management System — Entry Point
=========================================
Initialises the database, creates the Hospital controller,
and launches the interactive console menu.
"""

import sys
import os

# Ensure the project root is on sys.path so imports work when run directly.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hospital_system.database.db_manager import DatabaseManager
from hospital_system.controllers.hospital import Hospital
from hospital_system.ui.menu import main_menu


HOSPITAL_NAME: str = "City General Hospital"


def main() -> None:
    """Application entry point."""
    db = DatabaseManager()
    try:
        db.connect()
        db.initialize_tables()

        hospital = Hospital(name=HOSPITAL_NAME, db=db)
        main_menu(hospital)

    except RuntimeError as exc:
        print(f"\\n  ✖  Fatal error: {exc}")
    except KeyboardInterrupt:
        print("\\n\\n  Session interrupted. Goodbye!")
    finally:
        db.close()


if __name__ == "__main__":
    main()
''',

    "hospital_system/controllers/__init__.py": '''"""Controllers package for Hospital Management System."""''',

    "hospital_system/controllers/hospital.py": '''
"""
Hospital Controller
===================
Main controller class that orchestrates all hospital operations.
Acts as the central façade — like a GameEngine for the hospital domain.
Demonstrates Polymorphism by calling display_info() on any Person subtype.
"""

from typing import Optional

from hospital_system.database.db_manager import DatabaseManager
from hospital_system.models.patient import Patient
from hospital_system.models.doctor import Doctor
from hospital_system.models.nurse import Nurse
from hospital_system.models.appointment import Appointment
from hospital_system.models.prescription import Prescription, Medicine
from hospital_system.models.bill import Bill
from hospital_system.models.room import Room
from hospital_system.models.person import Person


class Hospital:
    """
    Central controller for the Hospital Management System.

    Coordinates all domain objects and database operations through
    the shared DatabaseManager instance.
    """

    def __init__(self, name: str, db: DatabaseManager) -> None:
        self.__name: str = name
        self.__db: DatabaseManager = db

    @property
    def name(self) -> str:
        """Return the hospital name."""
        return self.__name

    # ══════════════════════════════════════════════════════════════════
    #  PATIENT MANAGEMENT
    # ══════════════════════════════════════════════════════════════════

    def add_patient(self, name: str, age: int, gender: str,
                    contact: str, blood_group: str) -> Patient:
        """Register a new patient and persist to database."""
        patient = Patient(name=name, age=age, gender=gender,
                          contact=contact, blood_group=blood_group)
        patient.save(self.__db)
        return patient

    def get_patient(self, patient_id: int) -> Optional[Patient]:
        """Retrieve a patient by ID."""
        return Patient.get_by_id(self.__db, patient_id)

    def get_all_patients(self) -> list[Patient]:
        """Retrieve all patients."""
        return Patient.get_all(self.__db)

    def update_patient(self, patient: Patient) -> None:
        """Update an existing patient record."""
        patient.update(self.__db)

    def delete_patient(self, patient_id: int) -> bool:
        """Delete a patient by ID."""
        return Patient.delete(self.__db, patient_id)

    def search_patient(self, name: str) -> list[Patient]:
        """Search patients by name substring."""
        return Patient.search_by_name(self.__db, name)

    def add_medical_record(self, patient_id: int, record: str) -> bool:
        """Add a medical record to a patient."""
        patient = self.get_patient(patient_id)
        if not patient:
            return False
        patient.add_medical_record(record)
        patient.update(self.__db)
        return True

    # ══════════════════════════════════════════════════════════════════
    #  DOCTOR MANAGEMENT
    # ══════════════════════════════════════════════════════════════════

    def add_doctor(self, name: str, age: int, gender: str, contact: str,
                   specialization: str, available_days: list[str]) -> Doctor:
        """Register a new doctor and persist to database."""
        doctor = Doctor(name=name, age=age, gender=gender, contact=contact,
                        specialization=specialization, available_days=available_days)
        doctor.save(self.__db)
        return doctor

    def get_doctor(self, doctor_id: int) -> Optional[Doctor]:
        """Retrieve a doctor by ID."""
        return Doctor.get_by_id(self.__db, doctor_id)

    def get_all_doctors(self) -> list[Doctor]:
        """Retrieve all doctors."""
        return Doctor.get_all(self.__db)

    def update_doctor(self, doctor: Doctor) -> None:
        """Update an existing doctor record."""
        doctor.update(self.__db)

    def delete_doctor(self, doctor_id: int) -> bool:
        """Delete a doctor by ID."""
        return Doctor.delete(self.__db, doctor_id)

    def search_doctor(self, specialization: str) -> list[Doctor]:
        """Search doctors by specialization substring."""
        return Doctor.search_by_specialization(self.__db, specialization)

    # ══════════════════════════════════════════════════════════════════
    #  NURSE MANAGEMENT
    # ══════════════════════════════════════════════════════════════════

    def add_nurse(self, name: str, age: int, gender: str, contact: str,
                  assigned_ward: str = "") -> Nurse:
        """Register a new nurse and persist to database."""
        nurse = Nurse(name=name, age=age, gender=gender, contact=contact,
                      assigned_ward=assigned_ward)
        nurse.save(self.__db)
        return nurse

    def get_nurse(self, nurse_id: int) -> Optional[Nurse]:
        """Retrieve a nurse by ID."""
        return Nurse.get_by_id(self.__db, nurse_id)

    def get_all_nurses(self) -> list[Nurse]:
        """Retrieve all nurses."""
        return Nurse.get_all(self.__db)

    def update_nurse(self, nurse: Nurse) -> None:
        """Update an existing nurse record."""
        nurse.update(self.__db)

    def delete_nurse(self, nurse_id: int) -> bool:
        """Delete a nurse by ID."""
        return Nurse.delete(self.__db, nurse_id)

    # ══════════════════════════════════════════════════════════════════
    #  APPOINTMENT MANAGEMENT
    # ══════════════════════════════════════════════════════════════════

    def book_appointment(self, patient_id: int, doctor_id: int,
                         date: str, time: str) -> Optional[Appointment]:
        """Book a new appointment after verifying patient and doctor exist."""
        if not self.get_patient(patient_id):
            print(f"\\n  ✖  Patient ID {patient_id} not found.")
            return None
        if not self.get_doctor(doctor_id):
            print(f"\\n  ✖  Doctor ID {doctor_id} not found.")
            return None
        appt = Appointment(patient_id=patient_id, doctor_id=doctor_id,
                           date=date, time=time)
        appt.save(self.__db)
        return appt

    def cancel_appointment(self, appointment_id: int) -> bool:
        """Cancel an appointment by ID."""
        appt = Appointment.get_by_id(self.__db, appointment_id)
        if not appt:
            return False
        appt.cancel()
        appt.update(self.__db)
        return True

    def get_all_appointments(self) -> list[Appointment]:
        """Retrieve all appointments."""
        return Appointment.get_all(self.__db)

    def get_appointment(self, aid: int) -> Optional[Appointment]:
        """Retrieve an appointment by ID."""
        return Appointment.get_by_id(self.__db, aid)

    # ══════════════════════════════════════════════════════════════════
    #  PRESCRIPTION MANAGEMENT
    # ══════════════════════════════════════════════════════════════════

    def create_prescription(self, patient_id: int, doctor_id: int,
                            date: str, medicines: list[Medicine]) -> Optional[Prescription]:
        """Create a new prescription with medicines."""
        if not self.get_patient(patient_id):
            print(f"\\n  ✖  Patient ID {patient_id} not found.")
            return None
        if not self.get_doctor(doctor_id):
            print(f"\\n  ✖  Doctor ID {doctor_id} not found.")
            return None
        rx = Prescription(patient_id=patient_id, doctor_id=doctor_id,
                          date=date, medicines=medicines)
        rx.save(self.__db)
        return rx

    def get_all_prescriptions(self) -> list[Prescription]:
        """Retrieve all prescriptions."""
        return Prescription.get_all(self.__db)

    def get_prescription(self, rx_id: int) -> Optional[Prescription]:
        """Retrieve a prescription by ID."""
        return Prescription.get_by_id(self.__db, rx_id)

    # ══════════════════════════════════════════════════════════════════
    #  ROOM MANAGEMENT
    # ══════════════════════════════════════════════════════════════════

    def add_room(self, room_type: str) -> Room:
        """Add a new room to the hospital."""
        room = Room(room_type=room_type)
        room.save(self.__db)
        return room

    def assign_room(self, room_id: int, patient_id: int) -> bool:
        """Assign a patient to a room."""
        room = Room.get_by_id(self.__db, room_id)
        if not room:
            print(f"\\n  ✖  Room ID {room_id} not found.")
            return False
        if not self.get_patient(patient_id):
            print(f"\\n  ✖  Patient ID {patient_id} not found.")
            return False
        try:
            room.assign_patient(patient_id)
            room.update(self.__db)
            return True
        except ValueError as exc:
            print(f"\\n  ✖  {exc}")
            return False

    def discharge_patient_from_room(self, room_id: int) -> bool:
        """Discharge the patient from a room."""
        room = Room.get_by_id(self.__db, room_id)
        if not room:
            print(f"\\n  ✖  Room ID {room_id} not found.")
            return False
        room.discharge_patient()
        room.update(self.__db)
        return True

    def get_all_rooms(self) -> list[Room]:
        """Retrieve all rooms."""
        return Room.get_all(self.__db)

    def get_available_rooms(self) -> list[Room]:
        """Retrieve all available (unoccupied) rooms."""
        return Room.get_available(self.__db)

    # ══════════════════════════════════════════════════════════════════
    #  BILLING MANAGEMENT
    # ══════════════════════════════════════════════════════════════════

    def generate_bill(self, patient_id: int,
                      items: list[tuple[str, float]]) -> Optional[Bill]:
        """Generate a new bill for a patient."""
        if not self.get_patient(patient_id):
            print(f"\\n  ✖  Patient ID {patient_id} not found.")
            return None
        bill = Bill(patient_id=patient_id)
        for desc, amt in items:
            bill.add_item(desc, amt)
        bill.save(self.__db)
        return bill

    def mark_bill_paid(self, bill_id: int) -> bool:
        """Mark a bill as paid."""
        bill = Bill.get_by_id(self.__db, bill_id)
        if not bill:
            return False
        bill.mark_paid()
        bill.update(self.__db)
        return True

    def get_all_bills(self) -> list[Bill]:
        """Retrieve all bills."""
        return Bill.get_all(self.__db)

    def get_bill(self, bid: int) -> Optional[Bill]:
        """Retrieve a bill by ID."""
        return Bill.get_by_id(self.__db, bid)

    # ══════════════════════════════════════════════════════════════════
    #  POLYMORPHIC DISPLAY (demonstrates Polymorphism)
    # ══════════════════════════════════════════════════════════════════

    def display_all_patients(self) -> None:
        """Print all patients using polymorphic display_info()."""
        patients = self.get_all_patients()
        if not patients:
            print("\\n  No patients registered.")
            return
        print(f"\\n  {'═' * 50}")
        print(f"  Total Patients: {len(patients)}")
        print(f"  {'═' * 50}")
        for p in patients:
            print(p.display_info())
            print()

    def display_all_doctors(self) -> None:
        """Print all doctors using polymorphic display_info()."""
        doctors = self.get_all_doctors()
        if not doctors:
            print("\\n  No doctors registered.")
            return
        print(f"\\n  {'═' * 50}")
        print(f"  Total Doctors: {len(doctors)}")
        print(f"  {'═' * 50}")
        for d in doctors:
            print(d.display_info())
            print()

    def display_all(self) -> None:
        """
        Print ALL persons (patients, doctors, nurses) — demonstrates
        Polymorphism by calling display_info() on different Person subtypes.
        """
        people: list[Person] = []
        people.extend(self.get_all_patients())
        people.extend(self.get_all_doctors())
        people.extend(self.get_all_nurses())
        if not people:
            print("\\n  No people registered in the hospital.")
            return
        print(f"\\n  {'═' * 50}")
        print(f"  All Hospital Personnel & Patients ({len(people)} total)")
        print(f"  {'═' * 50}")
        for person in people:
            print(f"  [{person.get_role()}]")
            print(person.display_info())
            print()
''',

    "hospital_system/database/__init__.py": '''"""Database package for Hospital Management System."""''',

    "hospital_system/database/db_manager.py": '''
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
            print(f"\\n  [ERROR]  Database error: {exc}")
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
            print(f"\\n  [ERROR]  Database error: {exc}")
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
            print(f"\\n  [ERROR]  Database error: {exc}")
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
''',

    "hospital_system/models/__init__.py": '''"""Models package for Hospital Management System."""''',

    "hospital_system/models/person.py": '''
"""
Person Module (Abstract Base Class)
====================================
Demonstrates **Encapsulation** (private attributes + property access)
and **Abstraction** (ABC with abstract methods).

All staff and patient types inherit from Person.
"""

from abc import ABC, abstractmethod
from typing import Optional


# ── Validation constants ───────────────────────────────────────────────
VALID_GENDERS: tuple[str, ...] = ("Male", "Female", "Other")
MIN_AGE: int = 0
MAX_AGE: int = 120
CONTACT_LENGTH: int = 11


class Person(ABC):
    """
    Abstract base class representing any person in the hospital.

    Encapsulation:
        All attributes are **name-mangled private** (double underscore).
        External access is provided exclusively through ``@property``
        decorators with built-in validation.

    Abstraction:
        Subclasses *must* implement ``get_role()`` and ``display_info()``.

    Attributes:
        __name    (str): Full name (alphabetic characters and spaces only).
        __age     (int): Age between 0 and 120.
        __gender  (str): One of 'Male', 'Female', 'Other'.
        __contact (str): Exactly 11 digit characters.
    """

    def __init__(
        self,
        name: str,
        age: int,
        gender: str,
        contact: str,
    ) -> None:
        """
        Initialise a Person instance with validated data.

        Args:
            name:    Full name (letters and spaces only).
            age:     Integer age in [0, 120].
            gender:  'Male', 'Female', or 'Other'.
            contact: 11-digit contact string.
        """
        # Use the property setters so validation runs on construction.
        self.name = name
        self.age = age
        self.gender = gender
        self.contact = contact

    # ── name ───────────────────────────────────────────────────────────
    @property
    def name(self) -> str:
        """Return the person's name."""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """Set name after validating it contains only letters and spaces."""
        if not value or not value.replace(" ", "").isalpha():
            raise ValueError(
                "Name must be a non-empty string containing only letters and spaces."
            )
        self.__name = value.strip().title()

    # ── age ────────────────────────────────────────────────────────────
    @property
    def age(self) -> int:
        """Return the person's age."""
        return self.__age

    @age.setter
    def age(self, value: int) -> None:
        """Set age after validating it is an integer between 0 and 120."""
        if not isinstance(value, int) or not (MIN_AGE <= value <= MAX_AGE):
            raise ValueError(f"Age must be an integer between {MIN_AGE} and {MAX_AGE}.")
        self.__age = value

    # ── gender ─────────────────────────────────────────────────────────
    @property
    def gender(self) -> str:
        """Return the person's gender."""
        return self.__gender

    @gender.setter
    def gender(self, value: str) -> None:
        """Set gender after validating it is one of the allowed values."""
        normalised = value.strip().title()
        if normalised not in VALID_GENDERS:
            raise ValueError(
                f"Gender must be one of {VALID_GENDERS}. Got '{value}'."
            )
        self.__gender = normalised

    # ── contact ────────────────────────────────────────────────────────
    @property
    def contact(self) -> str:
        """Return the person's contact number."""
        return self.__contact

    @contact.setter
    def contact(self, value: str) -> None:
        """Set contact after validating it is exactly 11 digits."""
        cleaned = value.strip()
        if not cleaned.isdigit() or len(cleaned) != CONTACT_LENGTH:
            raise ValueError(
                f"Contact must be exactly {CONTACT_LENGTH} digits. Got '{value}'."
            )
        self.__contact = cleaned

    # ── Abstract interface ─────────────────────────────────────────────

    @abstractmethod
    def get_role(self) -> str:
        """Return the role of this person (e.g. 'Patient', 'Doctor')."""
        ...

    @abstractmethod
    def display_info(self) -> str:
        """Return a human-readable summary of this person's details."""
        ...

    # ── Shared helpers ─────────────────────────────────────────────────

    def _base_info(self) -> str:
        """Return the common info string shared by all subtypes."""
        return (
            f"  Name    : {self.name}\\n"
            f"  Age     : {self.age}\\n"
            f"  Gender  : {self.gender}\\n"
            f"  Contact : {self.contact}"
        )
''',

    "hospital_system/models/patient.py": '''
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
        return "\\n".join(lines)

    # ── Abstract implementations (Polymorphism) ───────────────────────

    def get_role(self) -> str:
        """Return 'Patient'."""
        return "Patient"

    def display_info(self) -> str:
        """Return a formatted summary of patient details."""
        header = f"  ── Patient (ID: {self.__patient_id or 'N/A'}) ──"
        base = self._base_info()
        extra = (
            f"  Blood Gr: {self.__blood_group}\\n"
            f"  History :\\n{self.get_history()}"
        )
        return f"{header}\\n{base}\\n{extra}"

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
''',

    "hospital_system/models/doctor.py": '''
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
            f"  Spec.   : {self.__specialization}\\n"
            f"  Days    : {days_str}"
        )
        return f"{header}\\n{base}\\n{extra}"

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
''',

    "hospital_system/models/nurse.py": '''
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
        return f"{header}\\n{base}\\n{extra}"

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
''',

    "hospital_system/models/appointment.py": '''
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
        return (f"  ── Appointment (ID: {self.__appointment_id or 'N/A'}) ──\\n"
                f"  Patient ID : {self.__patient_id}\\n"
                f"  Doctor ID  : {self.__doctor_id}\\n"
                f"  Date       : {self.__date}\\n"
                f"  Time       : {self.__time}\\n"
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
''',

    "hospital_system/models/prescription.py": '''
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
        return "\\n".join(lines)

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
''',

    "hospital_system/models/bill.py": '''
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
        return "\\n".join(lines)

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
''',

    "hospital_system/models/room.py": '''
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
        return (f"  ── Room (ID: {self.__room_id or 'N/A'}) ──\\n"
                f"  Type       : {self.__room_type}\\n"
                f"  Occupied   : {'Yes' if self.__is_occupied else 'No'}\\n"
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
''',

    "hospital_system/ui/__init__.py": '''"""UI package for Hospital Management System."""''',

    "hospital_system/ui/menu.py": '''
"""
Console Menu System
===================
All interactive menus and input validation for the Hospital Management System.
"""

import re
from datetime import datetime
from typing import Optional

from hospital_system.controllers.hospital import Hospital
from hospital_system.models.prescription import Medicine
from hospital_system.models.patient import VALID_BLOOD_GROUPS


# ── Input Validation Helpers ──────────────────────────────────────────

def get_valid_name(prompt: str = "  Enter name: ") -> str:
    """Prompt until a valid name (letters/spaces only) is entered."""
    while True:
        val = input(prompt).strip()
        if val and val.replace(" ", "").isalpha():
            return val
        print("  [ERROR]  Name must contain only letters and spaces.")


def get_valid_age(prompt: str = "  Enter age: ") -> int:
    """Prompt until a valid age (0-120) is entered."""
    while True:
        val = input(prompt).strip()
        if val.isdigit() and 0 <= int(val) <= 120:
            return int(val)
        print("  [ERROR]  Age must be an integer between 0 and 120.")


def get_valid_gender(prompt: str = "  Enter gender (Male/Female/Other): ") -> str:
    """Prompt until a valid gender is entered."""
    while True:
        val = input(prompt).strip().title()
        if val in ("Male", "Female", "Other"):
            return val
        print("  [ERROR]  Gender must be Male, Female, or Other.")


def get_valid_contact(prompt: str = "  Enter contact (11 digits): ") -> str:
    """Prompt until a valid 11-digit contact is entered."""
    while True:
        val = input(prompt).strip()
        if val.isdigit() and len(val) == 11:
            return val
        print("  [ERROR]  Contact must be exactly 11 digits.")


def get_valid_blood_group(prompt: str = "  Enter blood group (A+,A-,B+,B-,O+,O-,AB+,AB-): ") -> str:
    """Prompt until a valid blood group is entered."""
    while True:
        val = input(prompt).strip().upper()
        if val in VALID_BLOOD_GROUPS:
            return val
        print(f"  [ERROR]  Must be one of {VALID_BLOOD_GROUPS}.")


def get_valid_date(prompt: str = "  Enter date (YYYY-MM-DD): ") -> str:
    """Prompt until a valid date is entered."""
    while True:
        val = input(prompt).strip()
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return val
        except ValueError:
            print("  [ERROR]  Invalid date. Use YYYY-MM-DD format.")


def get_valid_time(prompt: str = "  Enter time (HH:MM): ") -> str:
    """Prompt until a valid time is entered."""
    while True:
        val = input(prompt).strip()
        if re.match(r"^\\d{2}:\\d{2}$", val):
            try:
                datetime.strptime(val, "%H:%M")
                return val
            except ValueError:
                pass
        print("  [ERROR]  Invalid time. Use HH:MM format (00:00 - 23:59).")


def get_valid_int(prompt: str, min_val: int = 1) -> int:
    """Prompt until a valid integer >= min_val is entered."""
    while True:
        val = input(prompt).strip()
        if val.isdigit() and int(val) >= min_val:
            return int(val)
        print(f"  [ERROR]  Please enter a valid integer (>= {min_val}).")


def get_valid_float(prompt: str) -> float:
    """Prompt until a valid positive float is entered."""
    while True:
        val = input(prompt).strip()
        try:
            f = float(val)
            if f >= 0:
                return f
            print("  [ERROR]  Amount cannot be negative.")
        except ValueError:
            print("  [ERROR]  Please enter a valid number.")


def get_valid_days() -> list[str]:
    """Prompt for available days (comma-separated weekday names)."""
    valid = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    while True:
        val = input("  Enter available days (comma-separated, e.g. Monday,Wednesday,Friday): ").strip()
        days = [d.strip().title() for d in val.split(",") if d.strip()]
        if days and all(d in valid for d in days):
            return days
        print(f"  [ERROR]  Each day must be one of {valid}.")


def pause() -> None:
    """Wait for user to press Enter."""
    input("\\n  Press Enter to continue...")


# ── Banner ────────────────────────────────────────────────────────────

def print_banner() -> None:
    """Print the main application banner."""
    print("\\n" + "  " + "╔" + "═" * 42 + "╗")
    print("  " + "║" + "   HOSPITAL MANAGEMENT SYSTEM".center(42) + "║")
    print("  " + "╚" + "═" * 42 + "╝")


# ══════════════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════════════

def main_menu(hospital: Hospital) -> None:
    """Display the main menu loop."""
    while True:
        print_banner()
        print(f"\\n  Welcome to {hospital.name}")
        print("  ─" * 22)
        print("  1. Patient Management")
        print("  2. Doctor Management")
        print("  3. Nurse Management")
        print("  4. Appointment Management")
        print("  5. Prescription Management")
        print("  6. Room Management")
        print("  7. Billing Management")
        print("  8. Search & Reports")
        print("  9. Exit")
        print("  ─" * 22)

        choice = input("  Enter choice: ").strip()
        if choice == "1":
            patient_menu(hospital)
        elif choice == "2":
            doctor_menu(hospital)
        elif choice == "3":
            nurse_menu(hospital)
        elif choice == "4":
            appointment_menu(hospital)
        elif choice == "5":
            prescription_menu(hospital)
        elif choice == "6":
            room_menu(hospital)
        elif choice == "7":
            billing_menu(hospital)
        elif choice == "8":
            search_menu(hospital)
        elif choice == "9":
            print("\\n  Goodbye! Thank you for using Hospital Management System.\\n")
            break
        else:
            print("  [ERROR]  Invalid choice. Please try again.")


# ══════════════════════════════════════════════════════════════════════
#  PATIENT MENU
# ══════════════════════════════════════════════════════════════════════

def patient_menu(hospital: Hospital) -> None:
    """Patient management sub-menu."""
    while True:
        print("\\n  ┌─── Patient Management ───┐")
        print("  │ 1. Register new patient  │")
        print("  │ 2. View all patients     │")
        print("  │ 3. View medical history  │")
        print("  │ 4. Add medical record    │")
        print("  │ 5. Update patient info   │")
        print("  │ 6. Delete patient        │")
        print("  │ 7. Back to main menu     │")
        print("  └──────────────────────────┘")

        choice = input("  Enter choice: ").strip()
        try:
            if choice == "1":
                name = get_valid_name()
                age = get_valid_age()
                gender = get_valid_gender()
                contact = get_valid_contact()
                blood = get_valid_blood_group()
                p = hospital.add_patient(name, age, gender, contact, blood)
                print(f"\\n  [OK]  Patient registered with ID: {p.patient_id}")
            elif choice == "2":
                hospital.display_all_patients()
            elif choice == "3":
                pid = get_valid_int("  Enter Patient ID: ")
                p = hospital.get_patient(pid)
                if p:
                    print(f"\\n  Medical History for {p.name}:")
                    print(p.get_history())
                else:
                    print("  [ERROR]  Patient not found.")
            elif choice == "4":
                pid = get_valid_int("  Enter Patient ID: ")
                record = input("  Enter medical record: ").strip()
                if hospital.add_medical_record(pid, record):
                    print("  [OK]  Medical record added.")
                else:
                    print("  [ERROR]  Patient not found.")
            elif choice == "5":
                pid = get_valid_int("  Enter Patient ID: ")
                p = hospital.get_patient(pid)
                if not p:
                    print("  [ERROR]  Patient not found.")
                else:
                    print(f"  Updating patient: {p.name}")
                    p.name = get_valid_name("  New name (current: {}): ".format(p.name))
                    p.age = get_valid_age("  New age (current: {}): ".format(p.age))
                    p.gender = get_valid_gender("  New gender (current: {}): ".format(p.gender))
                    p.contact = get_valid_contact("  New contact (current: {}): ".format(p.contact))
                    p.blood_group = get_valid_blood_group("  New blood group (current: {}): ".format(p.blood_group))
                    hospital.update_patient(p)
                    print("  [OK]  Patient updated.")
            elif choice == "6":
                pid = get_valid_int("  Enter Patient ID: ")
                if hospital.delete_patient(pid):
                    print("  [OK]  Patient deleted.")
                else:
                    print("  [ERROR]  Failed to delete patient.")
            elif choice == "7":
                break
            else:
                print("  [ERROR]  Invalid choice.")
        except ValueError as e:
            print(f"  [ERROR]  {e}")
        pause()


# ══════════════════════════════════════════════════════════════════════
#  DOCTOR MENU
# ══════════════════════════════════════════════════════════════════════

def doctor_menu(hospital: Hospital) -> None:
    """Doctor management sub-menu."""
    while True:
        print("\\n  ┌─── Doctor Management ────┐")
        print("  │ 1. Register new doctor   │")
        print("  │ 2. View all doctors      │")
        print("  │ 3. Update doctor info    │")
        print("  │ 4. Delete doctor         │")
        print("  │ 5. Back to main menu     │")
        print("  └──────────────────────────┘")

        choice = input("  Enter choice: ").strip()
        try:
            if choice == "1":
                name = get_valid_name()
                age = get_valid_age()
                gender = get_valid_gender()
                contact = get_valid_contact()
                spec = input("  Enter specialization: ").strip()
                days = get_valid_days()
                d = hospital.add_doctor(name, age, gender, contact, spec, days)
                print(f"\\n  [OK]  Doctor registered with ID: {d.doctor_id}")
            elif choice == "2":
                hospital.display_all_doctors()
            elif choice == "3":
                did = get_valid_int("  Enter Doctor ID: ")
                d = hospital.get_doctor(did)
                if not d:
                    print("  [ERROR]  Doctor not found.")
                else:
                    print(f"  Updating doctor: {d.name}")
                    d.name = get_valid_name("  New name (current: {}): ".format(d.name))
                    d.age = get_valid_age("  New age (current: {}): ".format(d.age))
                    d.gender = get_valid_gender("  New gender (current: {}): ".format(d.gender))
                    d.contact = get_valid_contact("  New contact (current: {}): ".format(d.contact))
                    d.specialization = input("  New specialization (current: {}): ".format(d.specialization)).strip()
                    d.available_days = get_valid_days()
                    hospital.update_doctor(d)
                    print("  [OK]  Doctor updated.")
            elif choice == "4":
                did = get_valid_int("  Enter Doctor ID: ")
                if hospital.delete_doctor(did):
                    print("  [OK]  Doctor deleted.")
                else:
                    print("  [ERROR]  Failed to delete doctor.")
            elif choice == "5":
                break
            else:
                print("  [ERROR]  Invalid choice.")
        except ValueError as e:
            print(f"  [ERROR]  {e}")
        pause()


# ══════════════════════════════════════════════════════════════════════
#  NURSE MENU
# ══════════════════════════════════════════════════════════════════════

def nurse_menu(hospital: Hospital) -> None:
    """Nurse management sub-menu."""
    while True:
        print("\\n  ┌─── Nurse Management ─────┐")
        print("  │ 1. Register new nurse    │")
        print("  │ 2. View all nurses       │")
        print("  │ 3. Assign ward           │")
        print("  │ 4. Update nurse info     │")
        print("  │ 5. Delete nurse          │")
        print("  │ 6. Back to main menu     │")
        print("  └──────────────────────────┘")

        choice = input("  Enter choice: ").strip()
        try:
            if choice == "1":
                name = get_valid_name()
                age = get_valid_age()
                gender = get_valid_gender()
                contact = get_valid_contact()
                ward = input("  Enter assigned ward (or leave blank): ").strip()
                n = hospital.add_nurse(name, age, gender, contact, ward)
                print(f"\\n  [OK]  Nurse registered with ID: {n.nurse_id}")
            elif choice == "2":
                nurses = hospital.get_all_nurses()
                if not nurses:
                    print("\\n  No nurses registered.")
                else:
                    for n in nurses:
                        print(n.display_info())
                        print()
            elif choice == "3":
                nid = get_valid_int("  Enter Nurse ID: ")
                n = hospital.get_nurse(nid)
                if not n:
                    print("  [ERROR]  Nurse not found.")
                else:
                    ward = input("  Enter ward name: ").strip()
                    n.assign_ward(ward)
                    hospital.update_nurse(n)
                    print(f"  [OK]  Nurse assigned to ward: {ward}")
            elif choice == "4":
                nid = get_valid_int("  Enter Nurse ID: ")
                n = hospital.get_nurse(nid)
                if not n:
                    print("  [ERROR]  Nurse not found.")
                else:
                    n.name = get_valid_name("  New name (current: {}): ".format(n.name))
                    n.age = get_valid_age("  New age (current: {}): ".format(n.age))
                    n.gender = get_valid_gender("  New gender (current: {}): ".format(n.gender))
                    n.contact = get_valid_contact("  New contact (current: {}): ".format(n.contact))
                    hospital.update_nurse(n)
                    print("  [OK]  Nurse updated.")
            elif choice == "5":
                nid = get_valid_int("  Enter Nurse ID: ")
                if hospital.delete_nurse(nid):
                    print("  [OK]  Nurse deleted.")
                else:
                    print("  [ERROR]  Failed to delete nurse.")
            elif choice == "6":
                break
            else:
                print("  [ERROR]  Invalid choice.")
        except ValueError as e:
            print(f"  [ERROR]  {e}")
        pause()


# ══════════════════════════════════════════════════════════════════════
#  APPOINTMENT MENU
# ══════════════════════════════════════════════════════════════════════

def appointment_menu(hospital: Hospital) -> None:
    """Appointment management sub-menu."""
    while True:
        print("\\n  ┌─── Appointment Management ──┐")
        print("  │ 1. Book appointment          │")
        print("  │ 2. View all appointments      │")
        print("  │ 3. Confirm appointment        │")
        print("  │ 4. Cancel appointment         │")
        print("  │ 5. Reschedule appointment     │")
        print("  │ 6. Back to main menu          │")
        print("  └──────────────────────────────-┘")

        choice = input("  Enter choice: ").strip()
        try:
            if choice == "1":
                pid = get_valid_int("  Enter Patient ID: ")
                did = get_valid_int("  Enter Doctor ID: ")
                date = get_valid_date()
                time = get_valid_time()
                appt = hospital.book_appointment(pid, did, date, time)
                if appt:
                    print(f"\\n  [OK]  Appointment booked with ID: {appt.appointment_id}")
            elif choice == "2":
                appts = hospital.get_all_appointments()
                if not appts:
                    print("\\n  No appointments found.")
                else:
                    for a in appts:
                        print(a.display())
                        print()
            elif choice == "3":
                aid = get_valid_int("  Enter Appointment ID: ")
                appt = hospital.get_appointment(aid)
                if appt:
                    appt.confirm()
                    appt.update(hospital._Hospital__db)
                    print("  [OK]  Appointment confirmed.")
                else:
                    print("  [ERROR]  Appointment not found.")
            elif choice == "4":
                aid = get_valid_int("  Enter Appointment ID: ")
                if hospital.cancel_appointment(aid):
                    print("  [OK]  Appointment cancelled.")
                else:
                    print("  [ERROR]  Appointment not found.")
            elif choice == "5":
                aid = get_valid_int("  Enter Appointment ID: ")
                appt = hospital.get_appointment(aid)
                if appt:
                    new_date = get_valid_date("  Enter new date (YYYY-MM-DD): ")
                    new_time = get_valid_time("  Enter new time (HH:MM): ")
                    appt.reschedule(new_date, new_time)
                    appt.update(hospital._Hospital__db)
                    print("  [OK]  Appointment rescheduled.")
                else:
                    print("  [ERROR]  Appointment not found.")
            elif choice == "6":
                break
            else:
                print("  [ERROR]  Invalid choice.")
        except ValueError as e:
            print(f"  [ERROR]  {e}")
        pause()


# ══════════════════════════════════════════════════════════════════════
#  PRESCRIPTION MENU
# ══════════════════════════════════════════════════════════════════════

def prescription_menu(hospital: Hospital) -> None:
    """Prescription management sub-menu."""
    while True:
        print("\\n  ┌─── Prescription Management ──┐")
        print("  │ 1. Create prescription        │")
        print("  │ 2. View all prescriptions      │")
        print("  │ 3. View prescription details   │")
        print("  │ 4. Delete prescription         │")
        print("  │ 5. Back to main menu           │")
        print("  └────────────────────────────────┘")

        choice = input("  Enter choice: ").strip()
        try:
            if choice == "1":
                pid = get_valid_int("  Enter Patient ID: ")
                did = get_valid_int("  Enter Doctor ID: ")
                date = get_valid_date()
                medicines: list[Medicine] = []
                while True:
                    print("\\n  Add a medicine (or type 'done' to finish):")
                    mname = input("  Medicine name: ").strip()
                    if mname.lower() == "done":
                        break
                    dosage = input("  Dosage (e.g. 500mg): ").strip()
                    freq = input("  Frequency (e.g. 3 times/day): ").strip()
                    dur = input("  Duration (e.g. 7 days): ").strip()
                    medicines.append(Medicine(name=mname, dosage=dosage, frequency=freq, duration=dur))
                if not medicines:
                    print("  [ERROR]  At least one medicine is required.")
                    continue
                rx = hospital.create_prescription(pid, did, date, medicines)
                if rx:
                    print(f"\\n  [OK]  Prescription created with ID: {rx.prescription_id}")
            elif choice == "2":
                rxs = hospital.get_all_prescriptions()
                if not rxs:
                    print("\\n  No prescriptions found.")
                else:
                    for rx in rxs:
                        print(rx.generate_summary())
            elif choice == "3":
                rid = get_valid_int("  Enter Prescription ID: ")
                rx = hospital.get_prescription(rid)
                if rx:
                    print(rx.display())
                else:
                    print("  [ERROR]  Prescription not found.")
            elif choice == "4":
                from hospital_system.models.prescription import Prescription
                rid = get_valid_int("  Enter Prescription ID: ")
                if Prescription.delete(hospital._Hospital__db, rid):
                    print("  ✔  Prescription deleted.")
                else:
                    print("  [ERROR]  Failed to delete.")
            elif choice == "5":
                break
            else:
                print("  [ERROR]  Invalid choice.")
        except ValueError as e:
            print(f"  [ERROR]  {e}")
        pause()


# ══════════════════════════════════════════════════════════════════════
#  ROOM MENU
# ══════════════════════════════════════════════════════════════════════

def room_menu(hospital: Hospital) -> None:
    """Room management sub-menu."""
    while True:
        print("\\n  ┌─── Room Management ──────┐")
        print("  │ 1. Add new room          │")
        print("  │ 2. View all rooms        │")
        print("  │ 3. View available rooms   │")
        print("  │ 4. Assign patient to room │")
        print("  │ 5. Discharge from room    │")
        print("  │ 6. Back to main menu     │")
        print("  └──────────────────────────┘")

        choice = input("  Enter choice: ").strip()
        try:
            if choice == "1":
                rtype = input("  Enter room type (General/Private/ICU/Emergency): ").strip()
                room = hospital.add_room(rtype)
                print(f"\\n  ✔  Room added with ID: {room.room_id}")
            elif choice == "2":
                rooms = hospital.get_all_rooms()
                if not rooms:
                    print("\\n  No rooms found.")
                else:
                    for r in rooms:
                        print(r.display())
                        print()
            elif choice == "3":
                rooms = hospital.get_available_rooms()
                if not rooms:
                    print("\\n  No available rooms.")
                else:
                    for r in rooms:
                        print(r.display())
                        print()
            elif choice == "4":
                rid = get_valid_int("  Enter Room ID: ")
                pid = get_valid_int("  Enter Patient ID: ")
                if hospital.assign_room(rid, pid):
                    print("  ✔  Patient assigned to room.")
            elif choice == "5":
                rid = get_valid_int("  Enter Room ID: ")
                if hospital.discharge_patient_from_room(rid):
                    print("  ✔  Patient discharged from room.")
            elif choice == "6":
                break
            else:
                print("  [ERROR]  Invalid choice.")
        except ValueError as e:
            print(f"  [ERROR]  {e}")
        pause()


# ══════════════════════════════════════════════════════════════════════
#  BILLING MENU
# ══════════════════════════════════════════════════════════════════════

def billing_menu(hospital: Hospital) -> None:
    """Billing management sub-menu."""
    while True:
        print("\\n  ┌─── Billing Management ───┐")
        print("  │ 1. Generate new bill      │")
        print("  │ 2. View all bills         │")
        print("  │ 3. View bill details      │")
        print("  │ 4. Mark bill as paid      │")
        print("  │ 5. Back to main menu      │")
        print("  └──────────────────────────-┘")

        choice = input("  Enter choice: ").strip()
        try:
            if choice == "1":
                pid = get_valid_int("  Enter Patient ID: ")
                items: list[tuple[str, float]] = []
                while True:
                    desc = input("  Item description (or 'done' to finish): ").strip()
                    if desc.lower() == "done":
                        break
                    amount = get_valid_float("  Amount (Rs.): ")
                    items.append((desc, amount))
                if not items:
                    print("  [ERROR]  At least one item is required.")
                    continue
                bill = hospital.generate_bill(pid, items)
                if bill:
                    print(f"\\n  ✔  Bill generated with ID: {bill.bill_id}")
                    print(bill.display())
            elif choice == "2":
                bills = hospital.get_all_bills()
                if not bills:
                    print("\\n  No bills found.")
                else:
                    for b in bills:
                        print(b.display())
                        print()
            elif choice == "3":
                bid = get_valid_int("  Enter Bill ID: ")
                b = hospital.get_bill(bid)
                if b:
                    print(b.display())
                else:
                    print("  ✖  Bill not found.")
            elif choice == "4":
                bid = get_valid_int("  Enter Bill ID: ")
                if hospital.mark_bill_paid(bid):
                    print("  ✔  Bill marked as paid.")
                else:
                    print("  ✖  Bill not found.")
            elif choice == "5":
                break
            else:
                print("  ✖  Invalid choice.")
        except ValueError as e:
            print(f"  ✖  {e}")
        pause()


# ══════════════════════════════════════════════════════════════════════
#  SEARCH & REPORTS MENU
# ══════════════════════════════════════════════════════════════════════

def search_menu(hospital: Hospital) -> None:
    """Search & Reports sub-menu."""
    while True:
        print("\\n  ┌─── Search & Reports ─────┐")
        print("  │ 1. Search patient by name │")
        print("  │ 2. Search doctor by spec  │")
        print("  │ 3. View all personnel     │")
        print("  │ 4. Patient bills report   │")
        print("  │ 5. Patient appointments   │")
        print("  │ 6. Back to main menu      │")
        print("  └──────────────────────────-┘")

        choice = input("  Enter choice: ").strip()
        try:
            if choice == "1":
                name = input("  Enter patient name to search: ").strip()
                results = hospital.search_patient(name)
                if not results:
                    print("  No patients found.")
                else:
                    for p in results:
                        print(p.display_info())
                        print()
            elif choice == "2":
                spec = input("  Enter specialization to search: ").strip()
                results = hospital.search_doctor(spec)
                if not results:
                    print("  No doctors found.")
                else:
                    for d in results:
                        print(d.display_info())
                        print()
            elif choice == "3":
                hospital.display_all()
            elif choice == "4":
                pid = get_valid_int("  Enter Patient ID: ")
                from hospital_system.models.bill import Bill
                bills = Bill.get_by_patient(hospital._Hospital__db, pid)
                if not bills:
                    print("  No bills found for this patient.")
                else:
                    for b in bills:
                        print(b.display())
                        print()
            elif choice == "5":
                pid = get_valid_int("  Enter Patient ID: ")
                from hospital_system.models.appointment import Appointment
                appts = Appointment.get_by_patient(hospital._Hospital__db, pid)
                if not appts:
                    print("  No appointments found for this patient.")
                else:
                    for a in appts:
                        print(a.display())
                        print()
            elif choice == "6":
                break
            else:
                print("  ✖  Invalid choice.")
        except ValueError as e:
            print(f"  ✖  {e}")
        pause()
''',
}


def create_project():
    """Create all directories and files."""
    for filepath, content in files.items():
        # Create directory if not exists
        dirname = os.path.dirname(filepath)
        if dirname:
            os.makedirs(dirname, exist_ok=True)

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.lstrip())  # Remove leading newline if any
        print(f"Created: {filepath}")

    print("\n✅ Project generated successfully!")
    print(f"Run the system with: python {PROJECT_ROOT}/main.py")


if __name__ == "__main__":
    create_project()
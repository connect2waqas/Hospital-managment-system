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
            print(f"\n  ✖  Patient ID {patient_id} not found.")
            return None
        if not self.get_doctor(doctor_id):
            print(f"\n  ✖  Doctor ID {doctor_id} not found.")
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
            print(f"\n  ✖  Patient ID {patient_id} not found.")
            return None
        if not self.get_doctor(doctor_id):
            print(f"\n  ✖  Doctor ID {doctor_id} not found.")
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
            print(f"\n  ✖  Room ID {room_id} not found.")
            return False
        if not self.get_patient(patient_id):
            print(f"\n  ✖  Patient ID {patient_id} not found.")
            return False
        try:
            room.assign_patient(patient_id)
            room.update(self.__db)
            return True
        except ValueError as exc:
            print(f"\n  ✖  {exc}")
            return False

    def discharge_patient_from_room(self, room_id: int) -> bool:
        """Discharge the patient from a room."""
        room = Room.get_by_id(self.__db, room_id)
        if not room:
            print(f"\n  ✖  Room ID {room_id} not found.")
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
            print(f"\n  ✖  Patient ID {patient_id} not found.")
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
            print("\n  No patients registered.")
            return
        print(f"\n  {'═' * 50}")
        print(f"  Total Patients: {len(patients)}")
        print(f"  {'═' * 50}")
        for p in patients:
            print(p.display_info())
            print()

    def display_all_doctors(self) -> None:
        """Print all doctors using polymorphic display_info()."""
        doctors = self.get_all_doctors()
        if not doctors:
            print("\n  No doctors registered.")
            return
        print(f"\n  {'═' * 50}")
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
            print("\n  No people registered in the hospital.")
            return
        print(f"\n  {'═' * 50}")
        print(f"  All Hospital Personnel & Patients ({len(people)} total)")
        print(f"  {'═' * 50}")
        for person in people:
            print(f"  [{person.get_role()}]")
            print(person.display_info())
            print()

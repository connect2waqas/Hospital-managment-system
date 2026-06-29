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
        if re.match(r"^\d{2}:\d{2}$", val):
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
    input("\n  Press Enter to continue...")


# ── Banner ────────────────────────────────────────────────────────────

def print_banner() -> None:
    """Print the main application banner."""
    print("\n" + "  " + "╔" + "═" * 42 + "╗")
    print("  " + "║" + "   HOSPITAL MANAGEMENT SYSTEM".center(42) + "║")
    print("  " + "╚" + "═" * 42 + "╝")


# ══════════════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════════════

def main_menu(hospital: Hospital) -> None:
    """Display the main menu loop."""
    while True:
        print_banner()
        print(f"\n  Welcome to {hospital.name}")
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
            print("\n  Goodbye! Thank you for using Hospital Management System.\n")
            break
        else:
            print("  [ERROR]  Invalid choice. Please try again.")


# ══════════════════════════════════════════════════════════════════════
#  PATIENT MENU
# ══════════════════════════════════════════════════════════════════════

def patient_menu(hospital: Hospital) -> None:
    """Patient management sub-menu."""
    while True:
        print("\n  ┌─── Patient Management ───┐")
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
                print(f"\n  [OK]  Patient registered with ID: {p.patient_id}")
            elif choice == "2":
                hospital.display_all_patients()
            elif choice == "3":
                pid = get_valid_int("  Enter Patient ID: ")
                p = hospital.get_patient(pid)
                if p:
                    print(f"\n  Medical History for {p.name}:")
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
        print("\n  ┌─── Doctor Management ────┐")
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
                print(f"\n  [OK]  Doctor registered with ID: {d.doctor_id}")
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
        print("\n  ┌─── Nurse Management ─────┐")
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
                print(f"\n  [OK]  Nurse registered with ID: {n.nurse_id}")
            elif choice == "2":
                nurses = hospital.get_all_nurses()
                if not nurses:
                    print("\n  No nurses registered.")
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
        print("\n  ┌─── Appointment Management ──┐")
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
                    print(f"\n  [OK]  Appointment booked with ID: {appt.appointment_id}")
            elif choice == "2":
                appts = hospital.get_all_appointments()
                if not appts:
                    print("\n  No appointments found.")
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
        print("\n  ┌─── Prescription Management ──┐")
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
                    print("\n  Add a medicine (or type 'done' to finish):")
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
                    print(f"\n  [OK]  Prescription created with ID: {rx.prescription_id}")
            elif choice == "2":
                rxs = hospital.get_all_prescriptions()
                if not rxs:
                    print("\n  No prescriptions found.")
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
        print("\n  ┌─── Room Management ──────┐")
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
                print(f"\n  ✔  Room added with ID: {room.room_id}")
            elif choice == "2":
                rooms = hospital.get_all_rooms()
                if not rooms:
                    print("\n  No rooms found.")
                else:
                    for r in rooms:
                        print(r.display())
                        print()
            elif choice == "3":
                rooms = hospital.get_available_rooms()
                if not rooms:
                    print("\n  No available rooms.")
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
        print("\n  ┌─── Billing Management ───┐")
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
                    print(f"\n  ✔  Bill generated with ID: {bill.bill_id}")
                    print(bill.display())
            elif choice == "2":
                bills = hospital.get_all_bills()
                if not bills:
                    print("\n  No bills found.")
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
        print("\n  ┌─── Search & Reports ─────┐")
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

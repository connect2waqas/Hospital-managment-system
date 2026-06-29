# 🏥 Hospital Management System

A complete **Hospital Management System** built with **Python** and **SQLite**, developed as a 4th‑semester project under the supervision of **Sir Fahad Quereshi**. This project showcases a pure **Object‑Oriented Programming** approach, applying the four pillars of OOP in a real‑world application.

---

## 📌 Features

- **Patient Management** – Register, view, update, delete, search, and maintain medical history.
- **Doctor Management** – Register, view, update, delete, and search by specialization.
- **Nurse Management** – Register, view, assign wards, update, and delete.
- **Appointment Management** – Book, confirm, cancel, reschedule, and view all appointments.
- **Prescription Management** – Create prescriptions with multiple medicines, view details, and delete.
- **Room Management** – Add rooms, assign patients, discharge, and view available rooms.
- **Billing Management** – Generate itemised bills, view all bills, mark as paid.
- **Search & Reports** – Search patients by name, doctors by specialization, view all personnel, patient‑specific bills and appointments.

All data is persistently stored in a local **SQLite** database with proper foreign key constraints.

---

## 🧱 Object‑Oriented Principles Demonstrated

The system is built entirely on OOP foundations:

### 🔒 Encapsulation
- All class attributes are **private** (using `__` prefix) and accessed only through `@property` decorators.
- Each setter includes validation logic (e.g., age range, contact length, blood group format).

### 🧬 Inheritance
- `Patient`, `Doctor`, and `Nurse` inherit from an abstract base class `Person`.
- Common attributes (name, age, gender, contact) and methods are reused.

### 🎭 Polymorphism
- The `Hospital` controller calls `display_info()` and `get_role()` on any `Person` subtype, and each subclass provides its own implementation.
- This allows treating all people uniformly while retaining specific behaviour.

### 📦 Abstraction
- `Person` is an abstract class with abstract methods `get_role()` and `display_info()`, forcing subclasses to implement them.
- `DatabaseManager` completely hides SQL complexity – all other classes interact only with its high‑level methods.

---

## 🛠️ Technology Stack

- **Python 3** – Core logic and OOP design.
- **SQLite3** – Lightweight embedded database (no external dependencies).
- **Standard Library Only** – No third‑party packages required.

---

## 📁 Project Structure

```
hospital_system/
├── __init__.py
├── main.py                         # Entry point
├── controllers/
│   ├── __init__.py
│   └── hospital.py                 # Central facade (Hospital class)
├── database/
│   ├── __init__.py
│   └── db_manager.py               # Database abstraction layer
├── models/
│   ├── __init__.py
│   ├── person.py                   # Abstract base class
│   ├── patient.py
│   ├── doctor.py
│   ├── nurse.py
│   ├── appointment.py
│   ├── prescription.py
│   ├── bill.py
│   └── room.py
└── ui/
    ├── __init__.py
    └── menu.py                     # Console menu system
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher (no additional libraries needed).

Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hospital-management-system.git
   cd hospital-management-system
   ```

2. Run the application:
   ```bash
   python hospital_system/main.py
   ```
   > The database file `hospital.db` will be automatically created in the project root.

First Use
- The system will create all necessary tables automatically.
- Navigate through the console menu using numbers.
- All data is saved persistently.
How to Use

After launching, you will see the main menu:
```
   ╔══════════════════════════════╗
   ║   HOSPITAL MANAGEMENT SYSTEM ║
   ╚══════════════════════════════╝

  Welcome to City General Hospital
  ────────────────────────────────────
  1. Patient Management
  2. Doctor Management
  3. Nurse Management
  4. Appointment Management
  5. Prescription Management
  6. Room Management
  7. Billing Management
  8. Search & Reports
  9. Exit
```
Select an option and follow the prompts. Every action is validated with clear error messages.
🧪 Example Workflow
1. Register a patient (gets a Patient ID).
2. Register a doctor (gets a Doctor ID).
3. Book an appointment between them.
4. Create a prescription with medicines.
5. Assign a room to the patient.
6. Generate a bill with items.
7. Mark the bill as paid.
All these steps are interconnected via foreign keys in the database.
🙏 Acknowledgements
I would like to express my sincere gratitude to Sir Fahad Quereshi for his invaluable guidance and support throughout this project. His emphasis on clean OOP design and best practices made this project a great learning experience.
 👨‍💻 Author
Waqas Ahmad – 4th Semester Student  
[GitHub Profile]() | [LinkedIn](www.linkedin.com/in/waqas-ahmad-578727286)

📄 License
This project is open‑source and available free. Feel free to use, modify, and distribute it.
## ⭐ Show Your Support
If you found this project helpful, please give it a ⭐ on GitHub!

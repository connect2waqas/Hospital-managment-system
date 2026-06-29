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
        print(f"\n  ✖  Fatal error: {exc}")
    except KeyboardInterrupt:
        print("\n\n  Session interrupted. Goodbye!")
    finally:
        db.close()


if __name__ == "__main__":
    main()

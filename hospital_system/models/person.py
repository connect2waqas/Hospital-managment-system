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
            f"  Name    : {self.name}\n"
            f"  Age     : {self.age}\n"
            f"  Gender  : {self.gender}\n"
            f"  Contact : {self.contact}"
        )

"""PawPal+ class skeleton generated from diagrams/uml_draft.mmd.

Class stubs only — no business logic implemented yet.
"""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass
class Pets:
    pet_id: str
    name: str
    species: str
    breed: str
    special_instructions: str = ""
    owner: Optional["Customer"] = None

    def add_record(self, record: dict) -> None:
        pass

    def update_record(self, record: dict) -> None:
        pass

    def delete_record(self, record_id: str) -> None:
        pass

    def set_special_instructions(self, text: str) -> None:
        pass


@dataclass
class Tasks:
    task_id: str
    type: str
    duration_minutes: int
    priority: str
    pet: Optional[Pets] = None

    def walk(self) -> None:
        pass

    def feed(self) -> None:
        pass

    def meds(self) -> None:
        pass

    def enrichment(self) -> None:
        pass

    def grooming(self) -> None:
        pass


class Customer:
    def __init__(self, customer_id: str, name: str, email: str, phone: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.pets: List[Pets] = []

    def add_task(self, task: Tasks) -> None:
        pass

    def update_task(self, task: Tasks) -> None:
        pass

    def delete_task(self, task_id: str) -> None:
        pass

    def add_user_info(self, info: dict) -> None:
        pass

    def update_user_info(self, info: dict) -> None:
        pass

    def delete_user_info(self, field: str) -> None:
        pass

    def assign_pet(self, pet: Pets) -> None:
        pass


class Plan:
    def __init__(self, plan_id: str, plan_date: date, customer: Customer):
        self.plan_id = plan_id
        self.date = plan_date
        self.customer = customer
        self.scheduled_tasks: List[Tasks] = []

    def book_plan(self) -> None:
        pass

    def update_plan(self, plan_id: str) -> None:
        pass

    def delete_plan(self, plan_id: str) -> None:
        pass

    def prioritize_tasks(self) -> None:
        pass

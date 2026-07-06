"""PawPal+ core classes, implemented from diagrams/uml_draft.mmd.

Task ownership lives on Pets (a pet "requires" its tasks). Customer aggregates
tasks across its pets rather than storing its own copy, and Plan pulls its
candidate task pool from Customer.get_all_tasks() rather than reaching into
Pets directly.
"""

from dataclasses import dataclass, field
from datetime import date, time
from typing import Dict, List, Optional

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Tasks:
    task_id: str
    description: str
    category: str  # e.g. "walk", "feeding", "meds", "enrichment", "grooming"
    scheduled_time: time
    frequency: str  # e.g. "once", "daily", "weekly"
    duration_minutes: int = 15
    priority: str = "medium"
    is_completed: bool = False
    pet: Optional["Pets"] = None

    def mark_complete(self) -> None:
        self.is_completed = True

    def mark_incomplete(self) -> None:
        self.is_completed = False


@dataclass
class Pets:
    pet_id: str
    name: str
    species: str
    breed: str
    special_instructions: str = ""
    owner: Optional["Customer"] = None
    tasks: List[Tasks] = field(default_factory=list)

    def add_task(self, task: Tasks) -> None:
        task.pet = self
        self.tasks.append(task)

    def update_task(self, task_id: str, **updates) -> Optional[Tasks]:
        for task in self.tasks:
            if task.task_id == task_id:
                for key, value in updates.items():
                    setattr(task, key, value)
                return task
        return None

    def remove_task(self, task_id: str) -> None:
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def get_tasks(self) -> List[Tasks]:
        return self.tasks

    def set_special_instructions(self, text: str) -> None:
        self.special_instructions = text


class Customer:
    def __init__(self, customer_id: str, name: str, email: str, phone: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.pets: List[Pets] = []
        self.plans: List["Plan"] = []
        self.extra_info: Dict[str, str] = {}

    def add_pet(self, pet: Pets) -> None:
        pet.owner = self
        self.pets.append(pet)

    def assign_pet(self, pet: Pets) -> None:
        self.add_pet(pet)

    def get_pet(self, pet_id: str) -> Optional[Pets]:
        return next((p for p in self.pets if p.pet_id == pet_id), None)

    def add_task(self, pet_id: str, task: Tasks) -> None:
        pet = self.get_pet(pet_id)
        if pet is None:
            raise ValueError(f"No pet found with id {pet_id}")
        pet.add_task(task)

    def update_task(self, pet_id: str, task_id: str, **updates) -> Optional[Tasks]:
        pet = self.get_pet(pet_id)
        if pet is None:
            return None
        return pet.update_task(task_id, **updates)

    def delete_task(self, pet_id: str, task_id: str) -> None:
        pet = self.get_pet(pet_id)
        if pet is not None:
            pet.remove_task(task_id)

    def get_all_tasks(self) -> List[Tasks]:
        return [task for pet in self.pets for task in pet.tasks]

    def add_user_info(self, field: str, value: str) -> None:
        self.extra_info[field] = value

    def update_user_info(self, field: str, value: str) -> None:
        if field in ("name", "email", "phone"):
            setattr(self, field, value)
        else:
            self.extra_info[field] = value

    def delete_user_info(self, field: str) -> None:
        self.extra_info.pop(field, None)


class Plan:
    def __init__(self, plan_id: str, plan_date: date, customer: Customer):
        self.plan_id = plan_id
        self.date = plan_date
        self.customer = customer
        self.scheduled_tasks: List[Tasks] = []

    def gather_tasks(self) -> List[Tasks]:
        """Pull the candidate task pool from the owner's pets."""
        return self.customer.get_all_tasks()

    def prioritize_tasks(self) -> None:
        self.scheduled_tasks.sort(
            key=lambda t: (PRIORITY_ORDER.get(t.priority, len(PRIORITY_ORDER)), t.duration_minutes)
        )

    def book_plan(self) -> None:
        self.scheduled_tasks = [t for t in self.gather_tasks() if not t.is_completed]
        self.prioritize_tasks()
        if self not in self.customer.plans:
            self.customer.plans.append(self)

    def update_plan(self) -> None:
        self.book_plan()

    def delete_plan(self) -> None:
        self.scheduled_tasks = []
        if self in self.customer.plans:
            self.customer.plans.remove(self)

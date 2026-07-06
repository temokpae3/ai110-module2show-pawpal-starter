"""PawPal+ core classes, implemented from diagrams/uml_draft.mmd.

Task ownership lives on Pets (a pet "requires" its tasks). Customer aggregates
tasks across its pets rather than storing its own copy, and Plan pulls its
candidate task pool from Customer.get_all_tasks() rather than reaching into
Pets directly.
"""

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from itertools import combinations
from typing import Dict, List, Optional

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# How far to push scheduled_date forward when a recurring task is completed.
# "once" tasks have no entry here, so they simply don't recur.
FREQUENCY_INTERVALS = {
    "daily": timedelta(days=1),
    "weekly": timedelta(weeks=1),
}


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
    scheduled_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        self.is_completed = True
        self.spawn_next_occurrence()

    def mark_incomplete(self) -> None:
        self.is_completed = False

    def spawn_next_occurrence(self) -> Optional["Tasks"]:
        """If this is a recurring task, create+attach the next occurrence.

        Uses timedelta to push scheduled_date forward by one interval
        ("daily" -> +1 day, "weekly" -> +7 days) rather than reasoning about
        calendar rollovers (month/year boundaries) by hand.
        """
        interval = FREQUENCY_INTERVALS.get(self.frequency)
        if interval is None or self.pet is None:
            return None

        next_task = Tasks(
            task_id=uuid.uuid4().hex[:8],
            description=self.description,
            category=self.category,
            scheduled_time=self.scheduled_time,
            frequency=self.frequency,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            scheduled_date=self.scheduled_date + interval,
        )
        self.pet.add_task(next_task)
        return next_task


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
        self.conflicts: List[str] = []

    def gather_tasks(self) -> List[Tasks]:
        """Pull the candidate task pool from the owner's pets."""
        return self.customer.get_all_tasks()

    def prioritize_tasks(self) -> None:
        """Sort scheduled_tasks by priority (high first), then by duration.

        Duration is the tie-breaker so that, within the same priority tier,
        shorter tasks sort first.
        """
        self.scheduled_tasks.sort(
            key=lambda t: (PRIORITY_ORDER.get(t.priority, len(PRIORITY_ORDER)), t.duration_minutes)
        )

    def sort_by_time(self) -> List[Tasks]:
        """Sort scheduled_tasks chronologically by scheduled_time.

        `time` objects compare directly, so no parsing is needed here.
        """
        self.scheduled_tasks = sorted(self.scheduled_tasks, key=lambda t: t.scheduled_time)
        return self.scheduled_tasks

    def filter_tasks(self, is_completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Tasks]:
        """Return scheduled_tasks narrowed by completion status and/or pet name.

        Each filter is optional and independent: passing both ANDs them
        together, passing neither returns every scheduled task unchanged.
        """
        tasks = self.scheduled_tasks
        if is_completed is not None:
            tasks = [t for t in tasks if t.is_completed == is_completed]
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet is not None and t.pet.name == pet_name]
        return tasks

    def detect_conflicts(self) -> List[str]:
        """Flag overlapping task time windows without raising.

        Lightweight on purpose: compares every pair of scheduled tasks
        (fine since a single day's task list stays small) and returns
        human-readable warning strings instead of raising, so a scheduling
        clash never crashes the app -- the caller decides what to do with
        the warnings (display them, log them, etc).
        """
        warnings: List[str] = []

        def window(t: Tasks):
            start = datetime.combine(t.scheduled_date, t.scheduled_time)
            return start, start + timedelta(minutes=t.duration_minutes)

        for task_a, task_b in combinations(self.scheduled_tasks, 2):
            a_start, a_end = window(task_a)
            b_start, b_end = window(task_b)
            if a_start < b_end and b_start < a_end:
                pet_a = task_a.pet.name if task_a.pet else "Unknown pet"
                pet_b = task_b.pet.name if task_b.pet else "Unknown pet"
                warnings.append(
                    f"Conflict: '{task_a.description}' ({pet_a}, {task_a.scheduled_time.strftime('%H:%M')}) "
                    f"overlaps with '{task_b.description}' ({pet_b}, {task_b.scheduled_time.strftime('%H:%M')})"
                )
        return warnings

    def book_plan(self) -> None:
        self.scheduled_tasks = [t for t in self.gather_tasks() if not t.is_completed]
        self.prioritize_tasks()
        self.conflicts = self.detect_conflicts()
        if self not in self.customer.plans:
            self.customer.plans.append(self)

    def update_plan(self) -> None:
        self.book_plan()

    def delete_plan(self) -> None:
        self.scheduled_tasks = []
        if self in self.customer.plans:
            self.customer.plans.remove(self)

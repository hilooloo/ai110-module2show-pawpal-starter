from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: str          # "low", "medium", or "high"
    category: str          # e.g. "walk", "feeding", "meds", "grooming", "enrichment"
    is_recurring: bool = False
    notes: str = ""


@dataclass
class Pet:
    name: str
    species: str           # "dog", "cat", "other"
    breed: str = ""
    age: int = 0
    tasks: list[Task] = field(default_factory=list)


class Owner:
    def __init__(self, name: str, available_minutes: int, preferences: Optional[dict] = None):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or {}
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def add_task(self, pet: Pet, task: Task) -> None:
        pass

    def get_tasks(self, pet: Pet) -> list[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.schedule: list[dict] = []

    def sort_tasks_by_priority(self, tasks: list[Task]) -> list[Task]:
        pass

    def filter_tasks_by_time(self, tasks: list[Task], available_minutes: int) -> list[Task]:
        pass

    def generate_schedule(self) -> list[dict]:
        pass

    def explain_plan(self) -> str:
        pass

    def display_schedule(self) -> None:
        pass

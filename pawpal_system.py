from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    """Represents a single pet care task with a scheduled time and completion state."""

    description: str
    time_str: str        # e.g. "08:00", "12:30"
    frequency: str       # e.g. "daily", "weekly", "as-needed"
    is_completed: bool = False
    last_completed_date: Optional[date] = None

    def mark_complete(self) -> None:
        """Mark this task as completed and record today's date."""
        self.is_completed = True
        self.last_completed_date = date.today()

    def get_next_due_date(self) -> Optional[date]:
        """Return the next calendar date this task is due using timedelta, or None if frequency is 'as-needed'."""
        if self.frequency == "daily":
            return date.today() + timedelta(days=1)
        if self.frequency == "weekly":
            return date.today() + timedelta(weeks=1)
        return None

    def __str__(self) -> str:
        """Return a formatted one-line string representation of the task."""
        status = "done" if self.is_completed else "todo"
        return f"[{status}] {self.time_str} - {self.description} ({self.frequency})"


@dataclass
class Pet:
    """Represents a pet and its associated list of care tasks."""

    name: str
    species: str         # e.g. "dog", "cat", "other"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def __str__(self) -> str:
        """Return a formatted string with the pet's name and species."""
        return f"{self.name} ({self.species})"


class Owner:
    """Represents the pet owner who manages one or more pets."""

    def __init__(self, name: str):
        """Initialize the owner with a name and an empty pets list."""
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every (pet, task) pair across all owned pets."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]

    def __str__(self) -> str:
        """Return a formatted string listing the owner's name and pet names."""
        pet_names = ", ".join(p.name for p in self.pets) if self.pets else "none"
        return f"Owner: {self.name} | Pets: {pet_names}"


class Scheduler:
    """Brain of PawPal+: retrieves, organizes, and manages tasks across all of an Owner's pets."""

    def __init__(self, owner: Owner):
        """Initialize the scheduler with the owner whose pets will be scheduled."""
        self.owner = owner

    # ── retrieval ──────────────────────────────────────────────────────────

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return all (pet, task) pairs for every pet owned."""
        return self.owner.get_all_tasks()

    def get_pending_tasks(self) -> list[tuple[Pet, Task]]:
        """Return tasks that have not been completed yet."""
        return [(pet, task) for pet, task in self.get_all_tasks() if not task.is_completed]

    def get_completed_tasks(self) -> list[tuple[Pet, Task]]:
        """Return tasks that have already been marked complete."""
        return [(pet, task) for pet, task in self.get_all_tasks() if task.is_completed]

    def get_tasks_by_pet(self, pet: Pet) -> list[Task]:
        """Return all tasks belonging to a specific pet."""
        return list(pet.tasks)

    def get_tasks_by_frequency(self, frequency: str) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs filtered by frequency string."""
        return [
            (pet, task)
            for pet, task in self.get_all_tasks()
            if task.frequency.lower() == frequency.lower()
        ]

    # ── organization ───────────────────────────────────────────────────────

    def sort_by_time(self, pairs: Optional[list[tuple[Pet, Task]]] = None) -> list[tuple[Pet, Task]]:
        """Sort (pet, task) pairs by time_str ascending; strings not in 'HH:MM' format are sorted to the end."""
        if pairs is None:
            pairs = self.get_all_tasks()

        def _sort_key(pair: tuple[Pet, Task]) -> str:
            t = pair[1].time_str
            # Valid "HH:MM" strings sort correctly as strings; others go to end
            if len(t) == 5 and t[2] == ":" and t[:2].isdigit() and t[3:].isdigit():
                return t
            return "99:99"

        return sorted(pairs, key=_sort_key)

    def generate_schedule(self) -> list[tuple[Pet, Task]]:
        """Return all pending tasks sorted by scheduled time."""
        return self.sort_by_time(self.get_pending_tasks())

    def check_conflicts(self) -> list[str]:
        """Return a non-blocking warning string for each group of tasks that share the exact same time_str."""
        from collections import defaultdict
        time_map: dict[str, list[tuple[Pet, Task]]] = defaultdict(list)
        for pet, task in self.sort_by_time():
            time_map[task.time_str].append((pet, task))

        warnings = []
        for time_str, pairs in time_map.items():
            if len(pairs) > 1:
                names = ", ".join(f"{p.name}: '{t.description}'" for p, t in pairs)
                warnings.append(f"WARNING - Conflict at {time_str}: {names}")
        return warnings

    # ── management ─────────────────────────────────────────────────────────

    def mark_task_complete(self, task: Task) -> None:
        """Delegate completion marking to the given task."""
        task.mark_complete()

    def reset_daily_tasks(self) -> None:
        """Reset completion status for all tasks with frequency 'daily'."""
        for _, task in self.get_all_tasks():
            if task.frequency.lower() == "daily":
                task.is_completed = False

    # ── display ────────────────────────────────────────────────────────────

    def generate_summary(self) -> str:
        """Return a formatted daily plan grouped by pet; prepends any conflict warnings detected by check_conflicts()."""
        lines = []
        conflicts = self.check_conflicts()
        if conflicts:
            lines.append("*** SCHEDULING CONFLICTS DETECTED ***")
            for warning in conflicts:
                lines.append(f"  {warning}")
            lines.append("")

        lines += [f"Daily plan for {self.owner.name}'s pets", "=" * 40]

        total = len(self.get_all_tasks())
        done = len(self.get_completed_tasks())

        if total == 0:
            lines.append("No tasks found.")
            return "\n".join(lines)

        for pet in self.owner.pets:
            pending = [t for t in pet.tasks if not t.is_completed]
            if not pending:
                continue
            sorted_tasks = sorted(pending, key=lambda t: t.time_str)
            lines.append(f"\n{pet}:")
            for task in sorted_tasks:
                lines.append(f"  {task}")

        if done == total:
            lines.append("\nAll tasks complete!")
        else:
            lines.append(f"\nProgress: {done}/{total} tasks completed")

        return "\n".join(lines)

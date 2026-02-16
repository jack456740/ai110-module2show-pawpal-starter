"""
PawPal+ System Module
Core system integration for the pet care scheduling application.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional


# ============================================================================
# ENUMERATIONS
# ============================================================================

class Priority(Enum):
    """Task priority levels."""
    HIGH = 3
    MEDIUM = 2
    LOW = 1


class Category(Enum):
    """Task categories."""
    WALK = "walk"
    FEEDING = "feeding"
    MEDICATION = "medication"
    GROOMING = "grooming"
    ENRICHMENT = "enrichment"
    OTHER = "other"


class Frequency(Enum):
    """Task frequency."""
    DAILY = "daily"
    WEEKLY = "weekly"
    AS_NEEDED = "as-needed"


# ============================================================================
# DATACLASSES
# ============================================================================

@dataclass
class PetOwner:
    """Represents the human using the app."""
    name: str
    daily_available_time: int = 480  # minutes
    preferences: Dict = field(default_factory=dict)

    def update_available_time(self, minutes: int) -> None:
        """Update the owner's available time for pet care."""
        pass

    def update_preferences(self, preferences: Dict) -> None:
        """Update owner's preferences."""
        pass


@dataclass
class Pet:
    """Represents the pet receiving care."""
    name: str
    species: str
    age: int = 0
    special_needs: List[str] = field(default_factory=list)

    def update_special_needs(self, special_needs: List[str]) -> None:
        """Update the pet's special needs."""
        pass

    def add_special_need(self, need: str) -> None:
        """Add a single special need."""
        pass


@dataclass
class Task:
    """Represents a single pet care activity."""
    task_id: int
    name: str
    category: Category
    duration: int  # minutes
    priority: Priority
    frequency: Frequency = Frequency.DAILY

    def update_duration(self, duration: int) -> None:
        """Update task duration."""
        pass

    def update_priority(self, priority: Priority) -> None:
        """Update task priority."""
        pass

    def update_category(self, category: Category) -> None:
        """Update task category."""
        pass


@dataclass
class TaskManager:
    """Handles creation and storage of tasks."""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the manager."""
        pass

    def edit_task(self, task_id: int, updates: Dict) -> None:
        """Edit an existing task."""
        pass

    def remove_task(self, task_id: int) -> bool:
        """Remove a task by ID."""
        pass

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        pass

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        pass


@dataclass
class SchedulePlan:
    """Represents a generated daily plan."""
    scheduled_tasks: List[Task] = field(default_factory=list)
    unscheduled_tasks: List[Task] = field(default_factory=list)
    total_time_used: int = 0  # minutes

    def add_task(self, task: Task, scheduled: bool = True) -> None:
        """Add a task to the plan."""
        pass

    def calculate_total_time(self) -> int:
        """Calculate total time used by scheduled tasks."""
        pass

    def get_scheduled_tasks(self) -> List[Task]:
        """Get all scheduled tasks."""
        pass

    def get_unscheduled_tasks(self) -> List[Task]:
        """Get all unscheduled tasks."""
        pass

    def is_feasible(self, available_time: int) -> bool:
        """Check if the plan fits within available time."""
        pass


@dataclass
class Scheduler:
    """Applies logic to build a daily plan."""
    owner: PetOwner
    task_manager: TaskManager

    def generate_plan(self) -> SchedulePlan:
        """Generate a daily plan based on constraints and priorities."""
        pass

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (high to low)."""
        pass

    def filter_tasks_by_time(self, tasks: List[Task], available_time: int) -> List[Task]:
        """Filter tasks that fit within available time."""
        pass

    def explain_plan(self, plan: SchedulePlan) -> str:
        """Generate a human-readable explanation of the plan."""
        pass

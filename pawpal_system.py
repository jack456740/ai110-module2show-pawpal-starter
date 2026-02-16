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
    pets: List['Pet'] = field(default_factory=list)

    def update_available_time(self, minutes: int) -> None:
        """Update the owner's available time for pet care."""
        if minutes < 0:
            raise ValueError("Available time cannot be negative")
        self.daily_available_time = minutes

    def update_preferences(self, preferences: Dict) -> None:
        """Update owner's preferences."""
        self.preferences.update(preferences)

    def add_pet(self, pet: 'Pet') -> None:
        """Add a pet to the owner's household."""
        if pet not in self.pets:
            self.pets.append(pet)


@dataclass
class Pet:
    """Represents the pet receiving care."""
    name: str
    species: str
    pet_id: int = 0  # Unique identifier for the pet
    age: int = 0
    special_needs: List[str] = field(default_factory=list)

    def update_special_needs(self, special_needs: List[str]) -> None:
        """Update the pet's special needs."""
        self.special_needs = special_needs

    def add_special_need(self, need: str) -> None:
        """Add a single special need."""
        if need not in self.special_needs:
            self.special_needs.append(need)


@dataclass
class Task:
    """Represents a single pet care activity."""
    task_id: int
    name: str
    category: Category
    duration: int  # minutes
    priority: Priority
    pet_id: int
    frequency: Frequency = Frequency.DAILY

    def update_duration(self, duration: int) -> None:
        """Update task duration."""
        if duration <= 0:
            raise ValueError("Duration must be positive")
        self.duration = duration

    def update_priority(self, priority: Priority) -> None:
        """Update task priority."""
        self.priority = priority

    def update_category(self, category: Category) -> None:
        """Update task category."""
        self.category = category


@dataclass
class TaskManager:
    """Handles creation and storage of tasks."""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the manager."""
        self.tasks.append(task)

    def edit_task(self, task_id: int, updates: Dict) -> None:
        """Edit an existing task."""
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")
        
        # Update allowed fields
        if "name" in updates:
            task.name = updates["name"]
        if "category" in updates:
            task.category = updates["category"]
        if "duration" in updates:
            task.duration = updates["duration"]
        if "priority" in updates:
            task.priority = updates["priority"]
        if "frequency" in updates:
            task.frequency = updates["frequency"]
        if "pet_id" in updates:
            task.pet_id = updates["pet_id"]

    def remove_task(self, task_id: int) -> bool:
        """Remove a task by ID."""
        original_length = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        return len(self.tasks) < original_length

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return self.tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None


@dataclass
class SchedulePlan:
    """Represents a generated daily plan."""
    scheduled_tasks: List[Task] = field(default_factory=list)
    unscheduled_tasks: List[Task] = field(default_factory=list)
    total_time_used: int = 0  # minutes
    pet: Optional['Pet'] = None
    scheduled_times: Dict[int, str] = field(default_factory=dict)

    def add_task(self, task: Task, scheduled: bool = True) -> None:
        """Add a task to the plan."""
        if scheduled:
            self.scheduled_tasks.append(task)
        else:
            self.unscheduled_tasks.append(task)

    def calculate_total_time(self) -> int:
        """Calculate total time used by scheduled tasks."""
        self.total_time_used = sum(task.duration for task in self.scheduled_tasks)
        return self.total_time_used

    def get_scheduled_tasks(self) -> List[Task]:
        """Get all scheduled tasks."""
        return self.scheduled_tasks.copy()

    def get_unscheduled_tasks(self) -> List[Task]:
        """Get all unscheduled tasks."""
        return self.unscheduled_tasks.copy()

    def is_feasible(self, available_time: int) -> bool:
        """Check if the plan fits within available time."""
        return self.total_time_used <= available_time


@dataclass
class Scheduler:
    """Applies logic to build a daily plan."""
    owner: PetOwner
    task_manager: TaskManager

    def generate_plan(self, pet: 'Pet') -> SchedulePlan:
        """Generate a daily plan based on constraints and priorities for a specific pet."""
        plan = SchedulePlan(pet=pet)
        
        # Get all tasks from task manager
        all_tasks = self.task_manager.get_all_tasks()
        
        # Filter tasks for this specific pet and daily frequency
        pet_tasks = [t for t in all_tasks if t.pet_id == pet.pet_id and t.frequency == Frequency.DAILY]
        
        # Sort by priority (high to low)
        sorted_tasks = self.sort_tasks_by_priority(pet_tasks)
        
        # Greedily schedule tasks starting with highest priority
        remaining_time = self.owner.daily_available_time
        
        for task in sorted_tasks:
            if task.duration <= remaining_time:
                # Task fits - add to scheduled
                plan.add_task(task, scheduled=True)
                remaining_time -= task.duration
            else:
                # Task doesn't fit - add to unscheduled
                plan.add_task(task, scheduled=False)
        
        # Calculate total time used
        plan.calculate_total_time()
        return plan

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (high to low)."""
        return sorted(tasks, key=lambda t: t.priority.value, reverse=True)

    def filter_tasks_by_time(self, tasks: List[Task], available_time: int) -> List[Task]:
        """Filter tasks that fit within available time."""
        return [t for t in tasks if t.duration <= available_time]

    def filter_tasks_by_frequency(self, tasks: List[Task], frequency: Frequency) -> List[Task]:
        """Filter tasks by frequency (e.g., only daily tasks)."""
        return [t for t in tasks if t.frequency == frequency]

    def validate_plan(self, plan: SchedulePlan) -> bool:
        """Validate plan for conflicts, feasibility, and pet compatibility."""
        # Check if plan is feasible (fits within available time)
        if plan.total_time_used > self.owner.daily_available_time:
            return False
        # Check if all scheduled tasks belong to the correct pet
        if plan.pet:
            for task in plan.scheduled_tasks:
                if task.pet_id != plan.pet.pet_id:
                    return False
        return True

    def explain_plan(self, plan: SchedulePlan) -> str:
        """Generate a human-readable explanation of the plan."""
        lines = []
        
        # Header
        pet_name = plan.pet.name if plan.pet else "Unknown Pet"
        owner_name = self.owner.name
        lines.append(f"📅 Daily Care Plan for {pet_name} (Owner: {owner_name})")
        lines.append(f"   Available time: {self.owner.daily_available_time} minutes")
        lines.append("")
        
        # Scheduled tasks section
        if plan.scheduled_tasks:
            lines.append("✅ SCHEDULED TASKS:")
            cumulative_time = 0
            for i, task in enumerate(plan.scheduled_tasks, 1):
                start_time = cumulative_time
                end_time = cumulative_time + task.duration
                priority_emoji = "🔴" if task.priority == Priority.HIGH else "🟡" if task.priority == Priority.MEDIUM else "🟢"
                lines.append(f"   {i}. {priority_emoji} {task.name} ({task.duration}min) [{start_time}-{end_time}min]")
                cumulative_time += task.duration
            lines.append("")
            lines.append(f"   Total scheduled: {plan.total_time_used}/{self.owner.daily_available_time} minutes")
            remaining = self.owner.daily_available_time - plan.total_time_used
            if remaining > 0:
                lines.append(f"   Remaining free time: {remaining} minutes")
            lines.append("")
        else:
            lines.append("✅ SCHEDULED TASKS: None")
            lines.append("")
        
        # Unscheduled tasks section
        if plan.unscheduled_tasks:
            lines.append("⚠️  COULD NOT FIT (Lower Priority / Not Enough Time):")
            for task in plan.unscheduled_tasks:
                priority_emoji = "🔴" if task.priority == Priority.HIGH else "🟡" if task.priority == Priority.MEDIUM else "🟢"
                reason = "insufficient time" if self.owner.daily_available_time - plan.total_time_used < task.duration else "lower priority"
                lines.append(f"   • {priority_emoji} {task.name} ({task.duration}min) — {reason}")
        else:
            lines.append("⚠️  COULD NOT FIT: All tasks scheduled!")
        
        lines.append("")
        lines.append("📌 Scheduling logic: Tasks prioritized by urgency (HIGH→MEDIUM→LOW).")
        lines.append("   Only daily tasks included. Tasks fit greedily in order of priority.")
        
        return "\n".join(lines)

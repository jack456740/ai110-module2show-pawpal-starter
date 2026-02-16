import pytest
from pawpal_system import (
    PetOwner,
    Pet,
    Task,
    TaskManager,
    Scheduler,
    Priority,
    Category,
    Frequency,
)


def test_task_manager_add_remove_get():
    tm = TaskManager()
    t = Task(task_id=1, name="Feed", category=Category.FEEDING, duration=10, priority=Priority.HIGH, pet_id=1, frequency=Frequency.DAILY)
    tm.add_task(t)
    assert tm.get_task_by_id(1) is t
    assert len(tm.get_all_tasks()) == 1
    assert tm.remove_task(1) is True
    assert tm.get_task_by_id(1) is None


def test_task_update_duration_invalid():
    t = Task(task_id=99, name="X", category=Category.OTHER, duration=5, priority=Priority.LOW, pet_id=1, frequency=Frequency.DAILY)
    with pytest.raises(ValueError):
        t.update_duration(0)


def test_scheduler_generate_plan_per_pet():
    owner = PetOwner("Sam", daily_available_time=60)
    pet = Pet("Rex", "dog", pet_id=1)
    owner.add_pet(pet)

    tm = TaskManager()
    tm.add_task(Task(task_id=1, name="Walk", category=Category.WALK, duration=30, priority=Priority.HIGH, pet_id=1, frequency=Frequency.DAILY))
    tm.add_task(Task(task_id=2, name="Play", category=Category.ENRICHMENT, duration=40, priority=Priority.MEDIUM, pet_id=1, frequency=Frequency.DAILY))

    scheduler = Scheduler(owner=owner, task_manager=tm)
    plan = scheduler.generate_plan(pet)

    # High-priority short task should be scheduled
    assert any(t.task_id == 1 for t in plan.scheduled_tasks)
    # Longer task should be unscheduled due to time limit
    assert any(t.task_id == 2 for t in plan.unscheduled_tasks)
    # total_time_used should reflect scheduled tasks
    assert plan.total_time_used == sum(t.duration for t in plan.scheduled_tasks)


def test_explain_plan_contains_info():
    owner = PetOwner("Sam", daily_available_time=100)
    pet = Pet("Kit", "cat", pet_id=2)
    owner.add_pet(pet)
    tm = TaskManager()
    tm.add_task(Task(task_id=3, name="Feed", category=Category.FEEDING, duration=10, priority=Priority.HIGH, pet_id=2, frequency=Frequency.DAILY))

    scheduler = Scheduler(owner=owner, task_manager=tm)
    plan = scheduler.generate_plan(pet)
    explanation = scheduler.explain_plan(plan)

    assert pet.name in explanation
    assert "SCHEDULED" in explanation or "Scheduled" in explanation or "Scheduled" in explanation


def test_plan_feasibility():
    owner = PetOwner("Sam", daily_available_time=20)
    pet = Pet("Tiny", "bird", pet_id=3)
    owner.add_pet(pet)
    tm = TaskManager()
    tm.add_task(Task(task_id=4, name="Feed", category=Category.FEEDING, duration=10, priority=Priority.HIGH, pet_id=3, frequency=Frequency.DAILY))
    tm.add_task(Task(task_id=5, name="Song", category=Category.ENRICHMENT, duration=15, priority=Priority.MEDIUM, pet_id=3, frequency=Frequency.DAILY))

    scheduler = Scheduler(owner=owner, task_manager=tm)
    plan = scheduler.generate_plan(pet)

    assert plan.is_feasible(owner.daily_available_time) == (plan.total_time_used <= owner.daily_available_time)

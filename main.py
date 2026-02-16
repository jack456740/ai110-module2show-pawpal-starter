"""
PawPal+ Main Script
Simple demonstration of the pet care scheduling system.
"""

from datetime import datetime
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


def main():
    # Build sample data
    owner = PetOwner(name="Alex", daily_available_time=150)

    pet1 = Pet(name="Mochi", species="dog", pet_id=1, age=3)
    pet2 = Pet(name="Neko", species="cat", pet_id=2, age=2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    tm = TaskManager()
    tm.add_task(Task(task_id=1, name="Morning Walk", category=Category.WALK, duration=30, priority=Priority.HIGH, pet_id=1, frequency=Frequency.DAILY))
    tm.add_task(Task(task_id=2, name="Feed Mochi", category=Category.FEEDING, duration=10, priority=Priority.HIGH, pet_id=1, frequency=Frequency.DAILY))
    tm.add_task(Task(task_id=3, name="Play with Neko", category=Category.ENRICHMENT, duration=20, priority=Priority.MEDIUM, pet_id=2, frequency=Frequency.DAILY))
    tm.add_task(Task(task_id=4, name="Neko Feeding", category=Category.FEEDING, duration=10, priority=Priority.HIGH, pet_id=2, frequency=Frequency.DAILY))
    tm.add_task(Task(task_id=5, name="Evening Walk", category=Category.WALK, duration=25, priority=Priority.MEDIUM, pet_id=1, frequency=Frequency.DAILY))

    scheduler = Scheduler(owner=owner, task_manager=tm)

    # Header
    now = datetime.now().strftime("%Y-%m-%d")
    print("=" * 72)
    print(f" PawPal+ — Today's Schedule ({now})")
    print("=" * 72)
    print()

    # Per-pet sections
    for pet in owner.pets:
        print(f"{pet.name} ({pet.species}) — Pet ID: {pet.pet_id}")
        print("-" * 72)
        plan = scheduler.generate_plan(pet)
        # Use human-readable explanation from Scheduler
        explanation = scheduler.explain_plan(plan)
        print(explanation)
        print()

    # Footer summary
    print("=" * 72)
    print(f"Owner: {owner.name} — Available time: {owner.daily_available_time} minutes")
    print("=" * 72)


if __name__ == "__main__":
    main()

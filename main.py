"""
PawPal+ Main Script
Simple demonstration of the pet care scheduling system.
"""

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
    """Run the PawPal+ scheduling system."""
    
    # Create a PetOwner
    owner = PetOwner(name="Sarah", daily_available_time=180)  # 3 hours
    print(f"Owner: {owner.name}")
    print()
    
    # Create two Pet objects and add to owner
    pet1 = Pet(name="Buddy", species="dog", pet_id=1, age=5)
    pet2 = Pet(name="Whiskers", species="cat", pet_id=2, age=3)
    
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    print(f"Pets: {[pet.name for pet in owner.pets]}")
    print()
    
    # Create TaskManager and add tasks
    task_manager = TaskManager()
    
    # Create at least three Task objects with different durations
    task1 = Task(
        task_id=1,
        name="Dog Walk",
        category=Category.WALK,
        duration=30,
        priority=Priority.HIGH,
        pet_id=1,
        frequency=Frequency.DAILY,
    )
    
    task2 = Task(
        task_id=2,
        name="Dog Feeding",
        category=Category.FEEDING,
        duration=15,
        priority=Priority.HIGH,
        pet_id=1,
        frequency=Frequency.DAILY,
    )
    
    task3 = Task(
        task_id=3,
        name="Cat Litter Box",
        category=Category.ENRICHMENT,
        duration=10,
        priority=Priority.MEDIUM,
        pet_id=2,
        frequency=Frequency.DAILY,
    )
    
    task4 = Task(
        task_id=4,
        name="Cat Feeding",
        category=Category.FEEDING,
        duration=10,
        priority=Priority.HIGH,
        pet_id=2,
        frequency=Frequency.DAILY,
    )
    
    task5 = Task(
        task_id=5,
        name="Dog Playtime",
        category=Category.ENRICHMENT,
        duration=20,
        priority=Priority.MEDIUM,
        pet_id=1,
        frequency=Frequency.DAILY,
    )
    
    # Add tasks using TaskManager
    task_manager.add_task(task1)
    task_manager.add_task(task2)
    task_manager.add_task(task3)
    task_manager.add_task(task4)
    task_manager.add_task(task5)
    
    # Create Scheduler and generate plans for each pet
    scheduler = Scheduler(owner=owner, task_manager=task_manager)
    
    print("=" * 60)
    print("TODAY'S SCHEDULE")
    print("=" * 60)
    print()
    
    # Generate plan for Buddy (dog)
    buddy_plan = scheduler.generate_plan(pet1)
    print(f"🐕 {pet1.name}'s Schedule:")
    print(f"   Scheduled: {len(buddy_plan.scheduled_tasks)} tasks")
    for i, task in enumerate(buddy_plan.scheduled_tasks, 1):
        print(f"      {i}. {task.name} ({task.duration} min)")
    print(f"   Total time: {buddy_plan.total_time_used} minutes")
    print()
    
    # Generate plan for Whiskers (cat)
    whiskers_plan = scheduler.generate_plan(pet2)
    print(f"🐱 {pet2.name}'s Schedule:")
    print(f"   Scheduled: {len(whiskers_plan.scheduled_tasks)} tasks")
    for i, task in enumerate(whiskers_plan.scheduled_tasks, 1):
        print(f"      {i}. {task.name} ({task.duration} min)")
    print(f"   Total time: {whiskers_plan.total_time_used} minutes")
    print()
    
    print("=" * 60)
    print(f"Summary: {owner.daily_available_time} minutes available")
    print("=" * 60)


if __name__ == "__main__":
    main()

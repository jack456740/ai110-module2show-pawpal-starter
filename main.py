"""
PawPal+ Main Demo
Example usage of the PawPal+ scheduling system.
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
    """Run a demo of the PawPal+ scheduling system."""
    
    print("=" * 70)
    print("🐾 PawPal+ Pet Care Scheduling Demo")
    print("=" * 70)
    print()
    
    # ========================================================================
    # 1. Create a Pet Owner
    # ========================================================================
    owner = PetOwner(name="Jordan", daily_available_time=120)  # 2 hours
    print(f"Owner created: {owner.name} with {owner.daily_available_time} minutes available")
    print()
    
    # ========================================================================
    # 2. Create a Pet
    # ========================================================================
    mochi = Pet(name="Mochi", species="dog", pet_id=1, age=3)
    mochi.add_special_need("arthritis - avoid stairs")
    print(f"Pet created: {mochi.name} ({mochi.species}), age {mochi.age}")
    print(f"Special needs: {mochi.special_needs}")
    print()
    
    # ========================================================================
    # 3. Add pet to owner
    # ========================================================================
    owner.add_pet(mochi)
    print(f"✅ Mochi added to {owner.name}'s household")
    print()
    
    # ========================================================================
    # 4. Create a TaskManager and add tasks
    # ========================================================================
    task_manager = TaskManager()
    
    # Create sample tasks for Mochi
    tasks = [
        Task(
            task_id=1,
            name="Morning Walk",
            category=Category.WALK,
            duration=30,
            priority=Priority.HIGH,
            pet_id=1,
            frequency=Frequency.DAILY,
        ),
        Task(
            task_id=2,
            name="Feeding (Breakfast)",
            category=Category.FEEDING,
            duration=10,
            priority=Priority.HIGH,
            pet_id=1,
            frequency=Frequency.DAILY,
        ),
        Task(
            task_id=3,
            name="Arthritis Medication",
            category=Category.MEDICATION,
            duration=5,
            priority=Priority.HIGH,
            pet_id=1,
            frequency=Frequency.DAILY,
        ),
        Task(
            task_id=4,
            name="Feeding (Dinner)",
            category=Category.FEEDING,
            duration=10,
            priority=Priority.MEDIUM,
            pet_id=1,
            frequency=Frequency.DAILY,
        ),
        Task(
            task_id=5,
            name="Afternoon Play",
            category=Category.ENRICHMENT,
            duration=30,
            priority=Priority.MEDIUM,
            pet_id=1,
            frequency=Frequency.DAILY,
        ),
        Task(
            task_id=6,
            name="Evening Walk",
            category=Category.WALK,
            duration=20,
            priority=Priority.MEDIUM,
            pet_id=1,
            frequency=Frequency.DAILY,
        ),
        Task(
            task_id=7,
            name="Grooming",
            category=Category.GROOMING,
            duration=25,
            priority=Priority.LOW,
            pet_id=1,
            frequency=Frequency.DAILY,
        ),
    ]
    
    for task in tasks:
        task_manager.add_task(task)
    
    print(f"Tasks created and added: {len(task_manager.get_all_tasks())} total tasks")
    for task in task_manager.get_all_tasks():
        print(f"  • {task.name} ({task.duration}min, {task.priority.name})")
    print()
    
    # ========================================================================
    # 5. Create Scheduler and generate plan
    # ========================================================================
    scheduler = Scheduler(owner=owner, task_manager=task_manager)
    print("📋 Generating daily schedule...")
    print()
    
    plan = scheduler.generate_plan(mochi)
    
    # ========================================================================
    # 6. Validate and explain the plan
    # ========================================================================
    is_valid = scheduler.validate_plan(plan)
    print(f"Plan validation: {'✅ VALID' if is_valid else '❌ INVALID'}")
    print()
    
    # Get the explanation
    explanation = scheduler.explain_plan(plan)
    print(explanation)
    print()
    
    # ========================================================================
    # 7. Show plan summary
    # ========================================================================
    print("=" * 70)
    print("📊 Plan Summary")
    print("=" * 70)
    print(f"Scheduled tasks: {len(plan.scheduled_tasks)}")
    print(f"Unscheduled tasks: {len(plan.unscheduled_tasks)}")
    print(f"Total time used: {plan.total_time_used} minutes")
    print(f"Available time: {owner.daily_available_time} minutes")
    print(f"Feasible: {plan.is_feasible(owner.daily_available_time)}")
    print()


if __name__ == "__main__":
    main()

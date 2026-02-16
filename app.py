import streamlit as st

# Backend models
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

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- Minimal wiring to backend models in session state ---
st.subheader("Quick Demo — Backend Wiring")

# Initialize or reuse backend objects in session state
owner_name = st.text_input("Owner name", value="Jordan")
if 'owner' not in st.session_state:
    st.session_state['owner'] = PetOwner(name=owner_name, daily_available_time=150)
if 'task_manager' not in st.session_state:
    st.session_state['task_manager'] = TaskManager()
if 'scheduler' not in st.session_state:
    st.session_state['scheduler'] = Scheduler(owner=st.session_state['owner'], task_manager=st.session_state['task_manager'])

owner = st.session_state['owner']
tm = st.session_state['task_manager']
scheduler = st.session_state['scheduler']

st.markdown("### Add a Pet")
with st.form("add_pet"):
    pet_name = st.text_input("Name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, value=1)
    submitted = st.form_submit_button("Add pet")
    if submitted:
        pet_id = max([p.pet_id for p in owner.pets], default=0) + 1
        new_pet = Pet(name=pet_name, species=species, pet_id=pet_id, age=age)
        owner.add_pet(new_pet)                      # uses PetOwner.add_pet()
        # update scheduler reference
        st.session_state['scheduler'] = Scheduler(owner=owner, task_manager=tm)
        st.success(f"Added pet {new_pet.name}")
        st.experimental_rerun()

st.markdown("### Add a Task")
with st.form("add_task"):
    if not owner.pets:
        st.info("Add a pet first.")
    else:
        pet_options = {p.pet_id: p.name for p in owner.pets}
        pet_choice = st.selectbox("Pet", options=list(pet_options.keys()), format_func=lambda pid: pet_options[pid])
        task_name = st.text_input("Task name")
        duration = st.number_input("Duration (minutes)", min_value=1, value=10)
        priority = st.selectbox("Priority", [Priority.HIGH, Priority.MEDIUM, Priority.LOW], format_func=lambda p: p.name)
        category = st.selectbox("Category", [Category.FEEDING, Category.WALK, Category.ENRICHMENT], format_func=lambda c: c.name)
        frequency = st.selectbox("Frequency", [Frequency.DAILY], format_func=lambda f: f.name)
        submitted = st.form_submit_button("Add task")
        if submitted:
            next_id = max([t.task_id for t in tm.get_all_tasks()], default=0) + 1
            task = Task(task_id=next_id, name=task_name, category=category, duration=int(duration), priority=priority, pet_id=pet_choice, frequency=frequency)
            tm.add_task(task)                          # uses TaskManager.add_task()
            st.success(f"Added task '{task_name}' for {pet_options[pet_choice]}")
            st.experimental_rerun()

st.divider()

st.subheader("Tasks")
for t in tm.get_all_tasks():
    st.write(f"{t.task_id}: {t.name} — {t.duration} min — Pet {t.pet_id} — {t.priority.name}")

st.divider()

st.subheader("Per-Pet Schedules")
for pet in owner.pets:
    st.write(f"### {pet.name} ({pet.species})")
    plan = scheduler.generate_plan(pet)             # generate schedule after changes
    st.text(scheduler.explain_plan(plan))           # human-readable explanation

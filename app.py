from datetime import time

import streamlit as st
from pawpal_system import Customer, Pets, Tasks, Plan

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

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")

# Streamlit reruns this whole script on every interaction, so without this
# check a brand-new Customer (and a fresh, empty pets/tasks list) would
# replace the existing one on every rerun. Check the session_state "vault"
# first and only create a Customer the first time.
if "customer" not in st.session_state:
    st.session_state.customer = Customer(customer_id="c1", name=owner_name, email="", phone="")
    st.caption("Created a new Customer for this session.")
else:
    st.session_state.customer.name = owner_name
    st.caption(f"Reusing existing Customer from session_state (id={st.session_state.customer.customer_id}).")

customer = st.session_state.customer

st.markdown("### Add a Pet")

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
breed = st.text_input("Breed", value="")
special_instructions = st.text_area(
    "Special instructions", value="", placeholder="e.g. Feed wet food only"
)

if st.button("Add pet"):
    new_pet = Pets(
        pet_id=f"p{len(customer.pets) + 1}",
        name=pet_name,
        species=species,
        breed=breed,
        special_instructions=special_instructions,
    )
    customer.add_pet(new_pet)

if customer.pets:
    st.write("Current pets:")
    st.table(
        [
            {"name": p.name, "species": p.species, "breed": p.breed, "tasks": len(p.tasks)}
            for p in customer.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Schedule a Task")
st.caption("Tasks are added directly to the selected pet via Customer.add_task().")

if not customer.pets:
    st.info("Add a pet above before scheduling a task.")
else:
    pet_ids_by_name = {p.name: p.pet_id for p in customer.pets}

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_pet_name = st.selectbox("Pet", list(pet_ids_by_name.keys()))
    with col2:
        category = st.selectbox("Category", ["walk", "feeding", "meds", "enrichment", "grooming"])
    with col3:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    col4, col5, col6 = st.columns(3)
    with col4:
        task_description = st.text_input("Task description", value="Morning walk")
    with col5:
        scheduled_time = st.time_input("Time", value=time(8, 0))
    with col6:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)

    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        new_task = Tasks(
            task_id=f"t{len(customer.get_all_tasks()) + 1}",
            description=task_description,
            category=category,
            scheduled_time=scheduled_time,
            frequency=frequency,
            duration_minutes=int(duration),
            priority=priority,
        )
        customer.add_task(pet_ids_by_name[selected_pet_name], new_task)

all_tasks = customer.get_all_tasks()
if all_tasks:
    st.write("Scheduled tasks:")
    st.table(
        [
            {
                "pet": t.pet.name if t.pet else "",
                "description": t.description,
                "category": t.category,
                "time": t.scheduled_time.strftime("%H:%M"),
                "frequency": t.frequency,
                "duration_minutes": t.duration_minutes,
                "priority": t.priority,
                "completed": t.is_completed,
            }
            for t in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add a pet, then add a task above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )

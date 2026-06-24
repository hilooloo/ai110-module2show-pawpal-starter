import streamlit as st

from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# ── Initialize session state once ─────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")

if "pets" not in st.session_state:
    st.session_state.pets = {}  # pet name → Pet object

# ── Section 1: Owner setup ────────────────────────────────────────────────
st.subheader("Owner")

owner_name = st.text_input("Owner name", value=st.session_state.owner.name)

if st.button("Save owner"):
    st.session_state.owner.name = owner_name
    st.success(f"Owner saved: {owner_name}")

st.divider()

# ── Section 2: Add a pet ──────────────────────────────────────────────────
st.subheader("Pets")

col1, col2 = st.columns(2)
with col1:
    new_pet_name = st.text_input("Pet name")
with col2:
    new_species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if not new_pet_name:
        st.warning("Please enter a pet name.")
    elif new_pet_name in st.session_state.pets:
        st.warning(f'"{new_pet_name}" is already registered.')
    else:
        pet = Pet(name=new_pet_name, species=new_species)
        st.session_state.pets[new_pet_name] = pet
        st.session_state.owner.add_pet(pet)
        st.success(f"Added {new_pet_name} ({new_species}).")

if st.session_state.pets:
    st.write("Registered pets:", ", ".join(st.session_state.pets.keys()))

st.divider()

# ── Section 3: Add a task ─────────────────────────────────────────────────
st.subheader("Tasks")

if not st.session_state.pets:
    st.info("Add at least one pet above before adding tasks.")
else:
    target_pet_name = st.selectbox("Assign task to", list(st.session_state.pets.keys()))

    col1, col2, col3 = st.columns(3)
    with col1:
        description = st.text_input("Task description", value="Morning walk")
    with col2:
        time_str = st.text_input("Time (HH:MM)", value="08:00")
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as-needed"])

    if st.button("Add task"):
        if not description:
            st.warning("Please enter a task description.")
        else:
            pet = st.session_state.pets[target_pet_name]
            pet.add_task(Task(description=description, time_str=time_str, frequency=frequency))
            st.success(f'Added "{description}" to {target_pet_name}.')

    # Show current tasks per pet
    all_pairs = st.session_state.owner.get_all_tasks()
    if all_pairs:
        rows = [
            {"Pet": pet.name, "Time": task.time_str, "Task": task.description,
             "Frequency": task.frequency, "Done": task.is_completed}
            for pet, task in all_pairs
        ]
        st.table(rows)

st.divider()

# ── Section 4: Generate schedule ──────────────────────────────────────────
st.subheader("Schedule")

if st.button("Generate schedule"):
    if not st.session_state.owner.name:
        st.warning("Please save an owner name first.")
    elif not st.session_state.pets:
        st.warning("Add at least one pet before generating a schedule.")
    else:
        scheduler = Scheduler(st.session_state.owner)
        st.text(scheduler.generate_summary())

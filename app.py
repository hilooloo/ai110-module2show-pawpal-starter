import streamlit as st
from datetime import time as dtime

from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("A smart daily care planner for your pets.")

# ── Session state ─────────────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")
if "pets" not in st.session_state:
    st.session_state.pets = {}  # pet name → Pet object

# ── Section 1: Owner ──────────────────────────────────────────────────────
st.subheader("Owner")

col_name, col_btn = st.columns([4, 1])
with col_name:
    owner_name = st.text_input(
        "Owner name",
        value=st.session_state.owner.name,
        placeholder="Enter your name",
        label_visibility="collapsed",
    )
with col_btn:
    if st.button("Save", use_container_width=True):
        if owner_name.strip():
            st.session_state.owner.name = owner_name.strip()
            st.success(f"Saved: {owner_name.strip()}")
        else:
            st.warning("Please enter a name.")

st.divider()

# ── Section 2: Pets ───────────────────────────────────────────────────────
st.subheader("Pets")

col_pet, col_species, col_add = st.columns([3, 2, 1])
with col_pet:
    new_pet_name = st.text_input(
        "Pet name", placeholder="e.g. Biscuit", label_visibility="collapsed"
    )
with col_species:
    new_species = st.selectbox(
        "Species", ["dog", "cat", "other"], label_visibility="collapsed"
    )
with col_add:
    if st.button("Add pet", use_container_width=True):
        name = new_pet_name.strip()
        if not name:
            st.warning("Please enter a pet name.")
        elif name in st.session_state.pets:
            st.warning(f'"{name}" is already registered.')
        else:
            pet = Pet(name=name, species=new_species)
            st.session_state.pets[name] = pet
            st.session_state.owner.add_pet(pet)
            st.success(f"Added {name} the {new_species}.")

if st.session_state.pets:
    metric_cols = st.columns(len(st.session_state.pets))
    for col, (_, pet) in zip(metric_cols, st.session_state.pets.items()):
        with col:
            st.metric(
                label=pet.species.capitalize(),
                value=pet.name,
                delta=f"{len(pet.tasks)} task(s)",
            )

st.divider()

# ── Section 3: Tasks ──────────────────────────────────────────────────────
st.subheader("Tasks")

if not st.session_state.pets:
    st.info("Add at least one pet above before adding tasks.")
else:
    # Task input form
    col_assign, col_desc = st.columns(2)
    with col_assign:
        target_pet_name = st.selectbox(
            "Assign task to", list(st.session_state.pets.keys())
        )
    with col_desc:
        description = st.text_input(
            "Task description", placeholder="e.g. Morning walk"
        )

    col_time, col_freq, col_add = st.columns([2, 2, 1])
    with col_time:
        # st.time_input always returns a datetime.time → strftime guarantees "HH:MM"
        task_time = st.time_input("Time", value=dtime(8, 0))
        time_str = task_time.strftime("%H:%M")
    with col_freq:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as-needed"])
    with col_add:
        st.write("")  # vertical alignment nudge
        if st.button("Add task", use_container_width=True):
            if not description.strip():
                st.warning("Please enter a task description.")
            else:
                pet = st.session_state.pets[target_pet_name]
                pet.add_task(
                    Task(
                        description=description.strip(),
                        time_str=time_str,
                        frequency=frequency,
                    )
                )
                st.success(f'Added "{description.strip()}" to {target_pet_name}.')

    # Task table — sorted by time via Scheduler.sort_by_time()
    all_pairs = st.session_state.owner.get_all_tasks()
    if all_pairs:
        scheduler = Scheduler(st.session_state.owner)

        conflicts = scheduler.check_conflicts()
        if conflicts:
            for conflict in conflicts:
                st.warning(f"⚠️ {conflict}")

        sorted_pairs = scheduler.sort_by_time()
        st.caption(f"{len(sorted_pairs)} task(s) across all pets — sorted chronologically")
        st.table(
            [
                {
                    "Time": task.time_str,
                    "Pet": pet.name,
                    "Task": task.description,
                    "Frequency": task.frequency,
                    "Status": "done" if task.is_completed else "pending",
                }
                for pet, task in sorted_pairs
            ]
        )
    else:
        st.caption("No tasks added yet.")

st.divider()

# ── Section 4: Daily Schedule ─────────────────────────────────────────────
st.subheader("Daily Schedule")

if st.button("Generate schedule", type="primary", use_container_width=True):
    if not st.session_state.owner.name.strip():
        st.warning("Please save an owner name before generating a schedule.")
    elif not st.session_state.pets:
        st.warning("Add at least one pet before generating a schedule.")
    else:
        scheduler = Scheduler(st.session_state.owner)

        # ── Progress metrics ──────────────────────────────────────────────
        all_pairs      = scheduler.get_all_tasks()
        pending_pairs  = scheduler.get_pending_tasks()
        completed_pairs = scheduler.get_completed_tasks()

        col_total, col_pending, col_done = st.columns(3)
        col_total.metric("Total tasks",  len(all_pairs))
        col_pending.metric("Pending",    len(pending_pairs))
        col_done.metric("Completed",     len(completed_pairs))

        # ── Schedule table (Scheduler.sort_by_time() on pending only) ────
        if not pending_pairs:
            st.success("All tasks complete for today — great job!")
        else:
            sorted_pending = scheduler.sort_by_time(pending_pairs)
            st.caption(
                f"Today's plan for {st.session_state.owner.name} "
                f"— {len(sorted_pending)} task(s) remaining"
            )
            st.table(
                [
                    {
                        "Time": task.time_str,
                        "Pet": pet.name,
                        "Task": task.description,
                        "Frequency": task.frequency,
                        "Next due": str(task.get_next_due_date())
                        if task.get_next_due_date()
                        else "as-needed",
                    }
                    for pet, task in sorted_pending
                ]
            )

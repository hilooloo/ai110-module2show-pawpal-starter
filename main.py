from pawpal_system import Task, Pet, Owner, Scheduler

# ── Setup ──────────────────────────────────────────────────────────────────

owner = Owner(name="Jordan")

dog = Pet(name="Biscuit", species="dog")
cat = Pet(name="Mochi", species="cat")

# ── Tasks added intentionally OUT OF ORDER to test sorting ─────────────────

dog.add_task(Task(description="Evening walk",    time_str="19:00", frequency="daily"))
dog.add_task(Task(description="Morning walk",    time_str="07:30", frequency="daily"))
dog.add_task(Task(description="Flea medication", time_str="14:00", frequency="weekly"))
dog.add_task(Task(description="Afternoon treat", time_str="08:30", frequency="daily"))   # intentional conflict

cat.add_task(Task(description="Dinner feeding",  time_str="19:30", frequency="daily"))
cat.add_task(Task(description="Playtime",        time_str="14:30", frequency="daily"))
cat.add_task(Task(description="Breakfast",       time_str="08:30", frequency="daily"))   # intentional conflict

owner.add_pet(dog)
owner.add_pet(cat)

# ── Mark one task complete to test status filtering ────────────────────────

dog.tasks[1].mark_complete()  # Morning walk → done

scheduler = Scheduler(owner)

# ── Test 1: Full schedule (all tasks, sorted) ──────────────────────────────

print("=" * 50)
print("TEST 1: generate_summary() - pending tasks by pet")
print("=" * 50)
print(scheduler.generate_summary())

# ── Test 2: sort_by_time() across all pets ─────────────────────────────────

print("\n" + "=" * 50)
print("TEST 2: sort_by_time() - all tasks, time-sorted")
print("=" * 50)
for pet, task in scheduler.sort_by_time():
    print(f"  {task.time_str}  [{pet.name}]  {task.description}")

# ── Test 3: get_pending_tasks() - only incomplete ──────────────────────────

print("\n" + "=" * 50)
print("TEST 3: get_pending_tasks() - incomplete only")
print("=" * 50)
for pet, task in scheduler.get_pending_tasks():
    print(f"  {pet.name}: {task.description} ({task.time_str})")

# ── Test 4: get_completed_tasks() - only done ─────────────────────────────

print("\n" + "=" * 50)
print("TEST 4: get_completed_tasks() - completed only")
print("=" * 50)
completed = scheduler.get_completed_tasks()
if completed:
    for pet, task in completed:
        print(f"  {pet.name}: {task.description} ({task.time_str})")
else:
    print("  None completed yet.")

# ── Test 5: get_tasks_by_pet() - single pet ───────────────────────────────

print("\n" + "=" * 50)
print("TEST 5: get_tasks_by_pet(dog) - Biscuit only")
print("=" * 50)
for task in scheduler.get_tasks_by_pet(dog):
    status = "done" if task.is_completed else "todo"
    print(f"  [{status}] {task.time_str}  {task.description}")

# ── Test 6: get_tasks_by_frequency() - weekly only ────────────────────────

print("\n" + "=" * 50)
print("TEST 6: get_tasks_by_frequency('weekly')")
print("=" * 50)
for pet, task in scheduler.get_tasks_by_frequency("weekly"):
    print(f"  {pet.name}: {task.description} ({task.time_str})")

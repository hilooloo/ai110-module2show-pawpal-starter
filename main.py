from pawpal_system import Task, Pet, Owner, Scheduler

# ── Setup ──────────────────────────────────────────────────────────────────

owner = Owner(name="Jordan")

dog = Pet(name="Biscuit", species="dog")
cat = Pet(name="Mochi", species="cat")

# ── Tasks for Biscuit (dog) ────────────────────────────────────────────────

dog.add_task(Task(description="Morning walk",    time_str="07:30", frequency="daily"))
dog.add_task(Task(description="Feeding",         time_str="08:00", frequency="daily"))
dog.add_task(Task(description="Flea medication", time_str="09:00", frequency="weekly"))

# ── Tasks for Mochi (cat) ─────────────────────────────────────────────────

cat.add_task(Task(description="Feeding",         time_str="08:30", frequency="daily"))
cat.add_task(Task(description="Litter box clean",time_str="18:00", frequency="daily"))

# ── Register pets with owner ──────────────────────────────────────────────

owner.add_pet(dog)
owner.add_pet(cat)

# ── Run scheduler ─────────────────────────────────────────────────────────

scheduler = Scheduler(owner)

print("Today's Schedule")
print(scheduler.generate_summary())

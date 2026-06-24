from datetime import date, timedelta

from pawpal_system import Task, Pet, Owner, Scheduler


# ── Helpers ───────────────────────────────────────────────────────────────

def make_scheduler(*pets: Pet) -> Scheduler:
    """Build an Owner with the given pets and return a Scheduler over it."""
    owner = Owner(name="Jordan")
    for pet in pets:
        owner.add_pet(pet)
    return Scheduler(owner)


def make_task(description="Task", time_str="08:00", frequency="daily") -> Task:
    return Task(description=description, time_str=time_str, frequency=frequency)


# ── Group 1: Task unit tests ───────────────────────────────────────────────

class TestTask:

    def test_default_is_not_completed(self):
        task = make_task()
        assert task.is_completed is False
        assert task.last_completed_date is None

    def test_mark_complete_sets_flag(self):
        task = make_task()
        task.mark_complete()
        assert task.is_completed is True

    def test_mark_complete_stamps_today(self):
        task = make_task()
        task.mark_complete()
        assert task.last_completed_date == date.today()

    def test_add_task_increases_pet_task_count(self):
        pet = Pet(name="Biscuit", species="dog")
        assert len(pet.tasks) == 0
        pet.add_task(make_task())
        assert len(pet.tasks) == 1


# ── Group 2: Recurrence logic ─────────────────────────────────────────────

class TestRecurrence:

    def test_next_due_daily(self):
        task = make_task(frequency="daily")
        assert task.get_next_due_date() == date.today() + timedelta(days=1)

    def test_next_due_weekly(self):
        task = make_task(frequency="weekly")
        assert task.get_next_due_date() == date.today() + timedelta(weeks=1)

    def test_next_due_as_needed_returns_none(self):
        task = make_task(frequency="as-needed")
        assert task.get_next_due_date() is None

    def test_reset_daily_tasks_only_resets_daily(self):
        dog = Pet(name="Biscuit", species="dog")
        daily_task  = make_task("Walk",  "07:30", "daily")
        weekly_task = make_task("Meds",  "09:00", "weekly")
        dog.add_task(daily_task)
        dog.add_task(weekly_task)
        daily_task.mark_complete()
        weekly_task.mark_complete()

        scheduler = make_scheduler(dog)
        scheduler.reset_daily_tasks()

        assert daily_task.is_completed is False
        assert weekly_task.is_completed is True


# ── Group 3: Sorting correctness ──────────────────────────────────────────

class TestSorting:

    def test_sort_chronological_order(self):
        dog = Pet(name="Biscuit", species="dog")
        dog.add_task(make_task("Dinner",   "19:00"))
        dog.add_task(make_task("Breakfast","07:30"))
        dog.add_task(make_task("Meds",     "14:00"))
        scheduler = make_scheduler(dog)

        times = [task.time_str for _, task in scheduler.sort_by_time()]
        assert times == ["07:30", "14:00", "19:00"]

    def test_sort_already_sorted_unchanged(self):
        dog = Pet(name="Biscuit", species="dog")
        dog.add_task(make_task("A", "07:00"))
        dog.add_task(make_task("B", "12:00"))
        dog.add_task(make_task("C", "18:00"))
        scheduler = make_scheduler(dog)

        times = [task.time_str for _, task in scheduler.sort_by_time()]
        assert times == ["07:00", "12:00", "18:00"]

    def test_sort_malformed_time_goes_last(self):
        dog = Pet(name="Biscuit", species="dog")
        dog.add_task(make_task("Walk",    "09:00"))
        dog.add_task(make_task("Anytime", "morning"))
        scheduler = make_scheduler(dog)

        pairs = scheduler.sort_by_time()
        assert pairs[-1][1].time_str == "morning"

    def test_sort_missing_leading_zero_goes_last(self):
        dog = Pet(name="Biscuit", species="dog")
        dog.add_task(make_task("Walk",  "09:00"))
        dog.add_task(make_task("Meds",  "8:00"))
        scheduler = make_scheduler(dog)

        pairs = scheduler.sort_by_time()
        assert pairs[-1][1].time_str == "8:00"

    def test_sort_cross_pet_interleaving(self):
        dog = Pet(name="Biscuit", species="dog")
        cat = Pet(name="Mochi",   species="cat")
        dog.add_task(make_task("Dog task", "09:00"))
        cat.add_task(make_task("Cat task", "07:30"))
        scheduler = make_scheduler(dog, cat)

        pairs = scheduler.sort_by_time()
        assert pairs[0][1].time_str == "07:30"
        assert pairs[0][0].name     == "Mochi"
        assert pairs[1][1].time_str == "09:00"
        assert pairs[1][0].name     == "Biscuit"


# ── Group 4: Filtering by status and pet ──────────────────────────────────

class TestFiltering:

    def test_get_pending_excludes_completed(self):
        dog = Pet(name="Biscuit", species="dog")
        t1 = make_task("Walk",    "07:30")
        t2 = make_task("Feeding", "08:00")
        dog.add_task(t1)
        dog.add_task(t2)
        t1.mark_complete()
        scheduler = make_scheduler(dog)

        pending_tasks = [t for _, t in scheduler.get_pending_tasks()]
        assert t2 in pending_tasks
        assert t1 not in pending_tasks

    def test_get_completed_returns_only_done(self):
        dog = Pet(name="Biscuit", species="dog")
        t1 = make_task("Walk",    "07:30")
        t2 = make_task("Feeding", "08:00")
        dog.add_task(t1)
        dog.add_task(t2)
        t1.mark_complete()
        scheduler = make_scheduler(dog)

        completed_tasks = [t for _, t in scheduler.get_completed_tasks()]
        assert t1 in completed_tasks
        assert t2 not in completed_tasks

    def test_get_tasks_by_pet_isolates_correctly(self):
        dog = Pet(name="Biscuit", species="dog")
        cat = Pet(name="Mochi",   species="cat")
        dog_task = make_task("Walk",      "07:30")
        cat_task = make_task("Cat snack", "08:30")
        dog.add_task(dog_task)
        cat.add_task(cat_task)
        scheduler = make_scheduler(dog, cat)

        assert dog_task in scheduler.get_tasks_by_pet(dog)
        assert cat_task not in scheduler.get_tasks_by_pet(dog)

    def test_get_tasks_by_frequency_daily(self):
        dog = Pet(name="Biscuit", species="dog")
        dog.add_task(make_task("Walk", "07:30", "daily"))
        dog.add_task(make_task("Meds", "09:00", "weekly"))
        scheduler = make_scheduler(dog)

        results = [t for _, t in scheduler.get_tasks_by_frequency("daily")]
        assert all(t.frequency == "daily" for t in results)
        assert len(results) == 1

    def test_get_tasks_by_frequency_case_insensitive(self):
        dog = Pet(name="Biscuit", species="dog")
        dog.add_task(make_task("Walk", "07:30", "Daily"))
        scheduler = make_scheduler(dog)

        assert len(scheduler.get_tasks_by_frequency("daily")) == 1


# ── Group 5: Conflict detection ───────────────────────────────────────────

class TestConflicts:

    def test_no_conflict_returns_empty(self):
        dog = Pet(name="Biscuit", species="dog")
        dog.add_task(make_task("Walk",    "07:30"))
        dog.add_task(make_task("Feeding", "08:00"))
        scheduler = make_scheduler(dog)

        assert scheduler.check_conflicts() == []

    def test_conflict_across_pets_detected(self):
        dog = Pet(name="Biscuit", species="dog")
        cat = Pet(name="Mochi",   species="cat")
        dog.add_task(make_task("Treat",     "08:30"))
        cat.add_task(make_task("Breakfast", "08:30"))
        scheduler = make_scheduler(dog, cat)

        assert len(scheduler.check_conflicts()) == 1

    def test_conflict_warning_contains_time(self):
        dog = Pet(name="Biscuit", species="dog")
        cat = Pet(name="Mochi",   species="cat")
        dog.add_task(make_task("Treat",     "08:30"))
        cat.add_task(make_task("Breakfast", "08:30"))
        scheduler = make_scheduler(dog, cat)

        assert "08:30" in scheduler.check_conflicts()[0]

    def test_conflict_warning_contains_both_pet_names(self):
        dog = Pet(name="Biscuit", species="dog")
        cat = Pet(name="Mochi",   species="cat")
        dog.add_task(make_task("Treat",     "08:30"))
        cat.add_task(make_task("Breakfast", "08:30"))
        scheduler = make_scheduler(dog, cat)

        warning = scheduler.check_conflicts()[0]
        assert "Biscuit" in warning
        assert "Mochi" in warning

    def test_conflict_same_pet_same_time(self):
        dog = Pet(name="Biscuit", species="dog")
        dog.add_task(make_task("Walk",    "08:00"))
        dog.add_task(make_task("Feeding", "08:00"))
        scheduler = make_scheduler(dog)

        assert len(scheduler.check_conflicts()) == 1

    def test_generate_summary_shows_conflict_header(self):
        dog = Pet(name="Biscuit", species="dog")
        cat = Pet(name="Mochi",   species="cat")
        dog.add_task(make_task("Treat",     "08:30"))
        cat.add_task(make_task("Breakfast", "08:30"))
        scheduler = make_scheduler(dog, cat)

        assert "*** SCHEDULING CONFLICTS DETECTED ***" in scheduler.generate_summary()

    def test_generate_summary_no_conflict_no_header(self):
        dog = Pet(name="Biscuit", species="dog")
        dog.add_task(make_task("Walk",    "07:30"))
        dog.add_task(make_task("Feeding", "09:00"))
        scheduler = make_scheduler(dog)

        assert "*** SCHEDULING CONFLICTS DETECTED ***" not in scheduler.generate_summary()


# ── Group 6: Edge cases and empty data ────────────────────────────────────

class TestEdgeCases:

    def test_pet_with_no_tasks_returns_empty(self):
        dog = Pet(name="Biscuit", species="dog")
        scheduler = make_scheduler(dog)

        assert scheduler.get_all_tasks() == []

    def test_owner_with_no_pets_returns_empty(self):
        scheduler = make_scheduler()
        assert scheduler.get_all_tasks() == []
        assert scheduler.get_pending_tasks() == []
        assert scheduler.check_conflicts() == []

    def test_generate_summary_no_tasks(self):
        dog = Pet(name="Biscuit", species="dog")
        scheduler = make_scheduler(dog)

        assert "No tasks found." in scheduler.generate_summary()

    def test_all_tasks_completed_shows_complete_message(self):
        dog = Pet(name="Biscuit", species="dog")
        t1 = make_task("Walk",    "07:30")
        t2 = make_task("Feeding", "08:00")
        dog.add_task(t1)
        dog.add_task(t2)
        t1.mark_complete()
        t2.mark_complete()
        scheduler = make_scheduler(dog)

        assert "All tasks complete!" in scheduler.generate_summary()

    def test_get_pending_returns_empty_when_all_done(self):
        dog = Pet(name="Biscuit", species="dog")
        task = make_task()
        dog.add_task(task)
        task.mark_complete()
        scheduler = make_scheduler(dog)

        assert scheduler.get_pending_tasks() == []

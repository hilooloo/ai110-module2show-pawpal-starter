# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

- **Chronological Sorting** — `Scheduler.sort_by_time()` orders all `(Pet, Task)` pairs by `time_str` in strict `HH:MM` ascending order. Malformed or non-standard time strings are automatically pushed to the end using a `"99:99"` sentinel, preventing silent sort failures.
- **Non-blocking Conflict Detection** — `Scheduler.check_conflicts()` scans all time-sorted tasks and flags any two or more tasks scheduled at the exact same time — across pets or on the same pet. Warnings are returned as plain strings and surfaced live in the Streamlit UI via `st.warning()` without stopping schedule generation.
- **Calendar Recurrence Logic** — `Task.get_next_due_date()` uses `datetime.timedelta` to compute when a task is next due: `+1 day` for `"daily"` tasks and `+7 days` for `"weekly"` tasks. `mark_complete()` simultaneously stamps `last_completed_date = date.today()` so recurrence tracking stays in sync automatically.
- **Status Filtering** — `Scheduler.get_pending_tasks()` and `Scheduler.get_completed_tasks()` filter live `Task` objects, so any call to `mark_complete()` is reflected immediately with no re-fetching.
- **Per-pet and Per-frequency Filtering** — `get_tasks_by_pet()` and `get_tasks_by_frequency()` return `(Pet, Task)` pairs so callers always know which pet each task belongs to. Frequency matching is case-insensitive.
- **Daily Reset** — `Scheduler.reset_daily_tasks()` clears completion status only for `"daily"` tasks, leaving `"weekly"` and `"as-needed"` tasks untouched.
- **Streamlit Session Persistence** — Owner, pets, and tasks are stored in `st.session_state` so all data survives button clicks, widget interactions, and rerenders without being reset.
- **Validated Time Input** — The UI uses `st.time_input()` instead of a free-text field, guaranteeing every stored `time_str` is a zero-padded `"HH:MM"` string compatible with `sort_by_time()`.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample CLI Output

Run `python main.py` to see the scheduler in action. The output below demonstrates
chronological sorting across two pets, live conflict detection, and status filtering.

```text
==================================================
TEST 1: generate_summary() - pending tasks by pet
==================================================
*** SCHEDULING CONFLICTS DETECTED ***
  WARNING - Conflict at 08:30: Biscuit: 'Afternoon treat', Mochi: 'Breakfast'

Daily plan for Jordan's pets
========================================

Biscuit (dog):
  [todo] 08:30 - Afternoon treat (daily)
  [todo] 14:00 - Flea medication (weekly)
  [todo] 19:00 - Evening walk (daily)

Mochi (cat):
  [todo] 08:30 - Breakfast (daily)
  [todo] 14:30 - Playtime (daily)
  [todo] 19:30 - Dinner feeding (daily)

Progress: 1/7 tasks completed

==================================================
TEST 2: sort_by_time() - all tasks, time-sorted
==================================================
  07:30  [Biscuit]  Morning walk
  08:30  [Biscuit]  Afternoon treat
  08:30  [Mochi]  Breakfast
  14:00  [Biscuit]  Flea medication
  14:30  [Mochi]  Playtime
  19:00  [Biscuit]  Evening walk
  19:30  [Mochi]  Dinner feeding

==================================================
TEST 3: get_pending_tasks() - incomplete only
==================================================
  Biscuit: Evening walk (19:00)
  Biscuit: Flea medication (14:00)
  Biscuit: Afternoon treat (08:30)
  Mochi: Dinner feeding (19:30)
  Mochi: Playtime (14:30)
  Mochi: Breakfast (08:30)

==================================================
TEST 4: get_completed_tasks() - completed only
==================================================
  Biscuit: Morning walk (07:30)

==================================================
TEST 5: get_tasks_by_pet(dog) - Biscuit only
==================================================
  [todo] 19:00  Evening walk
  [done] 07:30  Morning walk
  [todo] 14:00  Flea medication
  [todo] 08:30  Afternoon treat

==================================================
TEST 6: get_tasks_by_frequency('weekly')
==================================================
  Biscuit: Flea medication (14:00)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
========================================================================================== test session starts ==========================================================================================
platform win32 -- Python 3.13.14, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\hiloo\OneDrive\Desktop\Jiyoung\CodePath\AI110\Codepath_AI\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 30 items                                                                                                                                                                                       

tests\test_pawpal.py ..............................                                                                                                                                                [100%]

========================================================================================== 30 passed in 0.10s ===========================================================================================

Confidence Level
5 stars
All 30 happy paths and edge case tests passed successfully.

```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts `(Pet, Task)` pairs by `time_str` in `"HH:MM"` format ascending. Strings that don't match the format are pushed to the end using a `"99:99"` sentinel, preventing silent sort errors. |
| Filtering by status / pet | `Scheduler.get_pending_tasks()`, `Scheduler.get_completed_tasks()`, `Scheduler.get_tasks_by_pet()`, `Scheduler.get_tasks_by_frequency()` | Each method returns `(Pet, Task)` pairs so callers always know which pet a task belongs to. Filters operate on live `Task` objects, so `mark_complete()` is reflected immediately without re-fetching. |
| Conflict detection | `Scheduler.check_conflicts()` | Groups all time-sorted tasks by `time_str` using a `defaultdict`. Any time slot with more than one task produces a named warning string. Non-blocking — warnings are returned as a list and prepended to `generate_summary()` output without stopping schedule generation. |
| Recurring task logic | `Task.get_next_due_date()` | Uses `datetime.timedelta` to compute the next due date: `+1 day` for `"daily"`, `+7 days` for `"weekly"`, `None` for `"as-needed"`. `mark_complete()` automatically stamps `last_completed_date = date.today()` so recurrence tracking stays in sync. |

## 📸 Demo Walkthrough

Launch the app with `streamlit run app.py`, then follow these steps:

1. **Enter your name** — Type your name in the Owner field and click **Save**. The name appears in the generated schedule header.

2. **Add your pets** — Enter a pet name (e.g. `Biscuit`), select a species, and click **Add pet**. Repeat for each pet. Each registered pet appears as a metric card showing its name and current task count.

3. **Schedule tasks** — Select a pet from the dropdown, enter a description (e.g. `Morning walk`), pick a time using the time picker (always produces a valid `HH:MM` string), choose a frequency (`daily`, `weekly`, or `as-needed`), and click **Add task**.

4. **Observe live conflict warnings** — If two tasks share the same time across any pets, a `st.warning()` banner appears immediately above the task table on the next rerender — no button click required. Example: scheduling both Biscuit's `Afternoon treat` and Mochi's `Breakfast` at `08:30` produces: `⚠️ WARNING - Conflict at 08:30: Biscuit: 'Afternoon treat', Mochi: 'Breakfast'`.

5. **View the sorted task table** — The Tasks section displays all tasks sorted strictly by time via `Scheduler.sort_by_time()`, grouped with Pet, Time, Description, Frequency, and Status columns.

6. **Generate today's schedule** — Click **Generate schedule** (primary button at the bottom). The app shows:
   - Three metric cards: Total tasks / Pending / Completed
   - A chronologically sorted table of pending tasks only, with a **Next due** column populated by `Task.get_next_due_date()`
   - A `st.success()` banner if all tasks are complete

**Key scheduler behaviors demonstrated:**
- Tasks added out of order are always re-sorted chronologically before display
- Conflict warnings appear live as soon as a duplicate time is added, without blocking the schedule
- Completing a task removes it from the pending table and increments the Completed metric instantly

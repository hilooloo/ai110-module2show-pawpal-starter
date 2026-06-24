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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

```text
Today's Schedule
Daily plan for Jordan's pets
========================================

Biscuit (dog):
  [todo] 07:30 - Morning walk (daily)
  [todo] 08:00 - Feeding (daily)
  [todo] 09:00 - Flea medication (weekly)

Mochi (cat):
  [todo] 08:30 - Feeding (daily)
  [todo] 18:00 - Litter box clean (daily)

Progress: 0/5 tasks completed
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

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

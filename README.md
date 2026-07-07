# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## ✨ Features

- **Priority-based scheduling** — `Plan.prioritize_tasks()` orders tasks high → medium → low, using duration as a tie-breaker within the same priority tier.
- **Chronological sorting** — `Plan.sort_by_time()` re-orders the same task list by `scheduled_time`, so a plan can be viewed by importance or by time of day.
- **Conflict warnings** — `Plan.detect_conflicts()` checks every pair of scheduled tasks for overlapping time windows (`scheduled_date` + `scheduled_time` + `duration_minutes`) and returns human-readable warnings instead of raising. Catches both same-pet and cross-pet clashes, since one owner can't be in two places at once.
- **Daily/weekly recurrence** — completing a recurring task (`Tasks.mark_complete()`) automatically spawns the next occurrence via `Tasks.spawn_next_occurrence()`, advancing `scheduled_date` by a day or a week. `"once"` tasks don't recur.
- **Status & pet filtering** — `Plan.filter_tasks(is_completed=None, pet_name=None)` narrows the schedule by completion status and/or pet, independently or combined.
- **Automatic plan booking** — `Plan.book_plan()` ties it together: pulls every pet's tasks via `Customer.get_all_tasks()`, drops completed ones, prioritizes what's left, and runs conflict detection in one call.
- **Interactive UI** — the Streamlit app (`app.py`) lets an owner add pets/tasks, generate a schedule, toggle between priority and time ordering, filter by status/pet, and see conflict warnings live.

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
Today's Schedule for Jordan (2026-07-06):
--------------------------------------------------
08:00  Biscuit    Morning walk         [high, 30 min, pending]
08:30  Mochi      Feed breakfast       [high, 10 min, pending]
18:00  Biscuit    Evening meds         [medium, 5 min, pending]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

### What the Tests Cover

The current test suite verifies the following core functionality of the PawPal+ system:

- `mark_complete()` correctly updates a task's completion status.
- Adding a task to a pet increases the pet's task count.
- `sort_by_time()` orders tasks chronologically by their scheduled time.
- Completing a daily recurring task automatically creates the next day's occurrence.
- `detect_conflicts()` identifies overlapping scheduled tasks and reports scheduling conflicts.

Sample test output:

```
tests/test_pawpal.py::test_mark_complete_changes_status PASSED              [ 20%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED      [ 40%]
tests/test_pawpal.py::test_sort_by_time_orders_tasks_chronologically PASSED [ 60%]
tests/test_pawpal.py::test_mark_complete_on_daily_task_creates_next_day_occurrence PASSED [ 80%]
tests/test_pawpal.py::test_detect_conflicts_flags_tasks_at_duplicate_times PASSED [100%]
```

### Confidence Level

⭐⭐⭐⭐☆ (4/5)

All five automated tests passed successfully, indicating that the core task management, scheduling, recurring task generation, and conflict detection features are working as expected. Additional edge-case and integration tests (such as invalid inputs, empty task lists, and priority tie cases) would increase confidence in the overall reliability of the system.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Plan.prioritize_tasks()`, `Plan.sort_by_time()` | `prioritize_tasks()` sorts by priority (high first), then duration as a tie-breaker within the same priority. `sort_by_time()` sorts the same list chronologically by `scheduled_time` instead, so the plan can be viewed either by importance or by time of day. |
| Filtering | `Plan.filter_tasks(is_completed=None, pet_name=None)` | Narrows `scheduled_tasks` by completion status and/or pet name. Both filters are optional and independent — pass one, both (ANDed together), or neither. |
| Conflict handling | `Plan.detect_conflicts()` | Compares every pair of scheduled tasks by `[scheduled_date + scheduled_time, +duration_minutes)` window and flags any that overlap — regardless of whether it's the same pet or two different pets, since one owner can't be in two places at once. Returns a list of warning strings instead of raising, so a scheduling clash never crashes the app. `book_plan()` runs it automatically and stores the result in `Plan.conflicts`. |
| Recurring tasks | `Tasks.mark_complete()` → `Tasks.spawn_next_occurrence()` | Completing a `"daily"` or `"weekly"` task automatically creates and attaches the next occurrence, with `scheduled_date` advanced by a `timedelta` (1 day or 1 week). `"once"` tasks don't recur. |

## 📸 Demo Walkthrough

### Main UI features

The Streamlit app (`app.py`) is organized into four sections, each backed directly by the
`pawpal_system` classes:

- **Add a Pet** — enter a name, species, breed, and optional special instructions; submitted
  pets are added via `Customer.add_pet()` and listed in a table with their live task count.
- **Schedule a Task** — pick a pet, category, frequency, description, time, duration, and
  priority; submitting calls `Customer.add_task(pet_id, task)`, which attaches the task to that
  pet. All tasks across every pet are shown in a running table below the form.
- **Build Schedule** — generates a `Plan` for today via `Plan.book_plan()`, which gathers every
  pet's tasks, drops completed ones, and prioritizes what's left.
- **Sort & filter controls** — once a schedule exists, a radio toggle switches between priority
  order and `Plan.sort_by_time()`'s chronological order, and two dropdowns narrow the table by
  completion status and/or pet via `Plan.filter_tasks()`.

### Example workflow

1. **Add a pet** — e.g. "Mochi" (cat) and "Biscuit" (dog).
2. **Schedule a task** for each pet — e.g. a "Morning walk" for Biscuit at 08:00 and "Feed
   breakfast" for Mochi at 08:30.
3. **Click "Generate schedule"** to build today's plan.
4. **View today's schedule** — the table shows both tasks in priority order, with a success or
   warning banner depending on whether `detect_conflicts()` found any overlaps.
5. **Toggle "Sort by: Time"** to see the same tasks re-ordered chronologically instead, or use
   the Status/Pet filters to narrow the table down (e.g. just Mochi's pending tasks).

### Key Scheduler behaviors shown

- **Priority-based scheduling** — high-priority tasks surface first, with shorter tasks breaking
  ties within the same priority tier.
- **Chronological sorting** — the same task list re-ordered by time of day on demand.
- **Conflict warnings** — overlapping tasks (same pet or different pets) are flagged with a
  human-readable warning instead of silently double-booking the owner.
- **Filtering** — narrowing the plan by completion status, pet, or both at once.
- **Daily recurrence** — completing a `"daily"`/`"weekly"` task automatically schedules its next
  occurrence one interval later.

### Sample CLI output

`main.py` demonstrates the same behaviors end-to-end outside the UI — building an owner with two
pets, six deliberately out-of-order and overlapping tasks, then booking and inspecting a plan:

```
Today's Schedule for Jordan (2026-07-06) - priority order:
--------------------------------------------------
08:30  Mochi      Feed breakfast       [high, 10 min, pending]
08:00  Biscuit    Morning walk         [high, 30 min, pending]
18:00  Biscuit    Evening meds         [medium, 5 min, pending]
08:10  Biscuit    Ear cleaning         [low, 10 min, pending]
12:00  Mochi      Midday playtime      [low, 15 min, pending]
08:00  Mochi      Nail trim            [low, 15 min, pending]

Conflict check (detect_conflicts, run automatically by book_plan):
--------------------------------------------------
WARNING: Conflict: 'Morning walk' (Biscuit, 08:00) overlaps with 'Ear cleaning' (Biscuit, 08:10)
WARNING: Conflict: 'Morning walk' (Biscuit, 08:00) overlaps with 'Nail trim' (Mochi, 08:00)
WARNING: Conflict: 'Ear cleaning' (Biscuit, 08:10) overlaps with 'Nail trim' (Mochi, 08:00)

Sorted by time (sort_by_time):
--------------------------------------------------
08:00  Mochi      Nail trim            [low, 15 min, pending]
08:00  Biscuit    Morning walk         [high, 30 min, pending]
08:10  Biscuit    Ear cleaning         [low, 10 min, pending]
08:30  Mochi      Feed breakfast       [high, 10 min, done]
08:30  Mochi      Feed breakfast       [high, 10 min, pending]
12:00  Mochi      Midday playtime      [low, 15 min, pending]
18:00  Biscuit    Evening meds         [medium, 5 min, pending]

Filtered: pending tasks only (filter_tasks(is_completed=False)):
--------------------------------------------------
08:00  Mochi      Nail trim            [low, 15 min, pending]
08:00  Biscuit    Morning walk         [high, 30 min, pending]
08:10  Biscuit    Ear cleaning         [low, 10 min, pending]
08:30  Mochi      Feed breakfast       [high, 10 min, pending]
12:00  Mochi      Midday playtime      [low, 15 min, pending]
18:00  Biscuit    Evening meds         [medium, 5 min, pending]

Filtered: Mochi's tasks only (filter_tasks(pet_name='Mochi')):
--------------------------------------------------
08:00  Mochi      Nail trim            [low, 15 min, pending]
08:30  Mochi      Feed breakfast       [high, 10 min, done]
08:30  Mochi      Feed breakfast       [high, 10 min, pending]
12:00  Mochi      Midday playtime      [low, 15 min, pending]

Filtered: Mochi's pending tasks (filter_tasks(is_completed=False, pet_name='Mochi')):
--------------------------------------------------
08:00  Mochi      Nail trim            [low, 15 min, pending]
08:30  Mochi      Feed breakfast       [high, 10 min, pending]
12:00  Mochi      Midday playtime      [low, 15 min, pending]
```

Note the two "Feed breakfast" rows in the last three sections: `main.py` marks the first task in
the list complete before re-running `sort_by_time()`/`filter_tasks()`, which triggers
`spawn_next_occurrence()` and adds tomorrow's pending copy alongside the original completed one —
a live demonstration of daily recurrence.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

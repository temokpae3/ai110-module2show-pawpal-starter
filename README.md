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
Today's Schedule for Jordan (2026-07-06):
--------------------------------------------------
08:00  Biscuit    Morning walk         [high, 30 min, pending]
08:30  Mochi      Feed breakfast       [high, 10 min, pending]
18:00  Biscuit    Evening meds         [medium, 5 min, pending]
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
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Plan.prioritize_tasks()`, `Plan.sort_by_time()` | `prioritize_tasks()` sorts by priority (high first), then duration as a tie-breaker within the same priority. `sort_by_time()` sorts the same list chronologically by `scheduled_time` instead, so the plan can be viewed either by importance or by time of day. |
| Filtering | `Plan.filter_tasks(is_completed=None, pet_name=None)` | Narrows `scheduled_tasks` by completion status and/or pet name. Both filters are optional and independent — pass one, both (ANDed together), or neither. |
| Conflict handling | `Plan.detect_conflicts()` | Compares every pair of scheduled tasks by `[scheduled_date + scheduled_time, +duration_minutes)` window and flags any that overlap — regardless of whether it's the same pet or two different pets, since one owner can't be in two places at once. Returns a list of warning strings instead of raising, so a scheduling clash never crashes the app. `book_plan()` runs it automatically and stores the result in `Plan.conflicts`. |
| Recurring tasks | `Tasks.mark_complete()` → `Tasks.spawn_next_occurrence()` | Completing a `"daily"` or `"weekly"` task automatically creates and attaches the next occurrence, with `scheduled_date` advanced by a `timedelta` (1 day or 1 week). `"once"` tasks don't recur. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

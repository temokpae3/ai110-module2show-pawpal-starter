"""Demo script for PawPal+: builds an owner, pets, and tasks, then books a plan."""

from datetime import date, time

from pawpal_system import Customer, Pets, Plan, Tasks

owner = Customer("c1", "Jordan", "jordan@example.com", "555-0100")

mochi = Pets("p1", "Mochi", "cat", "Tabby", special_instructions="Feed wet food only")
biscuit = Pets("p2", "Biscuit", "dog", "Golden Retriever")
owner.add_pet(mochi)
owner.add_pet(biscuit)

# Tasks are added out of chronological order on purpose, to prove sort_by_time()
# actually reorders them instead of relying on insertion order.
owner.add_task(
    "p2",
    Tasks("t1", "Evening meds", "meds", time(18, 0), "daily", duration_minutes=5, priority="medium"),
)
owner.add_task(
    "p1",
    Tasks("t2", "Feed breakfast", "feeding", time(8, 30), "daily", duration_minutes=10, priority="high"),
)
owner.add_task(
    "p2",
    Tasks("t3", "Morning walk", "walk", time(8, 0), "daily", duration_minutes=30, priority="high"),
)
owner.add_task(
    "p1",
    Tasks("t4", "Midday playtime", "enrichment", time(12, 0), "daily", duration_minutes=15, priority="low"),
)

# Deliberately overlapping tasks, to verify detect_conflicts() catches both
# a same-pet clash and a different-pet clash:
# - t5 (Mochi, 08:00-08:15) overlaps t3 (Biscuit, 08:00-08:30) -> different pets
# - t6 (Biscuit, 08:10-08:20) also overlaps t3 (Biscuit, 08:00-08:30) -> same pet
owner.add_task(
    "p1",
    Tasks("t5", "Nail trim", "grooming", time(8, 0), "daily", duration_minutes=15, priority="low"),
)
owner.add_task(
    "p2",
    Tasks("t6", "Ear cleaning", "grooming", time(8, 10), "daily", duration_minutes=10, priority="low"),
)

# Mark one task already done so the completion filter has something to exclude.
owner.get_all_tasks()[0].mark_complete()

todays_plan = Plan("plan1", date.today(), owner)
todays_plan.book_plan()


def print_tasks(tasks, heading):
    print(heading)
    print("-" * 50)
    if not tasks:
        print("(none)")
    for task in tasks:
        pet_name = task.pet.name if task.pet else "Unknown pet"
        status = "done" if task.is_completed else "pending"
        print(
            f"{task.scheduled_time.strftime('%H:%M')}  "
            f"{pet_name:<10} {task.description:<20} "
            f"[{task.priority}, {task.duration_minutes} min, {status}]"
        )
    print()


print_tasks(todays_plan.scheduled_tasks, f"Today's Schedule for {owner.name} ({todays_plan.date}) - priority order:")

print("Conflict check (detect_conflicts, run automatically by book_plan):")
print("-" * 50)
if todays_plan.conflicts:
    for warning in todays_plan.conflicts:
        print(f"WARNING: {warning}")
else:
    print("(none)")
print()

# book_plan() already drops completed tasks, so add the completed one back in
# to demonstrate sort_by_time() and filter_tasks() against a fuller task list.
todays_plan.scheduled_tasks = owner.get_all_tasks()

todays_plan.sort_by_time()
print_tasks(todays_plan.scheduled_tasks, "Sorted by time (sort_by_time):")

pending_only = todays_plan.filter_tasks(is_completed=False)
print_tasks(pending_only, "Filtered: pending tasks only (filter_tasks(is_completed=False)):")

mochi_only = todays_plan.filter_tasks(pet_name="Mochi")
print_tasks(mochi_only, "Filtered: Mochi's tasks only (filter_tasks(pet_name='Mochi')):")

mochi_pending = todays_plan.filter_tasks(is_completed=False, pet_name="Mochi")
print_tasks(mochi_pending, "Filtered: Mochi's pending tasks (filter_tasks(is_completed=False, pet_name='Mochi')):")

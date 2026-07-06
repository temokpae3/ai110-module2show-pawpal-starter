"""Demo script for PawPal+: builds an owner, pets, and tasks, then books a plan."""

from datetime import date, time

from pawpal_system import Customer, Pets, Plan, Tasks

owner = Customer("c1", "Jordan", "jordan@example.com", "555-0100")

mochi = Pets("p1", "Mochi", "cat", "Tabby", special_instructions="Feed wet food only")
biscuit = Pets("p2", "Biscuit", "dog", "Golden Retriever")
owner.add_pet(mochi)
owner.add_pet(biscuit)

owner.add_task(
    "p2",
    Tasks("t1", "Morning walk", "walk", time(8, 0), "daily", duration_minutes=30, priority="high"),
)
owner.add_task(
    "p1",
    Tasks("t2", "Feed breakfast", "feeding", time(8, 30), "daily", duration_minutes=10, priority="high"),
)
owner.add_task(
    "p2",
    Tasks("t3", "Evening meds", "meds", time(18, 0), "daily", duration_minutes=5, priority="medium"),
)

todays_plan = Plan("plan1", date.today(), owner)
todays_plan.book_plan()

print(f"Today's Schedule for {owner.name} ({todays_plan.date}):")
print("-" * 50)
for task in sorted(todays_plan.scheduled_tasks, key=lambda t: t.scheduled_time):
    pet_name = task.pet.name if task.pet else "Unknown pet"
    status = "done" if task.is_completed else "pending"
    print(
        f"{task.scheduled_time.strftime('%H:%M')}  "
        f"{pet_name:<10} {task.description:<20} "
        f"[{task.priority}, {task.duration_minutes} min, {status}]"
    )

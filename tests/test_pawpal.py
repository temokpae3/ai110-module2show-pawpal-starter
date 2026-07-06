from datetime import date, time

from pawpal_system import Pets, Plan, Tasks


def make_task(task_id="t1"):
    return Tasks(
        task_id=task_id,
        description="Morning walk",
        category="walk",
        scheduled_time=time(8, 0),
        frequency="daily",
    )


def test_mark_complete_changes_status():
    task = make_task()
    assert task.is_completed is False

    task.mark_complete()

    assert task.is_completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pets("p1", "Mochi", "cat", "Tabby")
    assert len(pet.tasks) == 0

    pet.add_task(make_task())

    assert len(pet.tasks) == 1


def test_sort_by_time_orders_tasks_chronologically(sample_customer, sample_pet):
    late = Tasks("t1", "Dinner", "feeding", time(18, 0), "daily")
    early = Tasks("t2", "Breakfast", "feeding", time(8, 0), "daily")
    mid = Tasks("t3", "Walk", "walk", time(12, 0), "daily")

    # Add out of order on purpose so a passing test proves sort_by_time()
    # actually reorders them instead of relying on insertion order.
    sample_pet.add_task(late)
    sample_pet.add_task(early)
    sample_pet.add_task(mid)

    plan = Plan("plan1", date.today(), sample_customer)
    plan.scheduled_tasks = sample_customer.get_all_tasks()

    ordered = plan.sort_by_time()

    assert [t.task_id for t in ordered] == ["t2", "t3", "t1"]


def test_mark_complete_on_daily_task_creates_next_day_occurrence(sample_pet):
    task = Tasks(
        "t1",
        "Morning walk",
        "walk",
        time(8, 0),
        "daily",
        scheduled_date=date(2026, 7, 6),
    )
    sample_pet.add_task(task)

    task.mark_complete()

    assert len(sample_pet.tasks) == 2
    next_task = sample_pet.tasks[1]
    assert next_task.task_id != task.task_id
    assert next_task.scheduled_date == date(2026, 7, 7)
    assert next_task.scheduled_time == time(8, 0)
    assert next_task.is_completed is False


def test_detect_conflicts_flags_tasks_at_duplicate_times(sample_customer, sample_pet):
    biscuit = Pets("p2", "Biscuit", "dog", "Golden Retriever")
    sample_customer.add_pet(biscuit)

    task_a = Tasks("t1", "Morning walk", "walk", time(8, 0), "daily", duration_minutes=30)
    task_b = Tasks("t2", "Nail trim", "grooming", time(8, 0), "daily", duration_minutes=15)
    sample_pet.add_task(task_a)
    biscuit.add_task(task_b)

    plan = Plan("plan1", date.today(), sample_customer)
    plan.scheduled_tasks = sample_customer.get_all_tasks()

    conflicts = plan.detect_conflicts()

    assert len(conflicts) == 1
    assert "Morning walk" in conflicts[0]
    assert "Nail trim" in conflicts[0]

from datetime import time

from pawpal_system import Pets, Tasks


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

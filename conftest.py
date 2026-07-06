from datetime import time

import pytest

from pawpal_system import Customer, Pets, Tasks


@pytest.fixture
def sample_task():
    return Tasks(
        task_id="t1",
        description="Morning walk",
        category="walk",
        scheduled_time=time(8, 0),
        frequency="daily",
    )


@pytest.fixture
def sample_pet():
    return Pets("p1", "Mochi", "cat", "Tabby")


@pytest.fixture
def sample_customer(sample_pet):
    customer = Customer("c1", "Jordan", "jordan@example.com", "555-0100")
    customer.add_pet(sample_pet)
    return customer

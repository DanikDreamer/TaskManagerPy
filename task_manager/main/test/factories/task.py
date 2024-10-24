import factory
import random
from datetime import datetime, timedelta

from task_manager.main.models import Task
from task_manager.main.test.factories.base import faker


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.LazyAttribute(lambda _: faker.sentence()[:55])
    description = factory.LazyAttribute(lambda _: faker.text())
    created_at = factory.LazyAttribute(lambda _: datetime.now().strftime("%Y-%m-%d"))
    updated_at = factory.LazyAttribute(lambda _: datetime.now().strftime("%Y-%m-%d"))
    expired_at = factory.LazyAttribute(
        lambda _: (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    )
    state = factory.LazyAttribute(lambda _: random.choice(Task.States.values))
    priority = factory.LazyAttribute(
        lambda _: random.choice(Task.PriorityLevels.values)
    )

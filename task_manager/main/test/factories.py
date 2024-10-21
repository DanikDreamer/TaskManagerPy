import random
import factory
from faker import Faker
from datetime import datetime, timedelta

from task_manager.main.models import User, Tag, Task

faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.unique.user_name())
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    email = factory.LazyAttribute(lambda _: faker.email())
    date_of_birth = factory.LazyAttribute(lambda _: faker.date())
    phone = factory.LazyAttribute(lambda _: faker.phone_number()[:20])


class AdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.unique.user_name())
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    email = factory.LazyAttribute(lambda _: faker.email())
    date_of_birth = factory.LazyAttribute(lambda _: faker.date())
    phone = factory.LazyAttribute(lambda _: faker.phone_number()[:15])
    is_staff = True


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    title = factory.LazyAttribute(lambda _: faker.sentence()[:55])


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
    author = factory.SubFactory(UserFactory)
    assignee = factory.SubFactory(UserFactory)
    state = factory.LazyAttribute(lambda _: random.choice(Task.States.values))
    priority = factory.LazyAttribute(
        lambda _: random.choice(Task.PriorityLevels.values)
    )

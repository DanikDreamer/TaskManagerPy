import factory

from task_manager.main.models import Tag
from .base import faker


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    title = factory.LazyAttribute(lambda _: faker.sentence()[:55])

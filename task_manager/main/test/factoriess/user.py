import factory
from datetime import datetime, timedelta

from task_manager.main.models import User
from task_manager.main.test.factoriess.base import ImageFileProvider
from .base import faker

faker.add_provider(ImageFileProvider)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.LazyAttribute(lambda _: faker.unique.user_name())
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    email = factory.LazyAttribute(lambda _: faker.email())
    date_of_birth = factory.LazyAttribute(lambda _: faker.date())
    phone = factory.LazyAttribute(lambda _: faker.phone_number()[:20])
    avatar_picture = factory.LazyAttribute(lambda _: faker.image_file(fmt="jpeg"))
    # avatar_picture = faker.image_file(fmt="jpeg")

    @factory.post_generation
    def password(obj, create, extracted):
        if not create:
            return
        obj.set_password(extracted)
        obj.save()


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

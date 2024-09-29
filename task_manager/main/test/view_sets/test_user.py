import factory

from base import TestViewSetBase
from factories import UserFactory, AdminFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = UserFactory

    def test_list(self):
        user = UserFactory()

        response = self.list()
        usernames = [user["username"] for user in response]

        assert user.username in usernames

    def test_retrieve(self):
        user = UserFactory()

        response = self.retrieve(user.id)

        assert user.username == response["username"]

    def test_create(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

        self.create(user_attributes)

    def test_update(self):
        user = UserFactory()
        new_user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

        self.update(user.id, new_user_attributes)

    def test_delete(self):
        user = UserFactory()

        self.delete(user.id)


class TestUserNoAuthViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = None

    def test_list(self):
        UserFactory()

        self.list()

    def test_retrieve(self):
        user = UserFactory()

        self.retrieve(user.id)

    def test_create(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

        self.create(user_attributes)

    def test_update(self):
        user = UserFactory()
        new_user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

        self.update(user.id, new_user_attributes)

    def test_delete(self):
        user = UserFactory()

        self.delete(user.id)


class TestAdminOnlyDeleteUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = AdminFactory

    def test_delete(self):
        user = UserFactory()

        self.delete(user.id)

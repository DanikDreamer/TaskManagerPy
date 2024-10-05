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
        user_attributes = UserFactory.build()
        user_data = {
            "username": user_attributes.username,
            "first_name": user_attributes.first_name,
            "last_name": user_attributes.last_name,
            "email": user_attributes.email,
            "date_of_birth": user_attributes.date_of_birth,
            "phone": user_attributes.phone,
        }

        self.create(user_data)

    def test_update(self):
        user = UserFactory()
        new_user_attributes = UserFactory.build()
        new_user_data = {
            "username": new_user_attributes.username,
            "first_name": new_user_attributes.first_name,
            "last_name": new_user_attributes.last_name,
            "email": new_user_attributes.email,
            "date_of_birth": new_user_attributes.date_of_birth,
            "phone": new_user_attributes.phone,
        }

        self.update(user.id, new_user_data)

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
        user_attributes = UserFactory.build()
        user_data = {
            "username": user_attributes.username,
            "first_name": user_attributes.first_name,
            "last_name": user_attributes.last_name,
            "email": user_attributes.email,
            "date_of_birth": user_attributes.date_of_birth,
            "phone": user_attributes.phone,
        }

        self.create(user_data)

    def test_update(self):
        user = UserFactory()
        new_user_attributes = UserFactory.build()
        new_user_data = {
            "username": new_user_attributes.username,
            "first_name": new_user_attributes.first_name,
            "last_name": new_user_attributes.last_name,
            "email": new_user_attributes.email,
            "date_of_birth": new_user_attributes.date_of_birth,
            "phone": new_user_attributes.phone,
        }

        self.update(user.id, new_user_data)

    def test_delete(self):
        user = UserFactory()

        self.delete(user.id)


class TestAdminOnlyDeleteUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = AdminFactory

    def test_delete(self):
        user = UserFactory()

        self.delete(user.id)

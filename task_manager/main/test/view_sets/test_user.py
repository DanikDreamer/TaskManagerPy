import factory
from http import HTTPStatus

from task_manager.main.test.base import TestViewSetBase
from task_manager.main.test.factories import UserFactory, AdminFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

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

        user = self.create(user_attributes)

        expected_response = self.expected_details(user, user_attributes)
        assert user == expected_response

    def test_update(self):
        user = UserFactory()
        new_user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

        self.update(user.id, new_user_attributes)

    def test_delete(self):
        user = UserFactory()

        response = self.request_delete(user.id)

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestUserNoAuthViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = None

    def setUp(self):
        self.unauthenticate_user()

    def test_list(self):
        UserFactory()

        response = self.request_list()

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_retrieve(self):
        user = UserFactory()

        response = self.request_retrieve(user.id)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_create(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

        response = self.request_create(user_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_update(self):
        user = UserFactory()
        new_user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

        response = self.request_update(user.id, new_user_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_delete(self):
        user = UserFactory()

        response = self.request_delete(user.id)

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestAdminOnlyDeleteUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = factory.build(dict, FACTORY_CLASS=AdminFactory)

    def test_delete(self):
        user = UserFactory()

        self.delete(user.id)

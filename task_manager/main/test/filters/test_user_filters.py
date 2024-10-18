import factory

from task_manager.main.test.base import TestViewSetBase
from task_manager.main.test.factoriess import UserFactory


class TestUserFilterSet(TestViewSetBase):
    basename = "users"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    def test_username_field_filter(self):
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = UserFactory()

        response = self.list({"username": user1.username})
        usernames = [user["username"] for user in response]

        assert user1.username in usernames
        assert user2.username not in usernames
        assert user3.username not in usernames

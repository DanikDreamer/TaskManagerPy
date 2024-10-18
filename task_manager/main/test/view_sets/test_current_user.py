import factory
from urllib.parse import urlparse
from django.test import RequestFactory

from task_manager.main.test.base import TestViewSetBase
from task_manager.main.test.factoriess import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "current_user"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    @staticmethod
    def get_absolute_uri(relative_path):
        request = RequestFactory().get("/")
        return request.build_absolute_uri(relative_path)

    def test_retrieve(self):
        user = self.single_resource()

        assert user == {
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "role": self.user.role,
            "username": self.user.username,
            "date_of_birth": self.user.date_of_birth,
            "phone": self.user.phone,
            "avatar_picture": self.get_absolute_uri(self.user.avatar_picture.url),
        }

    def test_patch(self):
        self.patch_single_resource({"first_name": "TestName"})

        user = self.single_resource()
        assert user["first_name"] == "TestName"

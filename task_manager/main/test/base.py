from http import HTTPStatus
from typing import List, Union

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from task_manager.main.models import User


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.client = APIClient()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    @classmethod
    def create_api_user(cls) -> User:
        if cls.user_attributes:
            return User.objects.create(**cls.user_attributes)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    @classmethod
    def unauthenticate_user(cls) -> None:
        cls.client.logout()

    def request_list(
        self, data: dict = None, args: List[Union[str, int]] = None
    ) -> dict:
        response = self.client.get(self.list_url(args), data=data)
        return response

    def list(self, data: dict = None, args: List[Union[str, int]] = None) -> dict:
        response = self.client.get(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def request_retrieve(self, key: int) -> dict:
        response = self.client.get(self.detail_url(key))
        return response

    def retrieve(self, key: int) -> dict:
        response = self.client.get(self.detail_url(key))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def request_create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        response = self.client.post(self.list_url(args), data=data)
        return response

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.json()

    def request_update(self, key: int, data: dict) -> dict:
        response = self.client.put(self.detail_url(key), data=data)
        return response

    def update(self, key: int, data: dict) -> dict:
        response = self.client.put(self.detail_url(key), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def request_delete(self, key: int) -> dict:
        response = self.client.delete(self.detail_url(key))
        return response

    def delete(self, key: int) -> dict:
        response = self.client.delete(self.detail_url(key))
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        return response.data

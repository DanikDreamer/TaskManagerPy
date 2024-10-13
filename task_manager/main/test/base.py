from http import HTTPStatus
from typing import List, Union

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.response import Response

from task_manager.main.models import User
from task_manager.main.test.factories import UserFactory, TagFactory, TaskFactory


class ActionClient:
    def __init__(self, api_client: APIClient, user: User) -> None:
        self.api_client = api_client
        self.user = user

    def authenticate_user(self) -> None:
        if self.user:
            self.api_client.force_authenticate(self.user)

    def request_create_user(self, **attributes) -> Response:
        url = reverse("users-list")
        return self.api_client.post(url, data=attributes)

    def create_user(self) -> dict:
        user_attributes = UserFactory.build()
        user_data = {
            "username": user_attributes.username,
            "first_name": user_attributes.first_name,
            "last_name": user_attributes.last_name,
            "email": user_attributes.email,
            "date_of_birth": user_attributes.date_of_birth,
            "phone": user_attributes.phone,
        }
        response = self.request_create_user(**user_data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create_task(self, **attributes) -> Response:
        url = reverse("tasks-list")
        return self.api_client.post(url, data=attributes)

    def create_task(self, **attributes) -> dict:
        user = UserFactory()
        tag = TagFactory()
        task_attributes = TaskFactory.build()
        task_data = {
            "title": task_attributes.title,
            "description": task_attributes.description,
            "state": task_attributes.state,
            "priority": task_attributes.priority,
            "author": user.id,
            "tags": [tag.id],
        }
        task_data.update(attributes)
        response = self.request_create_task(**task_data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    action_client: ActionClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.client = APIClient()
        cls.action_client = ActionClient(cls.client, cls.user)
        cls.action_client.authenticate_user()

    @classmethod
    def create_api_user(cls) -> User:
        if cls.user_attributes:
            return cls.user_attributes.create()

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    @classmethod
    def assert_details(cls, response_data, expected_data) -> None:
        for key, value in expected_data.items():
            assert response_data.get(key) == value

    def authenticate_user(self) -> None:
        if self.user:
            self.client.force_login(self.user)

    def list(self, data: dict = None, args: List[Union[str, int]] = None) -> dict:
        self.authenticate_user()
        response = self.client.get(self.list_url(args), data=data)
        if self.user:
            assert response.status_code == HTTPStatus.OK, response.content
        else:
            assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data

    def retrieve(self, key: int) -> dict:
        self.authenticate_user()
        response = self.client.get(self.detail_url(key))
        if self.user:
            assert response.status_code == HTTPStatus.OK, response.content
        else:
            assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.authenticate_user()
        response = self.client.post(self.list_url(args), data=data)
        if self.user:
            self.assert_details(response.data, data)
            assert response.status_code == HTTPStatus.CREATED, response.content
        else:
            assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data

    def update(self, key: int, data: dict) -> dict:
        self.authenticate_user()
        response = self.client.put(self.detail_url(key), data=data)
        if self.user:
            self.assert_details(response.data, data)
            assert response.status_code == HTTPStatus.OK, response.content
        else:
            assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data

    def delete(self, key: int) -> dict:
        self.authenticate_user()
        response = self.client.delete(self.detail_url(key))
        if self.user and self.user.is_staff:
            assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        else:
            assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data

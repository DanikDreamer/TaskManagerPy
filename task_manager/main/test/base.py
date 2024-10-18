import factory
from http import HTTPStatus
from typing import List, Union

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.response import Response

from task_manager.main.models import User
from task_manager.main.test.factoriess import UserFactory, TagFactory, TaskFactory


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
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        response = self.request_create_user(**user_attributes)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create_task(self, **attributes) -> Response:
        url = reverse("tasks-list")
        return self.api_client.post(url, data=attributes)

    def create_task(self, **attributes) -> dict:
        task_attributes = factory.build(
            dict, FACTORY_CLASS=TaskFactory, author=self.user.id
        )
        task_attributes.update(attributes)
        response = self.request_create_task(**task_attributes)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create_tag(self, **attributes) -> Response:
        url = reverse("tags-list")
        return self.api_client.post(url, data=attributes)

    def create_tag(self, **attributes) -> dict:
        tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)
        response = self.request_create_tag(**tag_attributes)
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

    def setUp(self) -> None:
        self.client.force_login(self.user)

    @classmethod
    def create_api_user(cls) -> User:
        if cls.user_attributes:
            return User.objects.create(**cls.user_attributes)

    @classmethod
    def detail_url(cls, keys: List[int]) -> str:
        return reverse(f"{cls.basename}-detail", args=keys)

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

    def request_retrieve(self, keys: List[int]) -> dict:
        response = self.client.get(self.detail_url(keys))
        return response

    def retrieve(self, keys: List[int]) -> dict:
        response = self.client.get(self.detail_url(keys))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def request_create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        response = self.client.post(self.list_url(args), data=data)
        return response

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.json()

    def request_update(self, keys: List[int], data: dict) -> dict:
        response = self.client.put(self.detail_url(keys), data=data)
        return response

    def update(self, keys: List[int], data: dict) -> dict:
        response = self.client.put(self.detail_url(keys), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def request_delete(self, keys: List[int]) -> dict:
        response = self.client.delete(self.detail_url(keys))
        return response

    def delete(self, keys: List[int]) -> dict:
        response = self.client.delete(self.detail_url(keys))
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        return response.data

    def request_single_resource(self, data: dict = None) -> Response:
        return self.client.get(self.list_url(), data=data)

    def single_resource(self, data: dict = None) -> dict:
        response = self.request_single_resource(data)
        assert response.status_code == HTTPStatus.OK
        return response.data

    def request_patch_single_resource(self, attributes: dict) -> Response:
        url = self.list_url()
        return self.client.patch(url, data=attributes)

    def patch_single_resource(self, attributes: dict) -> dict:
        response = self.request_patch_single_resource(attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

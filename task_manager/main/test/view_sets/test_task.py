import factory
from http import HTTPStatus

from task_manager.main.test.base import TestViewSetBase
from task_manager.main.test.factories import (
    UserFactory,
    AdminFactory,
    TagFactory,
    TaskFactory,
)


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_list(self):
        task = TaskFactory()

        response = self.list()
        task_titles = [task["title"] for task in response]

        assert task.title in task_titles

    def test_retrieve(self):
        task = TaskFactory()

        response = self.retrieve(task.id)

        assert task.title == response["title"]

    def test_create(self):
        author = UserFactory()
        assignee = UserFactory()
        tag1 = TagFactory()
        tag2 = TagFactory()
        task_attributes = factory.build(
            dict,
            FACTORY_CLASS=TaskFactory,
            author=author.id,
            assignee=assignee.id,
            tags=[tag1.id, tag2.id],
        )

        task = self.create(task_attributes)

        expected_response = self.expected_details(task, task_attributes)
        assert task == expected_response

    def test_update(self):
        author = UserFactory()
        assignee = UserFactory()
        task = TaskFactory()
        tag = TagFactory()
        new_task_attributes = factory.build(
            dict,
            FACTORY_CLASS=TaskFactory,
            author=author.id,
            assignee=assignee.id,
            tags=[tag.id],
        )

        self.update(task.id, new_task_attributes)

    def test_delete(self):
        task = TaskFactory()

        response = self.request_delete(task.id)

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestTaskNoAuthViewSet(TestViewSetBase):
    basename = "tasks"
    user_attributes = None

    def setUp(self):
        self.unauthenticate_user()

    def test_list(self):
        TaskFactory()

        response = self.request_list()

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_retrieve(self):
        task = TaskFactory()

        response = self.request_retrieve(task.id)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_create(self):
        author = UserFactory()
        assignee = UserFactory()
        tag1 = TagFactory()
        tag2 = TagFactory()
        task_attributes = factory.build(
            dict,
            FACTORY_CLASS=TaskFactory,
            author=author.id,
            assignee=assignee.id,
            tags=[tag1.id, tag2.id],
        )

        response = self.request_create(task_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_update(self):
        author = UserFactory()
        assignee = UserFactory()
        task = TaskFactory()
        tag = TagFactory()
        new_task_attributes = factory.build(
            dict,
            FACTORY_CLASS=TaskFactory,
            author=author.id,
            assignee=assignee.id,
            tags=[tag.id],
        )

        response = self.request_update(task.id, new_task_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_delete(self):
        task = TaskFactory()

        response = self.request_delete(task.id)

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestAdminOnlyDeleteTaskViewSet(TestViewSetBase):
    basename = "tasks"
    user_attributes = factory.build(dict, FACTORY_CLASS=AdminFactory)

    def test_delete(self):
        task = TaskFactory()

        self.delete(task.id)

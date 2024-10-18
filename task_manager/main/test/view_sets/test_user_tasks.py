import factory
from http import HTTPStatus

from task_manager.main.test.base import TestViewSetBase
from task_manager.main.test.factoriess import UserFactory, TaskFactory


class TestUserTasksViewSet(TestViewSetBase):
    basename = "user_tasks"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {
            **attributes,
            "id": entity["id"],
            "author": entity["author"],
            "assignee": entity["assignee"],
            "tags": entity["tags"],
        }

    def test_list(self) -> None:
        user = self.action_client.create_user()
        task = self.action_client.create_task(assignee=user["id"])
        self.action_client.create_task()

        tasks = self.list(args=[user["id"]])

        assert tasks == [task]

    def test_retrieve_foreign_task(self) -> None:
        user = self.action_client.create_user()
        task = self.action_client.create_task()

        response = self.request_retrieve([user["id"], task["id"]])

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_retrieve(self) -> None:
        user = self.action_client.create_user()
        created_task = self.action_client.create_task(assignee=user["id"])

        retrieved_task = self.retrieve([user["id"], created_task["id"]])

        assert created_task == retrieved_task

    def test_create(self) -> None:
        user = self.action_client.create_user()
        task_attributes = factory.build(dict, FACTORY_CLASS=TaskFactory)

        task = self.create(task_attributes, [user["id"]])
        expected_response = self.expected_details(task, task_attributes)

        assert task["author"] == user["id"]
        assert task == expected_response

    def test_update(self) -> None:
        user = self.action_client.create_user()
        task = self.action_client.create_task(assignee=user["id"])

        new_task_attributes = factory.build(
            dict, FACTORY_CLASS=TaskFactory, author=task["author"]
        )

        updated_task = self.update([user["id"], task["id"]], new_task_attributes)

        expected_response = self.expected_details(updated_task, new_task_attributes)
        assert updated_task == expected_response

    def test_delete(self) -> None:
        user = self.action_client.create_user()
        task = self.action_client.create_task(assignee=user["id"])

        self.delete([user["id"], task["id"]])

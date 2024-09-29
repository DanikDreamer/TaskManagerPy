from task_manager.main.test.base import TestViewSetBase
from task_manager.main.test.factories import UserFactory, TagFactory, TaskFactory


class TestTaskFilterSet(TestViewSetBase):
    basename = "tasks"
    user_attributes = UserFactory

    def setUp(self):
        self.author1 = UserFactory(username="author1")
        self.author2 = UserFactory(username="author2")

        self.assignee1 = UserFactory(username="assignee1")
        self.assignee2 = UserFactory(username="assignee2")

        self.tag1 = TagFactory(title="tag1")
        self.tag2 = TagFactory(title="tag2")

        self.task1 = TaskFactory(
            author=self.author1, assignee=self.assignee1, state="new_task"
        )
        self.task1.tags.add(self.tag1)

        self.task2 = TaskFactory(
            author=self.author1, assignee=self.assignee2, state="in_development"
        )
        self.task2.tags.add(self.tag2)

        self.task3 = TaskFactory(
            author=self.author2, assignee=self.assignee2, state="in_qa"
        )
        self.task3.tags.add(self.tag1)
        self.task3.tags.add(self.tag2)

    def test_state_field_filter(self):
        response = self.list({"state": self.task1.state})
        task_ids = [task["id"] for task in response]

        assert self.task1.id in task_ids
        assert self.task2.id not in task_ids
        assert self.task3.id not in task_ids

    def test_tags_field_filter(self):
        response = self.list({"tags": self.tag1.title})
        task_ids = [task["id"] for task in response]

        assert self.task1.id in task_ids
        assert self.task2.id not in task_ids
        assert self.task3.id in task_ids

    def test_author_field_filter(self):
        response = self.list({"author": self.task1.author.id})
        task_ids = [task["id"] for task in response]

        assert self.task1.id in task_ids
        assert self.task2.id in task_ids
        assert self.task3.id not in task_ids

    def test_assignee_field_filter(self):
        response = self.list({"assignee": self.task1.assignee.id})
        task_ids = [task["id"] for task in response]

        assert self.task1.id in task_ids
        assert self.task2.id not in task_ids
        assert self.task3.id not in task_ids

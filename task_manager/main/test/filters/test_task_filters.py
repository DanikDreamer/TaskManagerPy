import factory

from task_manager.main.test.base import TestViewSetBase
from task_manager.main.test.factoriess import UserFactory, TagFactory, TaskFactory


class TestTaskFilterSet(TestViewSetBase):
    basename = "tasks"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.author1 = UserFactory(username="author1")
        cls.author2 = UserFactory(username="author2")

        cls.assignee1 = UserFactory(username="assignee1")
        cls.assignee2 = UserFactory(username="assignee2")

        cls.tag1 = TagFactory(title="tag1")
        cls.tag2 = TagFactory(title="tag2")

        cls.task1 = TaskFactory(
            author=cls.author1, assignee=cls.assignee1, state="new_task"
        )
        cls.task1.tags.add(cls.tag1)

        cls.task2 = TaskFactory(
            author=cls.author1, assignee=cls.assignee2, state="in_development"
        )
        cls.task2.tags.add(cls.tag2)

        cls.task3 = TaskFactory(
            author=cls.author2, assignee=cls.assignee2, state="in_qa"
        )
        cls.task3.tags.add(cls.tag1)
        cls.task3.tags.add(cls.tag2)

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

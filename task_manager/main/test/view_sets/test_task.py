import factory

from base import TestViewSetBase
from factories import UserFactory, AdminFactory, TagFactory, TaskFactory


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"
    user_attributes = UserFactory

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

        self.create(task_attributes)

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

        self.delete(task.id)


class TestTaskNoAuthViewSet(TestViewSetBase):
    basename = "tasks"
    user_attributes = None

    def test_list(self):
        TaskFactory()

        self.list()

    def test_retrieve(self):
        task = TaskFactory()

        self.retrieve(task.id)

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

        self.create(task_attributes)

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

        self.delete(task.id)


class TestAdminOnlyDeleteTaskViewSet(TestViewSetBase):
    basename = "tasks"
    user_attributes = AdminFactory

    def test_delete(self):
        task = TaskFactory()

        self.delete(task.id)

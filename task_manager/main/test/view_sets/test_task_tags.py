import factory

from task_manager.main.models import Task
from task_manager.main.test.base import TestViewSetBase
from task_manager.main.test.factoriess import UserFactory, TagFactory


class TestUserTasksViewSet(TestViewSetBase):
    basename = "task_tags"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    def add_tags(self, task: dict, tags: list) -> None:
        task_instance = Task.objects.get(pk=task["id"])
        task_instance.tags.add(*self.get_tag_ids(tags))
        task_instance.save()

    def get_tag_ids(self, tags: list) -> list:
        return [tag["id"] for tag in tags]

    def test_list(self) -> None:
        task = self.action_client.create_task()
        tag1 = self.action_client.create_tag()
        tag2 = self.action_client.create_tag()
        self.add_tags(task, [tag1, tag2])

        tags = self.list(args=[task["id"]])

        assert tags == [tag1, tag2]

    def test_create(self) -> None:
        task = self.action_client.create_task()
        tag1_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)
        tag2_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

        tag1 = self.create(tag1_attributes, [task["id"]])
        tag2 = self.create(tag2_attributes, [task["id"]])
        tags = self.list(args=[task["id"]])

        assert [tag1, tag2] == tags

    def test_update(self) -> None:
        task = self.action_client.create_task()
        tag1 = self.action_client.create_tag()
        tag2 = self.action_client.create_tag()
        self.add_tags(task, [tag1, tag2])
        new_tag1_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)
        new_tag2_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

        updated_tag1 = self.update([task["id"], tag1["id"]], new_tag1_attributes)
        updated_tag2 = self.update([task["id"], tag2["id"]], new_tag2_attributes)
        tags = self.list(args=[task["id"]])

        assert [updated_tag1, updated_tag2] == tags

    def test_delete(self) -> None:
        task = self.action_client.create_task()
        tag = self.action_client.create_tag()
        self.add_tags(task, [tag])

        self.delete([task["id"], tag["id"]])

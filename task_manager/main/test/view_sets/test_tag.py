import factory

from base import TestViewSetBase
from factories import UserFactory, AdminFactory, TagFactory


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    user_attributes = UserFactory

    def test_list(self):
        tag = TagFactory()

        response = self.list()
        tag_titles = [tag["title"] for tag in response]

        assert tag.title in tag_titles

    def test_retrieve(self):
        tag = TagFactory()

        response = self.retrieve(tag.id)

        assert tag.title == response["title"]

    def test_create(self):
        tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

        self.create(tag_attributes)

    def test_update(self):
        tag = TagFactory()
        new_tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

        self.update(tag.id, new_tag_attributes)

    def test_delete(self):
        tag = TagFactory()

        self.delete(tag.id)


class TestTagNoAuthViewSet(TestViewSetBase):
    basename = "tags"
    user_attributes = None

    def test_list(self):
        TagFactory()

        self.list()

    def test_retrieve(self):
        tag = TagFactory()

        self.retrieve(tag.id)

    def test_create(self):
        tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

        self.create(tag_attributes)

    def test_update(self):
        tag = TagFactory()
        new_tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

        self.update(tag.id, new_tag_attributes)

    def test_delete(self):
        tag = TagFactory()

        self.delete(tag.id)


class TestAdminOnlyDeleteTagViewSet(TestViewSetBase):
    basename = "tags"
    user_attributes = AdminFactory

    def test_delete(self):
        tag = TagFactory()

        self.delete(tag.id)

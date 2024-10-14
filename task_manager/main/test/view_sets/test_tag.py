import factory
from http import HTTPStatus

from task_manager.main.test.base import TestViewSetBase
from task_manager.main.test.factories import UserFactory, AdminFactory, TagFactory


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

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

        response = self.request_delete(tag.id)

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestTagNoAuthViewSet(TestViewSetBase):
    basename = "tags"
    user_attributes = None

    def setUp(self):
        self.unauthenticate_user()

    def test_list(self):
        TagFactory()

        response = self.request_list()

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_retrieve(self):
        tag = TagFactory()

        response = self.request_retrieve(tag.id)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_create(self):
        tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

        response = self.request_create(tag_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_update(self):
        tag = TagFactory()
        new_tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

        response = self.request_update(tag.id, new_tag_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_delete(self):
        tag = TagFactory()

        response = self.request_delete(tag.id)

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestAdminOnlyDeleteTagViewSet(TestViewSetBase):
    basename = "tags"
    user_attributes = factory.build(dict, FACTORY_CLASS=AdminFactory)

    def test_delete(self):
        tag = TagFactory()

        self.delete(tag.id)

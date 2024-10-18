import factory
from http import HTTPStatus

from task_manager.main.test.base import TestViewSetBase
from task_manager.main.test.factoriess import UserFactory, AdminFactory, TagFactory


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_list(self):
        tag = TagFactory()

        response = self.list()
        tag_titles = [tag["title"] for tag in response]

        assert tag.title in tag_titles

    def test_retrieve(self):
        tag = TagFactory()

        response = self.retrieve([tag.id])

        assert tag.title == response["title"]

    def test_create(self):
        tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

        tag = self.create(tag_attributes)

        expected_response = self.expected_details(tag, tag_attributes)
        assert tag == expected_response

    def test_update(self):
        tag = TagFactory()
        new_tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

        updated_tag = self.update([tag.id], new_tag_attributes)

        expected_response = self.expected_details(updated_tag, new_tag_attributes)
        assert updated_tag == expected_response

    def test_delete(self):
        tag = TagFactory()

        response = self.request_delete([tag.id])

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

        response = self.request_retrieve([tag.id])

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_create(self):
        tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

        response = self.request_create(tag_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_update(self):
        tag = TagFactory()
        new_tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

        response = self.request_update([tag.id], new_tag_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_delete(self):
        tag = TagFactory()

        response = self.request_delete([tag.id])

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestAdminOnlyDeleteTagViewSet(TestViewSetBase):
    basename = "tags"
    user_attributes = factory.build(dict, FACTORY_CLASS=AdminFactory)

    def test_delete(self):
        tag = TagFactory()

        self.delete([tag.id])

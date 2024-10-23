import factory
from unittest.mock import patch, MagicMock

from django.core import mail
from django.template.loader import render_to_string

from task_manager.main.models import Task
from task_manager.main.services.mail import send_assign_notification
from task_manager.main.test.base import TestViewSetBase
from task_manager.main.test.factories import UserFactory


class TestSendEmail(TestViewSetBase):
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    @patch.object(mail, "send_mail")
    def test_send_assign_notification(self, fake_sender: MagicMock) -> None:
        assignee = self.action_client.create_user()
        task = self.action_client.create_task(assignee=assignee["id"])

        send_assign_notification(task["id"])

        fake_sender.assert_called_once_with(
            subject="You've assigned a task.",
            message="",
            from_email=None,
            recipient_list=[assignee["email"]],
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task["id"])},
            ),
        )

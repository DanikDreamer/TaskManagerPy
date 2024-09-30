from django.db import models
from .user import User


class Task(models.Model):
    class States(models.TextChoices):
        NEW_TASK = "new_task"
        IN_DEVELOPMENT = "in_development"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    class PriorityLevels(models.IntegerChoices):
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        CRITICAL = 4

    title = models.CharField(max_length=55)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    expired_at = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        User,
        related_name="authored_tasks",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    assignee = models.ForeignKey(
        User,
        related_name="assigned_tasks",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    state = models.CharField(
        max_length=255, default=States.NEW_TASK, choices=States.choices
    )
    priority = models.IntegerField(
        default=PriorityLevels.MEDIUM, choices=PriorityLevels.choices
    )

    def __str__(self):
        return f"Task(title={self.title})"

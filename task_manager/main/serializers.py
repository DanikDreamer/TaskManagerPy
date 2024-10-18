from django.conf import settings
from django.core.files.base import File
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User, Task, Tag


class FileMaxSizeValidator:
    def __init__(self, max_size: int) -> None:
        self.max_size = max_size

    def __call__(self, value: File) -> None:
        if value.size > self.max_size:
            raise ValidationError(f"Maximum size {self.max_size} exceeded.")


class UserSerializer(serializers.ModelSerializer):
    avatar_picture = serializers.FileField(
        required=False,
        validators=[
            FileMaxSizeValidator(settings.UPLOAD_MAX_SIZES["avatar_picture"]),
            FileExtensionValidator(["jpeg", "jpg", "png"]),
        ],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "date_of_birth",
            "phone",
            "avatar_picture",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "title")


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    state = serializers.ChoiceField(choices=Task.States.choices)
    priority = serializers.ChoiceField(choices=Task.PriorityLevels.choices)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "expired_at",
            "author",
            "assignee",
            "tags",
            "state",
            "priority",
        )

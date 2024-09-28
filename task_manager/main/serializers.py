from rest_framework import serializers
from .models import User, Task, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "phone",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "title")


class TaskSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    assignee = UserSerializer()
    tags = TagSerializer(many=True)
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

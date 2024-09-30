from rest_framework import viewsets
from .models import User, Tag, Task
from .serializers import UserSerializer, TagSerializer, TaskSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.select_related("authors", "assignee")
        .prefetch_related("tags")
        .order_by("id")
    )
    serializer_class = TaskSerializer

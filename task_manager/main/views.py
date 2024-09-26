import django_filters
from rest_framework import viewsets
from .models import User, Tag, Task
from .serializers import UserSerializer, TagSerializer, TaskSerializer


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("name",)


class TaskFilter(django_filters.FilterSet):
    state = django_filters.ChoiceFilter(choices=Task.States.choices)
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
    author = django_filters.ChoiceFilter(queryset=User.objects.all())
    assignee = django_filters.ChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ("state", "tags", "author", "assignee")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


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
    filterset_class = TaskFilter

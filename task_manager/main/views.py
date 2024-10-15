import django_filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User, Tag, Task
from .serializers import UserSerializer, TagSerializer, TaskSerializer
from .permissions import IsStaffOnlyForDelete


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("username",)


class TaskFilter(django_filters.FilterSet):
    state = django_filters.ChoiceFilter(choices=Task.States.choices)
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(), field_name="tags__title", to_field_name="title"
    )
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    assignee = django_filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ("state", "tags", "author", "assignee")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = [IsAuthenticated, IsStaffOnlyForDelete]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsStaffOnlyForDelete]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.select_related("author", "assignee")
        .prefetch_related("tags")
        .order_by("id")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = [IsAuthenticated, IsStaffOnlyForDelete]

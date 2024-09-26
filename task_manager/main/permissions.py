from rest_framework.permissions import BasePermission


class IsStaffOnlyForDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["DELETE"]:
            return request.user.is_staff

        return True

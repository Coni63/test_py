from rest_framework.permissions import BasePermission


class IsInGroup(BasePermission):
    """
    Allows access only to users in a specific group.
    """

    def has_permission(self, request, view):
        # Replace 'your_group_name' with the actual group name you want to check
        return request.user and request.user.groups.filter(name='testgroup').exists()
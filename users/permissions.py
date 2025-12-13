from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsNotModerator(permissions.BasePermission):
    """Проверяет, что пользователь не является модератором."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and not request.user.groups.filter(name="moderators").exists()
        )

class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False

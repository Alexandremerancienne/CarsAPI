from rest_framework import permissions


class IsSuperuserOrAdminOrCarUser(permissions.BasePermission):
    message = "Missing credentials: Car can be edited only by Admin or Car User."

    def has_permission(self, request, view):
        if (
            request.method == "POST"
            and request.user.role == ""
            and not request.user.is_superuser
        ):
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            True
            if request.user.is_superuser
            or request.user.role == "admin"
            or obj.user == request.user
            else False
        )


class IsSuperuserOrAdmin(permissions.BasePermission):
    message = (
        "Missing credentials: Brand/Model can be edited only by Admin or Superuser."
    )

    def has_permission(self, request, view):
        if request.method == "POST" and request.user.role == "client":
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            True if request.user.is_superuser or request.user.role == "admin" else False
        )


class IsSuperuserOrSelfAdminOrAnonymousUser(permissions.BasePermission):
    message = "Missing credentials: You cannot edit this user."

    def has_permission(self, request, view):
        if request.method == "POST":
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            True
            if request.user.is_superuser
            or request.user.role == "admin"
            or (request.user.role == "client" and request.user == obj)
            else False
        )

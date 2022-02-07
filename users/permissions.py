from rest_framework.permissions import BasePermission


class AccessPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.posted_by == request.user and (request.method in {'PUT', 'PATCH', 'DELETE'}):
            return True
        if request.method == 'GET':
            return True

        return False

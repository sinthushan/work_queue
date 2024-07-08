from rest_framework.permissions import BasePermission

class CanAddWorker(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.worker.permission_group > 1:
            return True
        return False
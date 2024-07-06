from rest_framework.permissions import BasePermission

class IsCreatorAsignee(BasePermission):
    def has_object_permission(self, request, view, obj):
        if (obj.creator == request.user.worker) or (obj.assigned_to == request.user.worker):
            return True
        return False
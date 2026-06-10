from rest_framework.permissions import BasePermission
from reports.models import Report


class IsOwnerAndDraft(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        # create hanya citizen
        if request.method == 'POST':
            return not request.user.is_staff

        return True


    def has_object_permission(self, request, view, obj):

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return (
            obj.reporter == request.user
            and obj.status == Report.Status.DRAFT
        )

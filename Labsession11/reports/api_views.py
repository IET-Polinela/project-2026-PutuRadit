from rest_framework import viewsets, permissions
from django.db.models import Q

from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraft


class ReportViewSet(viewsets.ModelViewSet):

    queryset = Report.objects.all()

    serializer_class = ReportSerializer


    def get_queryset(self):

        user = self.request.user

        return Report.objects.filter(
            Q(status=Report.Status.DRAFT, reporter=user)
            |
            ~Q(status=Report.Status.DRAFT)
        )


    def get_permissions(self):

        if self.action in [
            'update',
            'partial_update',
            'destroy'
        ]:
            return [
                permissions.IsAuthenticated(),
                IsOwnerAndDraft()
            ]

        return [
            permissions.IsAuthenticated()
        ]


    def perform_create(self, serializer):

        serializer.save(
            reporter=self.request.user
        )

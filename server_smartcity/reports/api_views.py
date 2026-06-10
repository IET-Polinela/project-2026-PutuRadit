from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraft


class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReportViewSet(viewsets.ModelViewSet):

    queryset = Report.objects.all()

    serializer_class = ReportSerializer

    pagination_class = ReportPagination

    def get_queryset(self):

        user = self.request.user

        return Report.objects.filter(
            Q(status=Report.Status.DRAFT, reporter=user)
            |
            ~Q(status=Report.Status.DRAFT)
        ).order_by('-created_at')

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

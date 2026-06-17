from django.db.models import Q

from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from drf_spectacular.utils import extend_schema

from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraft


# =========================
# PAGINATION
# =========================
class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# =========================
# REPORT API VIEWSET
# =========================
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    pagination_class = ReportPagination

    def get_queryset(self):
        """
        Menampilkan:
        1. Laporan DRAFT milik pengguna yang sedang login.
        2. Semua laporan yang statusnya bukan DRAFT.
        """

        # Digunakan agar proses generate schema OpenAPI tidak error
        if getattr(self, 'swagger_fake_view', False):
            return Report.objects.none()

        user = self.request.user

        if not user.is_authenticated:
            return Report.objects.filter(
                ~Q(status=Report.Status.DRAFT)
            ).order_by('-created_at')

        return Report.objects.filter(
            Q(
                status=Report.Status.DRAFT,
                reporter=user
            )
            |
            ~Q(status=Report.Status.DRAFT)
        ).order_by('-created_at')

    def get_permissions(self):
        """
        Update, partial update, dan delete hanya boleh dilakukan
        oleh pemilik laporan yang masih berstatus DRAFT.
        """

        if self.action in [
            'update',
            'partial_update',
            'destroy',
        ]:
            permission_classes = [
                permissions.IsAuthenticated,
                IsOwnerAndDraft,
            ]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    def perform_create(self, serializer):
        """
        Reporter otomatis diambil dari pengguna yang sedang login.
        """

        serializer.save(
            reporter=self.request.user
        )

    # Operasi DELETE tetap berfungsi, tetapi tidak ditampilkan
    # pada dokumentasi OpenAPI Swagger dan Scalar.
    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(
            request,
            *args,
            **kwargs
        )

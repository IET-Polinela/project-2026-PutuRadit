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


# LAB15 PATCH START
from django.db.models import Q as _LAB15_Q

def _lab15_status_value(name, default):
    status_cls = getattr(Report, "Status", None)
    return getattr(status_cls, name, default) if status_cls else default

def _lab15_report_queryset(self):
    qs = Report.objects.all().order_by("-created_at")
    user = self.request.user
    tab = self.request.query_params.get("tab")

    draft_value = _lab15_status_value("DRAFT", "DRAFT")

    if tab == "feed":
        return qs.exclude(status=draft_value)

    if not user or not user.is_authenticated:
        return qs.none()

    if tab == "my_reports":
        return qs.filter(reporter=user)

    return qs.filter(_LAB15_Q(reporter=user) | ~_LAB15_Q(status=draft_value))

def _lab15_report_perform_create(self, serializer):
    save_kwargs = {"reporter": self.request.user}

    # Di model kamu ada field user dan reporter, jadi isi dua-duanya saat create via API.
    if hasattr(Report, "user"):
        save_kwargs["user"] = self.request.user

    serializer.save(**save_kwargs)

ReportViewSet.get_queryset = _lab15_report_queryset
ReportViewSet.perform_create = _lab15_report_perform_create
# LAB15 PATCH END

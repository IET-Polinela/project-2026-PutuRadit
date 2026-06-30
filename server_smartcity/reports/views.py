from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Count, Q

from .models import Report
from .forms import ReportForm


# =========================
# MIXIN ADMIN ONLY
# =========================
class AdminOnlyMixin:
    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.error(request, "Silakan login dulu!")
            return redirect('login')

        if not request.user.is_admin:
            messages.error(request, "Akses ditolak! Hanya admin yang boleh akses fitur ini.")
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)


# =========================
# DASHBOARD VIEW
# =========================
class DashboardView(TemplateView):
    template_name = "dashboard_24782059/index.html"


# =========================
# LIST REPORT
# =========================
class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        user = self.request.user

        # Semua user login, termasuk admin:
        # - bisa lihat semua laporan NON-DRAFT
        # - bisa lihat DRAFT hanya miliknya sendiri
        return Report.objects.filter(
            Q(status=Report.Status.DRAFT, reporter=user) |
            ~Q(status=Report.Status.DRAFT)
        ).order_by('-created_at')


# =========================
# CREATE REPORT
# =========================
class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/add_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.reporter = self.request.user
        form.instance.status = Report.Status.DRAFT

        messages.success(
            self.request,
            "Laporan berhasil disimpan sebagai DRAFT!"
        )
        return super().form_valid(form)


# =========================
# UPDATE REPORT
# =========================
class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/update_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()

        if report.reporter != request.user or report.status != Report.Status.DRAFT:
            messages.error(
                request,
                "Akses ditolak! Laporan hanya bisa diedit oleh pemiliknya saat status masih DRAFT."
            )
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.status = Report.Status.DRAFT

        messages.success(
            self.request,
            "Laporan DRAFT berhasil diupdate!"
        )
        return super().form_valid(form)


# =========================
# DELETE REPORT
# =========================
class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'reports/delete_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()

        if report.reporter != request.user or report.status != Report.Status.DRAFT:
            messages.error(
                request,
                "Akses ditolak! Laporan hanya bisa dihapus oleh pemiliknya saat status masih DRAFT."
            )
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(
            request,
            "Laporan DRAFT berhasil dihapus!"
        )
        return super().delete(request, *args, **kwargs)


# =========================
# UPDATE STATUS / PUBLISH
# =========================
class ReportUpdateStatusView(LoginRequiredMixin, View):

    def post(self, request, pk):

        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')

        # Citizen pemilik laporan boleh publish DRAFT -> REPORTED
        if (
            report.reporter == request.user
            and report.status == Report.Status.DRAFT
            and new_status == Report.Status.REPORTED
        ):
            report.status = Report.Status.REPORTED
            report.save()

            messages.success(
                request,
                "Laporan berhasil dipublish!"
            )
            return redirect('report_list')

        # Admin hanya mengubah laporan yang sudah publish / non-DRAFT
        if request.user.is_admin:

            if report.status == Report.Status.DRAFT:
                messages.error(
                    request,
                    "Admin tidak dapat mengubah status laporan yang masih DRAFT."
                )
                return redirect('report_list')

            valid_transitions = {
                Report.Status.REPORTED: [Report.Status.VERIFIED],
                Report.Status.VERIFIED: [Report.Status.IN_PROGRESS],
                Report.Status.IN_PROGRESS: [Report.Status.RESOLVED],
                Report.Status.RESOLVED: []
            }

            if new_status in valid_transitions.get(report.status, []):

                report.status = new_status
                report.save()

                messages.success(
                    request,
                    f"Status laporan berhasil diubah ke {new_status}"
                )

            else:
                messages.error(
                    request,
                    "Perubahan status tidak valid!"
                )

            return redirect('report_list')

        messages.error(
            request,
            "Akses ditolak! Kamu tidak punya izin mengubah status laporan ini."
        )
        return redirect('report_list')


# =========================
# API DETAIL REPORT (MODAL)
# =========================
def report_detail_api(request, id):
    report = get_object_or_404(Report, id=id)

    if (
        report.status == Report.Status.DRAFT
        and report.reporter != request.user
    ):
        return JsonResponse(
            {"error": "Akses ditolak! Laporan DRAFT hanya bisa dilihat pemiliknya."},
            status=403
        )

    data = {
        "title": report.title,
        "description": report.description,
        "location": report.location,
        "category": report.category,
        "status": report.status,
        "created_at": report.created_at.strftime("%Y-%m-%d %H:%M"),
    }

    return JsonResponse(data)


# =========================
# API STATUS (CHART DOUGHNUT)
# =========================
def report_status_data(request):
    user = request.user

    reports = Report.objects.filter(
        Q(status=Report.Status.DRAFT, reporter=user) |
        ~Q(status=Report.Status.DRAFT)
    )

    data = (
        reports.values('status')
        .annotate(total=Count('id'))
    )

    result = {item['status']: item['total'] for item in data}
    return JsonResponse(result)


# =========================
# API CATEGORY (CHART BAR)
# =========================
def report_category_data(request):
    user = request.user

    reports = Report.objects.filter(
        Q(status=Report.Status.DRAFT, reporter=user) |
        ~Q(status=Report.Status.DRAFT)
    )

    data = (
        reports.values('category')
        .annotate(total=Count('id'))
    )

    result = {item['category']: item['total'] for item in data}
    return JsonResponse(result)


# =========================
# API RECENT (TABEL DASHBOARD)
# =========================
def recent_reports(request):
    reported = list(
        Report.objects.filter(status=Report.Status.REPORTED)
        .order_by('-created_at')[:5]
        .values('title', 'created_at')
    )

    resolved = list(
        Report.objects.filter(status=Report.Status.RESOLVED)
        .order_by('-created_at')[:5]
        .values('title', 'created_at')
    )

    return JsonResponse({
        "reported": reported,
        "resolved": resolved
    })


# =========================
# API LIVE SEARCH
# =========================
def report_search_api(request):
    query = request.GET.get('q', '')
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({'results': []}, status=200)

    reports = Report.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(category__icontains=query) |
        Q(location__icontains=query)
    )

    reports = reports.filter(
        Q(status=Report.Status.DRAFT, reporter=user) |
        ~Q(status=Report.Status.DRAFT)
    )

    reports = reports.order_by('-created_at')[:50]

    data = [
        {
            "id": r.id,
            "title": r.title,
            "description": r.description,
            "user": r.user.username if r.user else "-",
            "status": r.status,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for r in reports
    ]

    return JsonResponse(data, safe=False)

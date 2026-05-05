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
class ReportListView(ListView):
    model = Report
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return Report.objects.all().order_by('-created_at')


# =========================
# CREATE REPORT
# =========================
class ReportCreateView(AdminOnlyMixin, LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/add_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "REPORTED"
        messages.success(self.request, "Laporan berhasil ditambahkan!")
        return super().form_valid(form)


# =========================
# UPDATE REPORT
# =========================
class ReportUpdateView(AdminOnlyMixin, LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/update_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diupdate!")
        return super().form_valid(form)


# =========================
# DELETE REPORT
# =========================
class ReportDeleteView(AdminOnlyMixin, LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'reports/delete_report.html'
    success_url = reverse_lazy('report_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Laporan berhasil dihapus!")
        return super().delete(request, *args, **kwargs)


# =========================
# UPDATE STATUS
# =========================
class ReportUpdateStatusView(AdminOnlyMixin, LoginRequiredMixin, View):
    def post(self, request, pk):

        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')

        valid_transitions = {
            "REPORTED": ["VERIFIED"],
            "VERIFIED": ["IN_PROGRESS"],
            "IN_PROGRESS": ["RESOLVED"],
            "RESOLVED": []
        }

        if new_status in valid_transitions.get(report.status, []):
            report.status = new_status
            report.save()
            messages.success(request, f"Status diubah ke {new_status}")
        else:
            messages.error(request, "Perubahan status tidak valid!")

        return redirect('report_list')


# =========================
# API DETAIL REPORT (MODAL)
# =========================
def report_detail_api(request, id):
    report = get_object_or_404(Report, id=id)

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
    data = (
        Report.objects.values('status')
        .annotate(total=Count('id'))
    )

    result = {item['status']: item['total'] for item in data}
    return JsonResponse(result)


# =========================
# API CATEGORY (CHART BAR)
# =========================
def report_category_data(request):
    data = (
        Report.objects.values('category')
        .annotate(total=Count('id'))
    )

    result = {item['category']: item['total'] for item in data}
    return JsonResponse(result)


# =========================
# API RECENT (TABEL DASHBOARD)
# =========================
def recent_reports(request):
    reported = list(
        Report.objects.filter(status='REPORTED')
        .order_by('-created_at')[:5]
        .values('title', 'created_at')
    )

    resolved = list(
        Report.objects.filter(status='RESOLVED')
        .order_by('-created_at')[:5]
        .values('title', 'created_at')
    )

    return JsonResponse({
        "reported": reported,
        "resolved": resolved
    })


# =========================
# 🔥 API LIVE SEARCH (FIXED)
# =========================
def report_search_api(request):
    query = request.GET.get('q', '')

    reports = Report.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(category__icontains=query) |
        Q(location__icontains=query)
    ).order_by('-created_at')[:50]

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

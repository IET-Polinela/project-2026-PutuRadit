from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Report
from .forms import ReportForm


# =========================
# MIXIN ADMIN ONLY
# =========================
class AdminOnlyMixin:
    def dispatch(self, request, *args, **kwargs):

        # belum login
        if not request.user.is_authenticated:
            messages.error(request, "Silakan login dulu!")
            return redirect('login')

        # bukan admin
        if not request.user.is_admin:
            messages.error(request, "Akses ditolak! Hanya admin yang boleh mengakses fitur ini.")
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)


# =========================
# LIST REPORT (SEMUA USER BISA LIHAT)
# =========================
class ReportListView(ListView):
    model = Report
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return Report.objects.all().order_by('-created_at')


# =========================
# CREATE REPORT (ADMIN ONLY)
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
# UPDATE REPORT (ADMIN ONLY)
# =========================
class ReportUpdateView(AdminOnlyMixin, LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/update_report.html'
    success_url = reverse_lazy('report_list')

    def get_queryset(self):
        return Report.objects.all()

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diupdate!")
        return super().form_valid(form)


# =========================
# DELETE REPORT (ADMIN ONLY)
# =========================
class ReportDeleteView(AdminOnlyMixin, LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'reports/delete_report.html'
    success_url = reverse_lazy('report_list')

    def get_queryset(self):
        return Report.objects.all()

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Laporan berhasil dihapus!")
        return super().delete(request, *args, **kwargs)


# =========================
# UPDATE STATUS (ADMIN ONLY)
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

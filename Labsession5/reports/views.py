from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib import messages

from .models import Report
from .forms import ReportForm


# ABOUT PAGE
class AboutPageView(TemplateView):
    template_name = 'about/about.html'


# LIST REPORT
class ReportListView(ListView):
    model = Report
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'


# CREATE REPORT
class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/add_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        form.instance.status = "REPORTED"  # biar default aman
        messages.success(self.request, "Laporan berhasil ditambahkan!")
        return super().form_valid(form)


# UPDATE REPORT
class ReportUpdateView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/update_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diupdate!")
        return super().form_valid(form)


# DELETE REPORT
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'reports/delete_report.html'
    success_url = reverse_lazy('report_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Laporan berhasil dihapus!")
        return super().delete(request, *args, **kwargs)


# WORKFLOW UPDATE STATUS (FIXED + VALIDATION)
class ReportUpdateStatusView(View):
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

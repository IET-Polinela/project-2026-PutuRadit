from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Report
from .forms import ReportForm


# ABOUT PAGE
class AboutPageView(TemplateView):
    template_name = 'about/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = Report.objects.filter(status='VERIFIED')
        return context


# LIST REPORT
class ReportListView(ListView):
    model = Report
    template_name = 'about/report_list.html'
    context_object_name = 'reports'


# CREATE REPORT
class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'about/add_report.html'
    success_url = reverse_lazy('report_list')


# UPDATE REPORT
class ReportUpdateView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'about/update_report.html'
    success_url = reverse_lazy('report_list')


# DELETE REPORT
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'about/delete_report.html'
    success_url = reverse_lazy('report_list')


# WORKFLOW UPDATE STATUS
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        return redirect('report_list')

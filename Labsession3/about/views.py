from django.shortcuts import render, redirect, get_object_or_404
from .models import Report
from .forms import ReportForm

def about_page(request):
    reports = Report.objects.filter(status='APPROVED')
    return render(request, 'about/about.html', {'reports': reports})

def add_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'about/add_report.html', {'form': form})

def report_list(request):
    reports = Report.objects.all()
    return render(request, 'about/report_list.html', {'reports': reports})

def update_report(request, id):
    report = get_object_or_404(Report, id=id)
    if request.method == "POST":
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm(instance=report)
    return render(request, 'about/update_report.html', {'form': form, 'report': report})

def delete_report(request, id):
    report = get_object_or_404(Report, id=id)
    if request.method == "POST":
        report.delete()
        return redirect('report_list')
    return render(request, 'about/delete_report.html', {'report': report})


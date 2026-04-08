from django.urls import path
from .views import (
    AboutPageView,
    ReportListView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView,
)

urlpatterns = [
    # About Page
    path('', AboutPageView.as_view(), name='about'),

    # List Report
    path('reports/', ReportListView.as_view(), name='report_list'),

    # Create Report
    path('add/', ReportCreateView.as_view(), name='add_report'),

    # Update Report
    path('update/<int:pk>/', ReportUpdateView.as_view(), name='update_report'),

    # Delete Report
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='delete_report'),

    # Update Status (Workflow)
    path('update-status/<int:pk>/', ReportUpdateStatusView.as_view(), name='update_status'),
]

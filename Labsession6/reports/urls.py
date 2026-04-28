from django.urls import path
from .views import (
    ReportListView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView,
)

urlpatterns = [
    # LIST
    path('', ReportListView.as_view(), name='report_list'),

    # CREATE
    path('add/', ReportCreateView.as_view(), name='report_add'),

    # UPDATE
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='report_edit'),

    # DELETE
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='report_delete'),

    # UPDATE STATUS (ADMIN)
    path('status/<int:pk>/', ReportUpdateStatusView.as_view(), name='report_status'),
]

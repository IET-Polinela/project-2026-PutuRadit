from django.urls import path
from .views import (
    ReportListView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView,

    # API
    report_detail_api,
    report_status_data,
    report_category_data,
    recent_reports,
    report_search_api,

    # DASHBOARD
    DashboardView,
)

urlpatterns = [
    # =========================
    # REPORT CRUD
    # =========================
    path('', ReportListView.as_view(), name='report_list'),
    path('add/', ReportCreateView.as_view(), name='report_add'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='report_edit'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='report_delete'),
    path('status/<int:pk>/', ReportUpdateStatusView.as_view(), name='report_status'),

    # =========================
    # API DETAIL (MODAL)
    # =========================
    path('api/report/<int:id>/', report_detail_api, name='report_detail_api'),

    # =========================
    # LIVE SEARCH API
    # =========================
    path('api/search/', report_search_api, name='report_search_api'),

    # =========================
    # DASHBOARD PAGE
    # =========================
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # =========================
    # API DASHBOARD (CHART & TABLE)
    # =========================
    path('api/status/', report_status_data, name='report_status_data'),
    path('api/category/', report_category_data, name='report_category_data'),
    path('api/recent/', recent_reports, name='recent_reports'),
]

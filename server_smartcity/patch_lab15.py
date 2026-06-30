from pathlib import Path

files = list(Path("main_app/tests").glob("test_*.py"))

replacements = [
    ("from main_app.models import Report", "from reports.models import Report"),
    ("from mainapp.models import Report", "from reports.models import Report"),
    ("from mainapp.serializers import ReportSerializer", "from reports.serializers import ReportSerializer"),

    ("reverse('report-list')", "reverse('reports-list')"),
    ('reverse("report-list")', 'reverse("reports-list")'),

    ("reverse('add_report')", "reverse('report_add')"),
    ('reverse("add_report")', 'reverse("report_add")'),

    ("reverse('delete_report'", "reverse('report_delete'"),
    ('reverse("delete_report"', 'reverse("report_delete"'),

    ("reverse('update_report'", "reverse('report_edit'"),
    ('reverse("update_report"', 'reverse("report_edit"'),

    ("reverse('update_status'", "reverse('report_status'"),
    ('reverse("update_status"', 'reverse("report_status"'),

    ("reverse('report_detail'", "reverse('report_detail_api'"),
    ('reverse("report_detail"', 'reverse("report_detail_api"'),

    ("reverse('report_search')", "reverse('report_search_api')"),
    ('reverse("report_search")', 'reverse("report_search_api")'),

    ("from main_app.views import report_detail_api", "from reports.views import report_detail_api"),
    ("from main_app.views import ReportDeleteView", "from reports.views import ReportDeleteView"),

    ("'main_app/report_list.html'", "'reports/report_list.html'"),
    ('"main_app/report_list.html"', '"reports/report_list.html"'),

    ("serializer.data['reporter_name']", "serializer.data['reporter']"),
    ('serializer.data["reporter_name"]', 'serializer.data["reporter"]'),
    ("laporan['reporter_name']", "laporan['reporter']"),
    ('laporan["reporter_name"]', 'laporan["reporter"]'),
]

for p in files:
    text = p.read_text(encoding="utf-8")
    for old, new in replacements:
        text = text.replace(old, new)

    text = text.replace("self.client.get('/api/report/?tab=feed')", "self.client.get(reverse('reports-list') + '?tab=feed')")
    text = text.replace('self.client.get("/api/report/?tab=feed")', 'self.client.get(reverse("reports-list") + "?tab=feed")')

    text = text.replace("self.client.get('/api/report/?tab=my_reports')", "self.client.get(reverse('reports-list') + '?tab=my_reports')")
    text = text.replace('self.client.get("/api/report/?tab=my_reports")', 'self.client.get(reverse("reports-list") + "?tab=my_reports")')

    text = text.replace("f'/api/report/{self.draft_milik_b.pk}/'", "reverse('reports-detail', kwargs={'pk': self.draft_milik_b.pk})")
    text = text.replace("f'/api/report/{self.laporan_draft.pk}/'", "reverse('reports-detail', kwargs={'pk': self.laporan_draft.pk})")
    text = text.replace("f'/api/report/{self.laporan_reported.pk}/'", "reverse('reports-detail', kwargs={'pk': self.laporan_reported.pk})")
    text = text.replace("f'/api/report/{self.laporan_resolved.pk}/'", "reverse('reports-detail', kwargs={'pk': self.laporan_resolved.pk})")

    p.write_text(text, encoding="utf-8")

print(f"patched {len(files)} test files")

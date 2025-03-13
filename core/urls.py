from django.urls import path
from .views import dashboard, export_monthly_pdf, get_annual_report

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("export_monthly_pdf/", export_monthly_pdf, name="export_monthly_pdf"),
    path("annual-report/", get_annual_report, name="get_annual_report"),
]

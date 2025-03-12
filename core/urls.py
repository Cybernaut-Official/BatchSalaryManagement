from django.urls import path
from .views import dashboard, export_annual_pdf, export_monthly_pdf

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("export_monthly_pdf/", export_monthly_pdf, name="export_monthly_pdf"),
    path("export_annual_pdf/", export_annual_pdf, name="export_annual_pdf"),
]

from django.urls import path
from . import views

app_name = "payroll"

urlpatterns = [
    path("", views.PayrollDashboardView.as_view(), name="dashboard"),
    path("holerite/<int:pk>/selecionar/", views.PayslipSelectorView.as_view(), name="payslip_selector"),
    path("holerite/<int:pk>/", views.PayslipView.as_view(), name="payslip"),
    path("rescisao/", views.TerminationFormView.as_view(), name="termination_form"),
    path("rubricas/", views.RubricaReportView.as_view(), name="rubrica_report"),
]

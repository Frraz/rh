from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Payroll, PayrollItem, Termination


@admin.register(Payroll)
class PayrollAdmin(SimpleHistoryAdmin):
    list_display = ["entity", "reference_month", "reference_year", "status", "closed_at"]
    list_filter = ["status", "entity"]


@admin.register(PayrollItem)
class PayrollItemAdmin(admin.ModelAdmin):
    list_display = ["person", "payroll", "gross_salary", "net_salary"]
    search_fields = ["person__name"]


@admin.register(Termination)
class TerminationAdmin(admin.ModelAdmin):
    list_display = ["person", "termination_type", "termination_date", "net_total"]
    search_fields = ["person__name"]
    readonly_fields = ["created_at", "calculation_memory"]
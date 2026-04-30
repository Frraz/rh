from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Adjustment, DiscountInstallment


@admin.register(DiscountInstallment)
class DiscountInstallmentAdmin(SimpleHistoryAdmin):
    list_display = [
        "person",
        "installment_type",
        "description",
        "total_value",
        "num_installments",
        "installment_value",
        "first_reference_month",
        "first_reference_year",
    ]
    list_filter = ["installment_type"]
    search_fields = ["person__name", "description"]


@admin.register(Adjustment)
class AdjustmentAdmin(SimpleHistoryAdmin):
    list_display = [
        "person",
        "adjustment_type",
        "reference_month",
        "reference_year",
        "value",
        "origin",
    ]
    list_filter = ["adjustment_type", "origin", "reference_year"]
    search_fields = ["person__name", "description"]
    readonly_fields = ["created_at", "updated_at"]

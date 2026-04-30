from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Advance


@admin.register(Advance)
class AdvanceAdmin(SimpleHistoryAdmin):
    list_display = ["person", "requested_value", "approved_value", "status", "request_date"]
    list_filter = ["status"]
    search_fields = ["person__name"]
    readonly_fields = ["created_at", "updated_at", "reviewed_at"]
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import DocumentType, Document


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "has_expiry", "alert_days_before", "is_required"]
    search_fields = ["name"]


@admin.register(Document)
class DocumentAdmin(SimpleHistoryAdmin):
    list_display = ["person", "document_type", "status", "expiry_date"]
    list_filter = ["status", "document_type"]
    search_fields = ["person__name"]
    readonly_fields = ["created_at", "updated_at"]
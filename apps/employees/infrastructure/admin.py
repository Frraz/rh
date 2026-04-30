from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Entity, Farm, JobRole, Person


@admin.register(Entity)
class EntityAdmin(SimpleHistoryAdmin):
    list_display = ["name", "cnpj", "is_active"]
    search_fields = ["name", "cnpj"]
    list_filter = ["is_active"]


@admin.register(Farm)
class FarmAdmin(SimpleHistoryAdmin):
    list_display = ["name", "entity", "city", "is_active"]
    search_fields = ["name", "entity__name"]
    list_filter = ["entity", "is_active"]


@admin.register(JobRole)
class JobRoleAdmin(SimpleHistoryAdmin):
    list_display = ["name", "entity", "is_active"]
    search_fields = ["name"]
    list_filter = ["entity"]


@admin.register(Person)
class PersonAdmin(SimpleHistoryAdmin):
    list_display = ["name", "cpf", "person_type", "entity", "farm", "job_role", "status"]
    search_fields = ["name", "cpf"]
    list_filter = ["person_type", "status", "entity", "farm"]
    readonly_fields = ["created_at", "updated_at"]
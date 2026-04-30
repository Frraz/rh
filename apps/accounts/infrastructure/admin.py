from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from apps.accounts.infrastructure.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ["username", "first_name", "last_name", "email", "role", "is_active"]
    list_filter = ["role", "is_active"]
    search_fields = ["username", "first_name", "last_name", "email"]
    ordering = ["first_name", "last_name"]

    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Perfil RH", {"fields": ("role", "entity", "phone")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("Perfil RH", {"fields": ("role", "entity", "phone")}),
    )

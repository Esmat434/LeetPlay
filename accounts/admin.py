from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Password_Token

# Register your models here.

User = get_user_model()


@admin.register(User)
class CusUserAdmin(UserAdmin):
    list_display = ["username", "email", "is_superuser", "is_staff", "is_emailverified"]
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "birth_date",
                    "last_login_ip",
                    "avatar",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_emailverified",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "birth_date"),
            },
        ),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=...):
        return True

    def has_change_permission(self, request, obj=...):
        return True


@admin.register(Password_Token)
class PasswordTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "token", "created_at"]

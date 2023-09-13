from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Post


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("user_id", "is_staff", "is_active",)
    list_filter = ("user_id", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("user_id", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "user_id", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    ordering = ("user_id",)
    search_fields = ("user_id",)


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "writer", "is_active", "created_at")
    ordering = ("-created_at",)
    search_fields = ("title", "write",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post, PostAdmin)

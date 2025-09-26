from django.contrib import admin
from .models import Contestant, EmailVerificationToken, WinnerDraw

@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "is_verified", "created_at")
    list_filter = ("is_verified", "created_at")
    search_fields = ("first_name", "last_name", "second_last_name", "email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    # Sube la UX del admin
    date_hierarchy = "created_at"
    list_per_page = 50

    fieldsets = (
        ("Información Personal", {
            "fields": ("first_name", "last_name", "second_last_name", "email", "phone")
        }),
        ("Estado del Concurso", {
            "fields": ("is_verified", "user")
        }),
        ("Fechas", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ("contestant", "token", "created_at", "expires_at", "is_expired_flag", "used_at")
    list_filter = ("created_at", "expires_at", "used_at")
    search_fields = ("contestant__email", "contestant__first_name", "contestant__last_name")
    ordering = ("-created_at",)
    readonly_fields = ("token", "created_at", "expires_at")
    # Optimiza FK en listas
    list_select_related = ("contestant",)
    date_hierarchy = "created_at"
    list_per_page = 50

    def is_expired_flag(self, obj):
        return obj.is_expired()
    is_expired_flag.boolean = True
    is_expired_flag.short_description = "¿Expirado?"


@admin.register(WinnerDraw)
class WinnerDrawAdmin(admin.ModelAdmin):
    list_display = ("contestant", "drawn_at")
    list_filter = ("drawn_at",)
    search_fields = ("contestant__email", "contestant__first_name", "contestant__last_name")
    ordering = ("-drawn_at",)
    readonly_fields = ("drawn_at",)
    list_select_related = ("contestant",)
    date_hierarchy = "drawn_at"
    list_per_page = 50

    def has_add_permission(self, request):
        # Mantén True si quieres poder simular ganadores desde admin.
        # Déjalo en False (como Copilot) si quieres obligar el flujo real vía endpoint.
        return False

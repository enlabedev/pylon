from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Contacts, User


# Inline para Contactos
class ContactsInline(admin.StackedInline):
    model = Contacts
    extra = 1  # Número de formularios vacíos a mostrar


# Personalización del Admin para el modelo User
class UserAdmin(BaseUserAdmin):
    list_display = (
        "document_type",
        "document_number",
        "first_name",
        "father_surname",
        "maternal_surname",
        "email",
        "is_staff",
        "is_superuser",
        "is_verified",
    )
    search_fields = (
        "document_number",
        "first_name",
        "father_surname",
        "maternal_surname",
        "email",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_verified",
        "document_type",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Información Personal",
            {
                "fields": (
                    "document_type",
                    "document_number",
                    "first_name",
                    "father_surname",
                    "maternal_surname",
                    "phone",
                    "mobile",
                    "is_verified",
                )
            },
        ),
        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Fechas Importantes", {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ("last_login", "date_joined")
    inlines = [ContactsInline]


# Personalización del Admin para el modelo Contacts
class ContactsAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "father_surname",
        "maternal_surname",
        "relationship",
        "phone",
        "mobile",
        "user",
    )
    search_fields = (
        "first_name",
        "father_surname",
        "maternal_surname",
        "phone",
        "mobile",
    )
    list_filter = ("relationship",)


admin.site.register(User, UserAdmin)

# Registrar el modelo Contacts con la personalización
admin.site.register(Contacts, ContactsAdmin)

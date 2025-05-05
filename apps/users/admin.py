from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import Contacts, User


class ContactsInline(admin.StackedInline):
    model = Contacts
    extra = 1  # Número de formularios vacíos a mostrar


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
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
    # Fieldsets para la vista de cambio de usuario
    fieldsets = (
        (None, {"fields": ("password",)}),  # La contraseña se maneja por el formulario
        (
            _("Personal Information"),
            {
                "fields": (
                    "email",
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
            _("Address Information"),
            {
                "fields": (
                    "department",
                    "province",
                    "district",
                    "address",
                    "street",
                    "zip_code",
                    "reference",
                    "latitude",
                    "longitude",
                )
            },
        ),
        (
            _("Permissions"),
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
        (_("Date Important"), {"fields": ("last_login", "date_joined")}),
    )
    # Fieldsets para la vista de creación de usuario
    add_fieldsets = (
        (
            None,
            {"fields": ("email", "password", "password2")},
        ),
        (
            _("Información Personal"),
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
            _("Address Information"),
            {
                "fields": (
                    "department",
                    "province",
                    "district",
                    "address",
                    "street",
                    "zip_code",
                    "reference",
                    "latitude",
                    "longitude",
                )
            },
        ),
        (
            _("Permissions"),
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
    )
    readonly_fields = ("last_login", "date_joined")
    inlines = [ContactsInline]


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

admin.site.register(Contacts, ContactsAdmin)

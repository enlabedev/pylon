from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from apps.core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from apps.users import choices


class User(BaseModel, AbstractUser):
    # Campos base personalizados
    first_name = models.CharField(_("Nombres"), max_length=150)
    last_name = models.CharField(_("Apellido Paterno"), max_length=150)
    maternal_surname = models.CharField(
        _("Apellido Materno"), max_length=150, blank=True
    )

    # Campos adicionales
    document_type = models.CharField(
        _("Tipo de Documento"),
        max_length=10,
        choices=choices.DocumentTypeChoices.choices,
        default=choices.DocumentTypeChoices.DNI.value,
    )
    document_number = models.CharField(
        _("Número de Documento"),
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[0-9]{8,12}$", message=_("Formato de documento inválido")
            )
        ],
    )
    ubigeo = models.CharField(
        _("Ubigeo"),
        max_length=6,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^[0-9]{6}$", message=_("Ubigeo debe tener 6 dígitos")
            )
        ],
    )
    current_address = models.TextField(_("Dirección Actual"))
    address_reference = models.TextField(_("Referencia"), blank=True)
    phone = models.CharField(
        _("Teléfono"),
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^\+?[0-9]{9,15}$", message=_("Formato de teléfono inválido")
            )
        ],
    )
    emergency_contact = models.JSONField(
        _("Contacto de Emergencia"), default=dict, blank=True
    )
    is_verified = models.BooleanField(_("Verificado"), default=False)

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")
        constraints = [
            models.UniqueConstraint(
                fields=["document_type", "document_number"], name="unique_document"
            )
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.document_number})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name} {self.maternal_surname}".strip()

    def get_short_name(self):
        return f"{self.first_name} {self.last_name}"

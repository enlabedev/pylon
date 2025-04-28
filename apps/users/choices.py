from django.db import models
from django.utils.translation import gettext_lazy as _


class DocumentTypeChoices(models.TextChoices):
    DNI = "DNI", _("Documento Nacional de Identidad")
    CE = "CE", _("Carnet de Extranjería")
    PASAPORTE = "PASAPORTE", _("Pasaporte")


class EmergencyContactTypeChoices(models.TextChoices):
    FAMILIAR = "FAMILIAR", _("Familiar")
    AMIGO = "AMIGO", _("Amigo")
    VECINO = "VECINO", _("Vecino")
    OTRO = "OTRO", _("Otro")

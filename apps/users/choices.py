from django.db import models
from django.utils.translation import gettext_lazy as _


class DocumentTypeChoices(models.TextChoices):
    DNI = "ID", _("National Identity Document")
    CE = "FC", _("Foreigner's Card")
    PASSPORT = "PASSPORT", _("Passport")


class RelationshipChoices(models.TextChoices):
    FAMILY = "FAMILY", _("Family")
    FRIEND = "FRIEND", _("Friend")
    NEIGHBOR = "NEIGHBOR", _("Neighbor")
    OTHER = "OTHER", _("Other")

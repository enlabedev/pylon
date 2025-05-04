from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AddressModel, BaseModel
from apps.users import choices
from apps.users.managers import UserManager


class PeopleMixin(AddressModel, BaseModel):
    """
    Mixin to add people fields to a model.
    """

    first_name = models.CharField(_("First Nane"), max_length=150)
    father_surname = models.CharField(_("Father Surname "), max_length=150)
    maternal_surname = models.CharField(_("Mather Surname"), max_length=150, blank=True)

    # Campos adicionales
    document_type = models.CharField(
        _("Document Type"),
        max_length=10,
        choices=choices.DocumentTypeChoices.choices,
        default=choices.DocumentTypeChoices.DNI.value,
    )
    document_number = models.CharField(
        _("Document Number"),
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(regex=r"^[0-9]{8,12}$", message=_("Document number invalid"))
        ],
    )

    phone = models.CharField(
        _("Phone"),
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(regex=r"^0[0-9]{8}$", message=_("Phone number invalid"))
        ],
    )

    mobile = models.CharField(
        _("Mobile"),
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(regex=r"^9[0-9]{8}$", message=_("Mobile number invalid"))
        ],
    )

    class Meta:
        abstract = True
        verbose_name = _("People")
        verbose_name_plural = _("People")
        ordering = ["first_name", "father_surname", "maternal_surname"]


class User(
    PeopleMixin,
    AbstractUser,
    BaseModel,
):
    is_verified = models.BooleanField(_("Verificado"), default=False)

    objects: UserManager = UserManager()
    all_objects = models.Manager()

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
        return (
            f"{self.first_name} {self.father_surname} {self.maternal_surname}".strip()
        )

    def get_short_name(self):
        return f"{self.first_name} {self.father_surname}"


class Contacts(PeopleMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="contacts",
        verbose_name=_("User"),
    )
    relationship = models.CharField(
        _("Relationship"),
        max_length=50,
        choices=choices.RelationshipChoices.choices,
        default=choices.RelationshipChoices.FAMILY.value,
    )

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = ["father_surname"]

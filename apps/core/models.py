import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class SoftDeleteQuerySet(models.QuerySet):
    def active(self):
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).active()


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Fecha de creación")
    )
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Fecha de modificación")
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Fecha de eliminación")
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    @property
    def is_active(self):
        return self.deleted_at is None


class Department(BaseModel):
    name = models.CharField(
        max_length=100, unique=True, blank=False, null=False, verbose_name=_("Name")
    )


class Province(BaseModel):
    name = models.CharField(
        max_length=100, unique=True, blank=False, null=False, verbose_name=_("Name")
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="provinces",
        verbose_name=_("Department"),
    )

    def __str__(self):
        return self.name


class District(BaseModel):
    name = models.CharField(
        max_length=100, unique=True, blank=False, null=False, verbose_name=_("Name")
    )
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="districts",
        verbose_name=_("Province"),
    )

    def __str__(self):
        return self.name


class AddressModel(BaseModel):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_addresses",
        verbose_name=_("Department"),
    )
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_addresses",
        verbose_name=_("Province"),
    )
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_addresses",
        verbose_name=_("District"),
    )
    address = models.CharField(max_length=255, verbose_name=_("Address"))
    street = models.CharField(max_length=255, verbose_name=_("Street"))
    zip_code = models.CharField(max_length=20, verbose_name=_("Zip Code"))
    reference = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Reference")
    )
    latitude = models.FloatField(blank=True, null=True, verbose_name=_("Latitude"))
    longitude = models.FloatField(blank=True, null=True, verbose_name=_("Longitude"))

    @property
    def full_address(self):
        district_name = self.district.name if self.district else _("Unknown District")
        province_name = self.province.name if self.province else _("Unknown Province")
        department_name = (
            self.department.name if self.department else _("Unknown Department")
        )
        return f"{self.address}, {self.street}, {district_name}, {province_name}, {department_name}, {self.zip_code}"

    @property
    def full_address_with_reference(self):
        return (
            f"{self.full_address}, {self.reference}"
            if self.reference
            else self.full_address
        )

    @property
    def full_address_with_coordinates(self):
        return f"{self.full_address}, Lat: {self.latitude}, Lon: {self.longitude}"

    @property
    def full_address_with_reference_and_coordinates(self):
        return (
            f"{self.full_address_with_reference}, Lat: {self.latitude}, Lon: {self.longitude}"
            if self.latitude and self.longitude
            else self.full_address_with_reference
        )

    def validate_province(self):
        if self.province and self.province.department != self.department:
            raise ValueError(_("Province does not belong to the selected department."))

    def validate_district(self):
        if self.district and self.district.province != self.province:
            raise ValueError(_("District does not belong to the selected province."))

    class Meta:
        abstract = True

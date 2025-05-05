from django.db import models

from apps.core.models import BaseModel
from apps.users.models import User


class Building(BaseModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Tower(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    no_departments = models.IntegerField(blank=False, null=False)
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name="towers",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} - {self.no_departments} departments"


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    tower = models.ForeignKey(Tower, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="departments",
    )

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "tower")
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ["name"]

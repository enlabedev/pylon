from django.contrib.auth.models import BaseUserManager
from apps.core.models import SoftDeleteManager


class UserManager(BaseUserManager, SoftDeleteManager):
    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un usuario regular con los campos dados"""
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Crea y guarda un superusuario con los campos dados"""
        return self._create_user(email, password, True, True, **extra_fields)

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """Implementación central de creación de usuarios"""
        if not email:
            raise ValueError("El email debe ser proporcionado")

        email = self.normalize_email(email)
        user = self.model(
            email=email, is_staff=is_staff, is_superuser=is_superuser, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

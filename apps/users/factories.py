import logging
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from faker import Faker

from .choices import DocumentTypeChoices

logger = logging.getLogger(__name__)
User = get_user_model()
fake = Faker("es_ES")


class UserFactory:
    @classmethod
    def create_superuser(
        cls, document_number=None, email=None, password=None
    ):
        try:
            if not document_number:
                document_number = fake.unique.numerify("########")
            if not email:
                email = fake.unique.email()
            if not password:
                password = "pylon.admin.2025"
            return User.objects.create_superuser(
                email=email,
                password=password,
                document_type=DocumentTypeChoices.DNI,
                document_number=document_number,
                username=document_number,
                first_name="Admin",
                father_surname="Pylon",
                maternal_surname="Sistema",
                # Eliminar is_superuser=is_superuser
            )
        except Exception as e:
            logger.error(f"Error creando superusuario: {str(e)}")
            pass

    @classmethod
    def create_user(
        cls, document_number=None, email=None, password=None, is_staff=False
    ):
        try:
            if not document_number:
                document_number = fake.unique.numerify("########")
            if not email:
                email = fake.unique.email()
            if not password:
                password = "pylon.user.2025"
            return User.objects.create_user(
                email=email,
                password=password,
                document_type=DocumentTypeChoices.DNI,
                document_number=document_number,
                username=document_number,
                first_name=fake.first_name(),
                father_surname=fake.last_name(),
                maternal_surname=fake.last_name(),
                # Eliminar is_staff=is_staff
            )
        except Exception as e:
            logger.error(f"Error creando usuario: {str(e)}")
            pass

    @classmethod
    def create_test_users(cls, quantity=5):
        users = []
        for _ in range(quantity):
            try:
                users.append(cls.create_user())
            except Exception as e:
                logger.error(f"Error creando usuario: {str(e)}")
        return users

    @classmethod
    def validate_environment(cls, env):
        if env == "prod" and not settings.DEBUG:
            raise ValueError("Seeding en producción requiere DEBUG=True")

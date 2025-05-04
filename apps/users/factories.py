from django.contrib.auth import get_user_model
from django.conf import settings
from faker import Faker
import random
import logging
from .choices import DocumentTypeChoices

logger = logging.getLogger(__name__)
User = get_user_model()
fake = Faker("es_ES")


class UserFactory:
    @classmethod
    def create_superuser(cls):
        try:
            return User.objects.create_superuser(
                email="admin@pylon.pe",
                password="pylon.admin.2025",
                document_type=DocumentTypeChoices.DNI,
                document_number="00000000",
                username="00000000",
                first_name="Admin",
                last_name="Pylon",
                maternal_surname="Sistema",
                current_address="Av. Principal 123, Lima",
                ubigeo="150101",
            )
        except Exception as e:
            logger.error(f"Error creando superusuario: {str(e)}")
            pass

    @classmethod
    def create_test_users(cls, quantity=5):
        users = []
        for _ in range(quantity):
            try:
                document_number = fake.unique.numerify("########")
                user_data = {
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "maternal_surname": fake.last_name(),
                    "document_type": random.choice(
                        [dt.value for dt in DocumentTypeChoices]
                    ),
                    "document_number": document_number,
                    "username": document_number,
                    "ubigeo": fake.numerify("######"),
                    "current_address": fake.address(),
                    "email": fake.unique.email(),
                    "password": "pylon.user.2025",
                }
                users.append(User.objects.create_user(**user_data))
            except Exception as e:
                logger.error(f"Error creando usuario: {str(e)}")
        return users

    @classmethod
    def validate_environment(cls, env):
        if env == "prod" and not settings.DEBUG:
            raise ValueError("Seeding en producción requiere DEBUG=True")

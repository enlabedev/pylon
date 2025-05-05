import logging
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .models import User

logger = logging.getLogger(__name__)

class UserAdminCreationForm(UserCreationForm):
    """
    Formulario personalizado para la creación de usuarios en el admin.
    Incluye campos adicionales y lógica para propietarios.
    """
    class Meta:
        model = User
        fields = (
            "email",
            "document_type",
            "document_number",
            "first_name",
            "father_surname",
            "maternal_surname",
            "phone",
            "mobile",
            "department",
            "province",
            "district",
            "address",
            "street",
            "zip_code",
            "reference",
            "latitude",
            "longitude",
            "is_verified",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)

        # Lógica para propietarios
        user.is_staff = False
        user.is_superuser = False

        # Generación automática de username (basado en document_number)
        if not user.username:
            user.username = user.document_number

        # Generación automática de password segura
        generated_password = User.objects.make_random_password()
        user.set_password(generated_password)

        if commit:
            user.save()

            # Asignar a grupo de Propietarios si existe
            try:
                proprietario_group = Group.objects.get(name='Propietario')
                user.groups.add(proprietario_group)
            except Group.DoesNotExist:
                logger.warning("El grupo 'Propietario' no existe. No se asignó al usuario.")
                # TODO: [PYLON-XXX] Considerar crear el grupo si no existe o manejar este caso

            # Envío síncrono de correo de bienvenida con credenciales
            try:
                subject = _("Bienvenido a Pylon - Tu cuenta ha sido creada")
                message = render_to_string('emails/welcome_owner.txt', {
                    'user': user,
                    'password': generated_password,
                    'login_url': settings.LOGIN_URL # Asumiendo que LOGIN_URL está definido en settings
                })
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL, # Asumiendo que DEFAULT_FROM_EMAIL está definido en settings
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"Error enviando correo de bienvenida a {user.email}: {str(e)}")
                # TODO: [PYLON-XXX] Considerar reintentar el envío o notificar al administrador

        return user

class UserAdminChangeForm(UserChangeForm):
    """
    Formulario personalizado para la edición de usuarios en el admin.
    """
    class Meta:
        model = User
        fields = (
            "email",
            "document_type",
            "document_number",
            "first_name",
            "father_surname",
            "maternal_surname",
            "phone",
            "mobile",
            "department",
            "province",
            "district",
            "address",
            "street",
            "zip_code",
            "reference",
            "latitude",
            "longitude",
            "is_verified",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )

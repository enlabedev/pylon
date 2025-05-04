from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from apps.users.factories import UserFactory


class Command(BaseCommand):
    help = _("Crea usuarios iniciales para el sistema")

    def add_arguments(self, parser):
        parser.add_argument(
            "--env",
            type=str,
            default="dev",
            choices=["dev", "prod"],
            help=_("Entorno de ejecución: dev o prod"),
        )

    def handle(self, *args, **options):
        env = options["env"]

        try:
            UserFactory.validate_environment(env)

            self.stdout.write(
                self.style.SUCCESS(_(f"Iniciando seeding para entorno {env}"))
            )

            # Superusuario
            admin = UserFactory.create_superuser()
            if admin:
                self.stdout.write(
                    self.style.SUCCESS(_(f"Superusuario creado: {admin.email}"))
                )
            else:
                self.stdout.write(
                    self.style.ERROR(_("No se pudo crear el superusuario"))
                )

            # Usuarios de prueba solo en desarrollo
            if env == "dev":
                users = UserFactory.create_test_users(quantity=5)
                self.stdout.write(
                    self.style.SUCCESS(_(f"Se crearon {len(users)} usuarios de prueba"))
                )

            self.stdout.write(self.style.SUCCESS(_("Seeding completado exitosamente")))

        except Exception as e:
            self.stdout.write(self.style.ERROR(_(f"Error en seeding: {str(e)}")))

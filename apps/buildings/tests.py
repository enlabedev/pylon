from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.test import TestCase
from django.test.client import RequestFactory  # Importar RequestFactory
from django.urls import reverse
from guardian.shortcuts import assign_perm, get_perms, get_perms_for_model, remove_perm

from apps.users.factories import UserFactory

from .admin import DepartmentAdmin  # Importar la clase DepartmentAdmin
from .models import Building, Department, Tower

User = get_user_model()


class DepartmentPermissionsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.superuser: AbstractUser | None = UserFactory.create_superuser(
            document_number=99999999
        )
        self.assertIsNotNone(self.superuser, "Superuser creation failed.")
        self.owner_user = UserFactory.create_user(
            document_number=11111111, is_staff=True
        )
        self.other_user = UserFactory.create_user(
            document_number=22222222, is_staff=True
        )
        self.non_staff_user: AbstractUser | None = UserFactory.create_user(
            document_number=33333333, is_staff=False
        )

        self.building = Building.objects.create(name="Building 1")
        self.tower = Tower.objects.create(
            name="Tower 1", no_departments=10, building=self.building
        )
        self.department_owner = Department.objects.create(
            name="Department Owner", tower=self.tower, owner=self.owner_user
        )
        self.department_other = Department.objects.create(
            name="Department Other", tower=self.tower, owner=self.other_user
        )
        self.department_owner.save()
        self.department_other.save()

    def test_permissions_assigned_on_save(self):
        """Verifica que los permisos se asignan al propietario al guardar."""
        perms = get_perms(self.owner_user, self.department_owner)
        self.assertIn("view_department", perms)
        self.assertIn("change_department", perms)
        self.assertNotIn("delete_department", perms)
        perms_other_dept = get_perms(self.owner_user, self.department_other)
        self.assertNotIn("view_department", perms_other_dept)
        self.assertNotIn("change_department", perms_other_dept)
        self.assertNotIn("delete_department", perms_other_dept)
        perms_other_user = get_perms(self.other_user, self.department_owner)
        self.assertNotIn("view_department", perms_other_user)
        self.assertNotIn("change_department", perms_other_user)
        self.assertNotIn("delete_department", perms_other_user)

    def test_superuser_has_all_permissions(self):
        """Verifica que el superusuario tiene todos los permisos."""
        self.assertIsNotNone(self.superuser, "Superuser is None.")
        self.assertTrue(
            self.superuser
            and self.superuser.has_perm("view_department", self.department_owner)
        )
        self.assertTrue(
            self.superuser
            and self.superuser.has_perm("change_department", self.department_owner)
        )
        self.assertTrue(
            self.superuser
            and self.superuser.has_perm("delete_department", self.department_owner)
        )
        self.assertTrue(
            self.superuser
            and self.superuser.has_perm("view_department", self.department_other)
        )
        self.assertTrue(
            self.superuser
            and self.superuser.has_perm("change_department", self.department_other)
        )
        self.assertTrue(
            self.superuser
            and self.superuser.has_perm("delete_department", self.department_other)
        )

    def test_owner_can_view_and_change_own_department(self):
        """Verifica que el propietario puede ver y cambiar su propio departamento."""
        self.assertTrue(
            self.owner_user
            and self.owner_user.has_perm("view_department", self.department_owner)
        )
        self.assertTrue(
            self.owner_user
            and self.owner_user.has_perm("change_department", self.department_owner)
        )
        self.assertFalse(
            self.owner_user
            and self.owner_user.has_perm("delete_department", self.department_owner)
        )

    def test_owner_cannot_view_or_change_other_departments(self):
        """Verifica que el propietario no puede ver ni cambiar departamentos de otros."""
        self.assertFalse(
            self.owner_user
            and self.owner_user.has_perm("view_department", self.department_other)
        )
        self.assertFalse(
            self.owner_user
            and self.owner_user.has_perm("change_department", self.department_other)
        )
        self.assertFalse(
            self.owner_user
            and self.owner_user.has_perm("delete_department", self.department_other)
        )

    def test_other_staff_cannot_view_or_change_departments(self):
        """Verifica que otro usuario staff no propietario no puede ver ni cambiar departamentos."""
        self.assertFalse(
            self.other_user
            and self.other_user.has_perm("view_department", self.department_owner)
        )
        self.assertFalse(
            self.other_user
            and self.other_user.has_perm("change_department", self.department_owner)
        )
        self.assertFalse(
            self.other_user
            and self.other_user.has_perm("delete_department", self.department_owner)
        )
        self.assertFalse(
            self.other_user
            and self.other_user.has_perm("view_department", self.department_owner)
        )
        self.assertFalse(
            self.other_user
            and self.other_user.has_perm("change_department", self.department_owner)
        )
        self.assertFalse(
            self.other_user
            and self.other_user.has_perm("delete_department", self.department_owner)
        )

    def test_department_admin_queryset_for_owner(self):
        """Verifica que el queryset del admin para un propietario solo muestra sus departamentos."""
        site = AdminSite()
        department_admin = DepartmentAdmin(Department, site)
        request = self.factory.get("/")
        assert self.owner_user is not None, "Owner user is None."
        request.user = self.owner_user  # Adjuntar el usuario
        queryset = department_admin.get_queryset(request)
        self.assertEqual(queryset.count(), 1)
        self.assertIn(self.department_owner, queryset)
        self.assertNotIn(self.department_other, queryset)

    def test_department_admin_queryset_for_superuser(self):
        """Verifica que el queryset del admin para un superusuario muestra todos los departamentos."""
        site = AdminSite()
        department_admin = DepartmentAdmin(Department, site)
        request = self.factory.get("/")
        assert self.superuser is not None, "Superuser is None."
        request.user = self.superuser
        queryset = department_admin.get_queryset(request)
        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.department_owner, queryset)
        self.assertIn(self.department_other, queryset)

    def test_department_admin_has_permission_for_owner(self):
        """Verifica los permisos en el admin para un propietario."""
        site = AdminSite()
        department_admin = DepartmentAdmin(Department, site)
        request = self.factory.get("/")
        assert self.owner_user is not None, "Owner user is None."
        request.user = self.owner_user

        self.assertTrue(
            department_admin.has_view_permission(request, obj=self.department_owner)
        )
        self.assertTrue(
            department_admin.has_change_permission(request, obj=self.department_owner)
        )
        self.assertFalse(
            department_admin.has_delete_permission(request, obj=self.department_owner)
        )

        self.assertFalse(
            department_admin.has_view_permission(request, obj=self.department_other)
        )
        self.assertFalse(
            department_admin.has_change_permission(request, obj=self.department_other)
        )
        self.assertFalse(
            department_admin.has_delete_permission(request, obj=self.department_other)
        )

    def test_department_admin_has_permission_for_other_staff(self):
        """Verifica los permisos en el admin para otro usuario staff no propietario."""
        site = AdminSite()
        department_admin = DepartmentAdmin(Department, site)
        request = self.factory.get("/")
        assert self.other_user is not None, "Other user is None."
        request.user = self.other_user
        self.assertFalse(
            department_admin.has_view_permission(request, obj=self.department_owner)
        )
        self.assertFalse(
            department_admin.has_change_permission(request, obj=self.department_owner)
        )
        self.assertFalse(
            department_admin.has_delete_permission(request, obj=self.department_owner)
        )
        self.assertTrue(
            department_admin.has_view_permission(request, obj=self.department_other)
        )
        self.assertTrue(
            department_admin.has_change_permission(request, obj=self.department_other)
        )
        self.assertFalse(
            department_admin.has_delete_permission(request, obj=self.department_other)
        )

    def test_department_admin_has_permission_for_superuser(self):
        """Verifica los permisos en el admin para un superusuario."""
        site = AdminSite()
        department_admin = DepartmentAdmin(Department, site)
        request = self.factory.get("/")
        assert self.superuser is not None, "Superuser is None."
        request.user = self.superuser

        self.assertTrue(
            department_admin.has_view_permission(request, obj=self.department_owner)
        )
        self.assertTrue(
            department_admin.has_change_permission(request, obj=self.department_owner)
        )
        self.assertTrue(
            department_admin.has_delete_permission(request, obj=self.department_owner)
        )
        self.assertTrue(
            department_admin.has_view_permission(request, obj=self.department_other)
        )
        self.assertTrue(
            department_admin.has_change_permission(request, obj=self.department_other)
        )
        self.assertTrue(
            department_admin.has_delete_permission(request, obj=self.department_other)
        )

    def test_non_staff_user_cannot_access_admin(self):
        """Verifica que un usuario no staff no puede acceder al admin."""
        site = AdminSite()
        department_admin = DepartmentAdmin(Department, site)
        request = self.factory.get("/")
        assert self.non_staff_user is not None, "Non-staff user is None."
        request.user = self.non_staff_user

        self.assertFalse(department_admin.has_module_permission(request))

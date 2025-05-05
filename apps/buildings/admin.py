from django.contrib import admin
from django.contrib.auth import get_user_model
from guardian.admin import GuardedModelAdmin

from .models import Building, Department, Tower

User = get_user_model()

# Register your models here.
admin.site.register(Building)
admin.site.register(Tower)


class DepartmentAdmin(GuardedModelAdmin):
    def has_view_permission(self, request, obj=None):
        if getattr(request.user, "is_superuser", False):
            return True
        if obj is None:
            return True  # acceso a la lista
        return isinstance(request.user, User) and request.user.has_perm(
            "view_department", obj
        )

    def has_change_permission(self, request, obj=None):
        if isinstance(request.user, User) and getattr(
            request.user, "is_superuser", False
        ):
            return True
        if obj is None:
            return True  # para acceder al listado
        return isinstance(request.user, User) and request.user.has_perm(
            "change_department", obj
        )

    def has_delete_permission(self, request, obj=None):
        if isinstance(request.user, User) and request.user.is_superuser:
            return True
        if obj is None:
            return False
        return isinstance(request.user, User) and request.user.has_perm(
            "delete_department", obj
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # filtra solo los departamentos donde tiene permiso
        return qs.filter(
            pk__in=[
                obj.pk
                for obj in qs
                if isinstance(request.user, User)
                and request.user.has_perm("view_department", obj)
            ]
        )


admin.site.register(Department, DepartmentAdmin)

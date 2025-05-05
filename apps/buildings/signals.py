from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from guardian.shortcuts import assign_perm, remove_perm

from .models import Department

User = get_user_model()

@receiver(post_save, sender=Department)
def assign_department_permissions(sender, instance, created, **kwargs):
    """
    Asigna permisos de objeto al propietario del departamento después de guardar.
    """
    if instance.owner:
        # Eliminar permisos anteriores si el propietario ha cambiado
        if not created and 'owner' in instance._meta.fields:
             try:
                 original_instance = sender.objects.get(pk=instance.pk)
                 if original_instance.owner and original_instance.owner != instance.owner:
                     remove_perm('view_department', original_instance.owner, instance)
                     remove_perm('change_department', original_instance.owner, instance)
                     remove_perm('delete_department', original_instance.owner, instance)
             except sender.DoesNotExist:
                 pass # Objeto recién creado, no hay permisos anteriores que eliminar

        # Asignar nuevos permisos al propietario actual
        assign_perm('view_department', instance.owner, instance)
        assign_perm('change_department', instance.owner, instance)
        # remove_perm('delete_department', instance.owner, instance) # No asignar permiso de eliminar por ahora

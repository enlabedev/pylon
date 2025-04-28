# Estándares de Código

## Principios Generales

- Seguir el principio de "Código Limpio" para todas las implementaciones
- Mantener la simplicidad y legibilidad como prioridades
- Favorecer la composición sobre la herencia
- Utilizar patrones de repositorio para acceso a datos

## Estándares Python

- Utilizar Python 3.12+ y Django 5.2 y aprovechar sus nuevas características
- Seguir PEP 8 para formato y estilo de código
- Limitar longitud de línea a 88 caracteres (compatible con black)
- Usar anotaciones de tipo (type hints) en todas las funciones
- Documentar todas las funciones y clases con docstrings en formato Google

## Estándares Django

- Utilizar modelos abstractos en `core` para comportamientos compartidos
- Implementar mixins para funcionalidades reutilizables
- Mantener vistas delgadas y mover lógica de negocio a servicios
- Usar Django REST Framework para APIs con serializers explícitos
- Gestionar permisos a nivel de vista con decoradores explícitos

## Nomenclatura

- Utilizar nombres descriptivos en español
- Variables y funciones: snake_case
- Clases: PascalCase
- Constantes: UPPER_SNAKE_CASE
- Utilizar prefijos descriptivos para tipos similares

## Ejemplo de estructura de clases

```python
# Modelo base en core
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.BooleanField(default=True)

    class Meta:
        abstract = True

# Servicio en una aplicación específica
class ServiceUser:
    """Servicio para gestionar operaciones de usuario."""
    
    def get_by_id(self, user_id: uuid) -> Optional[User]:
        """Obtiene un usuario por su ID.
        
        Args:
            user_id: ID del usuario a buscar
            
        Returns:
            User encontrado o None si no existe
        """
        try:
            return User.objects.get(id=user_id, deleted_at=False)
        except User.DoesNotExist:
            return None
```

## Patrones a seguir

- Servicios para encapsular lógica de negocio
- Repositorios para operaciones de datos complejas
- Inyección de dependencias para facilitar pruebas
- Uso de dataclasses para transferencia de datos

## Manejo de errores

- Crear excepciones personalizadas y específicas
- Capturar excepciones en nivel apropiado
- Registrar errores con nivel de detalle adecuado
- Devolver mensajes de error descriptivos en respuestas API
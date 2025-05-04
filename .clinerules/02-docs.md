# Requisitos de Documentación para Pylon

## Principios Generales

- La documentación debe mantenerse actualizada con los cambios de código
- Documentar el "por qué" además del "qué" y "cómo"
- Utilizar lenguaje claro y conciso
- Mantener consistencia en el formato y estilo

## Docstrings

Utilizar formato Google para docstrings:

```python
def funcion_ejemplo(param1: str, param2: int = 10) -> bool:
    """Breve descripción de la función en una línea.
    
    Descripción más detallada que explica el propósito,
    comportamiento y contexto de la función.
    
    Args:
        param1: Descripción del primer parámetro
        param2: Descripción del segundo parámetro. Valor predeterminado: 10
        
    Returns:
        Descripción de lo que devuelve la función
        
    Raises:
        ValueError: Condiciones que provocan esta excepción
        
    Examples:
        >>> funcion_ejemplo("test", 5)
        True
    """
```

## Documentación de APIs

- Documentar todos los endpoints con especificaciones OpenAPI
- Incluir ejemplos de solicitud y respuesta
- Documentar posibles códigos de estado y sus significados
- Especificar requisitos de autenticación y permisos

## Documentación de Modelos

Para cada modelo de Django, documentar:

- Propósito y contexto del modelo
- Significado de cada campo
- Relaciones con otros modelos
- Métodos personalizados y su comportamiento
- Considerar usar diagramas para modelos complejos

## Cambios y Decisiones Arquitectónicas

Mantener un archivo ADR (Architecture Decision Records) en `/docs/adr/`:

```
# ADR-001: Uso de Celery para tareas asíncronas

## Estado
Aceptado

## Contexto
Necesitamos procesar tareas largas sin bloquear respuestas HTTP.

## Decisión
Utilizaremos Celery con Redis como broker para gestionar tareas asíncronas.

## Consecuencias
* (+) Mejor experiencia de usuario con respuestas rápidas
* (+) Escalabilidad de procesamiento en worker separados
* (-) Complejidad adicional en la infraestructura
```

## Actualización de README

El README.md debe actualizarse cuando:

- Se añadan nuevas dependencias
- Cambien los procedimientos de instalación o configuración
- Se implementen nuevas características principales
- Se modifiquen los flujos de trabajo de desarrollo

## Mantenimiento de CHANGELOG

Mantener un archivo CHANGELOG.md siguiendo el formato [Keep a Changelog](https://keepachangelog.com/):

```markdown
# Registro de cambios

## [Unreleased]
### Añadido
- Nueva funcionalidad X

### Cambiado
- Comportamiento modificado en Y

### Corregido
- Bug en la función Z

## [1.0.0] - 2025-04-20
### Añadido
- Características iniciales
```

## Comentarios de Código

- Utilizar comentarios para explicar "por qué" no "qué"
- Los nombres autoexplicativos son mejores que los comentarios
- Mantener comentarios TODO con el formato: `# TODO: [TICKET-123] Descripción`
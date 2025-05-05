# Guía del Proyecto PyLon

Este archivo contiene los lineamientos de desarrollo que Cline debe seguir al proporcionar asistencia para este proyecto, todo el trabajo se realizara solo usando django admin.

## Estructura General del Proyecto

El proyecto Pylon es un backend desarrollado con Django que sigue una estructura modular con múltiples aplicaciones especializadas:

pylon/                    # Directorio raíz del proyecto
│
├── config/                           # Configuración del proyecto
│   ├── __init__.py
│   ├── settings/                     # Configuraciones por entorno
│   │   ├── __init__.py
│   │   ├── base.py                   # Configuración base
│   │   ├── development.py            # Configuración de desarrollo
│   │   ├── production.py             # Configuración de producción
│   │   └── test.py                   # Configuración para pruebas
│   ├── urls.py                       # URLs principales
│   ├── wsgi.py                       # Configuración WSGI
│   └── asgi.py                       # Configuración ASGI
│
├── apps/                             # Aplicaciones del proyecto
│   ├── __init__.py
│   │
│   ├── accounts/                     # Gestión de usuarios y autenticación
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py                  # Formularios de autenticación
│   │   ├── managers.py               # Managers personalizados
│   │   ├── migrations/
│   │   ├── models.py                 # Modelo User extendido, Rol, Permiso
│   │   ├── services.py               # Lógica de negocio
│   │   ├── tests/
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── buildings/                    # Gestión de edificios
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations/
│   │   ├── models.py                 # Modelos Edificio, Departamento, Propietario
│   │   ├── services.py
│   │   ├── tests/
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── finances/                     # Gestión financiera
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations/
│   │   ├── models.py                 # Modelos Gasto, Recibo, Pago, MovimientoCaja
│   │   ├── services/                 # Lógica de negocio compleja
│   │   │   ├── __init__.py
│   │   │   ├── caja_service.py
│   │   │   ├── facturacion_service.py
│   │   │   └── gastos_service.py
│   │   ├── tests/
│   │   ├── urls.py
│   │   └── views/                    # Vistas organizadas por funcionalidad
│   │       ├── __init__.py
│   │       ├── caja_views.py
│   │       ├── facturacion_views.py
│   │       └── gastos_views.py
│   │
│   ├── services/                    # Gestión de servicios (agua, etc.)
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations/
│   │   ├── models.py                 # Modelos Medidor, Lectura, Consumo
│   │   ├── services.py
│   │   ├── tests/
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── penalties/                       # Gestión de multas e infracciones
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations/
│   │   ├── models.py                 # Modelos Infraccion, TipoInfraccion, Descargo
│   │   ├── services.py
│   │   ├── tests/
│   │   ├── urls.py
│   │   └── views.py
│   │
│   │
│   ├── tenants/                        # Gestión de junta directiva
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations/
│   │   ├── models.py                 # Modelos JuntaDirectiva, MiembroJunta, Reunion
│   │   ├── services.py
│   │   ├── tests/
│   │   ├── urls.py
│   │   └── views.py
│   │
│   └── reports/                     # Reportes y consultas
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── migrations/
│       ├── services.py               # Lógica de generación de reportes
│       ├── tests/
│       ├── urls.py
│       └── views.py
│
├── core/                             # Funcionalidades compartidas
│   ├── __init__.py
│   ├── constants.py                  # Constantes del sistema
│   ├── middleware.py                 # Middleware personalizado
│   ├── models.py                     # Modelos base abstractos
│   ├── permissions.py                # Permisos personalizados
│   ├── storage.py                    # Storage personalizado para archivos
│   └── utils.py                      # Utilidades generales
│
├── templates/                        # Plantillas HTML
│   ├── base.html                     # Plantilla base
│   ├── accounts/                     # Plantillas de autenticación
│   ├── buildings/                    # Plantillas de edificios
│   ├── finances/                     # Plantillas financieras
│   └── ...                           # Resto de plantillas por app
│
├── static/                           # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
│
├── media/                            # Archivos subidos por usuarios
│   ├── documentos/
│   ├── facturas/
│   └── comprobantes/
│
├── requirements/                     # Dependencias del proyecto
│   ├── base.txt                      # Dependencias base
│   ├── development.txt               # Dependencias de desarrollo
│   └── production.txt                # Dependencias de producción
│
├── manage.py                         # Script de administración de Django
├── .env.example                      # Ejemplo de variables de entorno
├── .gitignore                        # Archivos a ignorar por Git
├── README.md                         # Documentación del proyecto
└── docker-compose.yml                # Configuración Docker (opcional)

## Convenciones de Commit

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Documentación
- `style:` Formato
- `refactor:` Refactorización
- `test:` Tests
- `chore:` Mantenimiento

## Principios de Desarrollo

1. **Modularidad**: Desarrollar funcionalidades en sus módulos correspondientes
2. **Reutilización**: Las funcionalidades comunes deben implementarse en `core`
3. **Consistencia**: Mantener patrones de diseño y nomenclatura coherentes
4. **Calidad**: Todo código debe tener tests unitarios adecuados
5. **Documentación**: Mantener documentación actualizada con el código

## Estándares de Código

- Seguir PEP 8 para estilo de código Python
- Nombres de variables, funciones y clases descriptivos en español
- Usar snake_case para variables y funciones, PascalCase para clases
- Documentar todas las funciones y clases con docstrings
- Aplicar principios SOLID en el diseño de clases

## Modelos y Base de Datos

- Crear modelos abstractos en `core` para comportamientos compartidos
- Implementar validación a nivel de modelo cuando sea posible
- Usar relaciones con `on_delete` adecuados (generalmente PROTECT)
- Definir `related_name` explícito en todas las relaciones
- Considerar el rendimiento en consultas complejas

## Testing

- Tests unitarios obligatorios para toda funcionalidad nueva
- Implementar tests de integración para flujos críticos
- Usar factories para generar datos de prueba
- Mantener cobertura de código superior al 90%
- Seguir metodología Arrange-Act-Assert

## Gestión de Configuración

- Usar variables de entorno para configuraciones sensibles
- Separar configuraciones por entorno (desarrollo, producción)
- No incluir credenciales en el código
- Usar archivos de ejemplo para configuraciones (.env.example)

## Convenciones de Commit

- Seguir formato de Conventional Commits
- Referenciar tickets relacionados en mensajes de commit
- Mantener commits enfocados y descriptivos

## Flujo de Trabajo

- Desarrollar en ramas feature desde develop
- Crear Pull Requests para revisión de código
- Requerir aprobación antes de merge
- Ejecutar tests y validaciones automáticas en CI

Este archivo se actualizará según evolucionen los requisitos y estándares del proyecto.
El desarrollo debe estar escrito en inglés, pero los comentarios y documentación deben estar en español.
Los nombres de las variables y funciones deben ser descriptivos y seguir las convenciones de nomenclatura de Python. Se recomienda el uso de snake_case para variables y funciones, y PascalCase para clases. Además, se debe evitar el uso de abreviaturas innecesarias y mantener la claridad en el código.

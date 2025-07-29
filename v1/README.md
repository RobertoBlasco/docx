# DocX Manipulation Project - Version 1 (Original)

## Descripción
Versión original del proyecto de manipulación de documentos Word (.docx) antes de la refactorización a managers especializados.

## Estructura del Proyecto

```
v1/
├── actions/                          # Acciones específicas
│   ├── action_docx.py               # Acciones principales
│   ├── action_replace_text_with_text.py
│   ├── action_replace_text_with_image.py
│   ├── action_set_form_checkbox.py
│   └── ...
├── data/                            # Archivos de test
│   ├── *.docx                       # Documentos de prueba
│   ├── *.png, *.jpg                 # Imágenes de prueba
│   └── ...
├── main.py                          # Punto de entrada principal
├── main_cmdline.py                  # Versión línea de comandos
├── utils.py                         # Utilidades
├── requirements.txt                 # Dependencias
├── CLAUDE.md                        # Instrucciones originales
├── MIGRATION_SUMMARY.md             # Resumen de migración
└── README.md                        # Este archivo
```

## Características

### Arquitectura Monolítica
- Todo el código en archivos individuales
- Lógica distribuida en actions/
- Dependía originalmente de chilkat2
- **Migrado a python-docx puro**

### Funcionalidades Implementadas
- ✅ Reemplazo de texto por texto
- ✅ Reemplazo de texto por imagen  
- ✅ Gestión de checkboxes de formulario
- ✅ Procesamiento de headers, footers, tablas, textboxes

### Uso
```bash
# Ejecutar con XML de configuración
python main.py ./action.xml

# Versión línea de comandos
python main_cmdline.py [opciones]
```

## Estado
**⚠️ VERSIÓN LEGACY** - Se recomienda usar la versión v2 refactorizada con arquitectura de managers.

## Migración Completada
- ✅ **Eliminadas dependencias** de chilkat2 y lxml
- ✅ **Migrado completamente** a python-docx
- ✅ **Funcionalidad preservada** en version v2

---

**Esta es la versión original antes de la refactorización a managers especializados.**
**Para desarrollo nuevo, usar la versión v2.**
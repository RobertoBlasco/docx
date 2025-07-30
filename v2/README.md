# DocX Manipulation Project - Version 2

## Descripción
Proyecto refactorizado para manipular documentos Word (.docx) usando python-docx con arquitectura basada en managers especializados.

## Estructura del Proyecto

```
v2/
├── managers/                          # Managers especializados
│   ├── __init__.py
│   ├── base_manager.py               # Clase base común
│   ├── checkbox_manager.py           # Gestión de checkboxes
│   ├── text_manager.py               # Gestión de reemplazo de texto
│   └── image_manager.py              # Gestión de reemplazo texto→imagen
├── models/                           # Modelos de datos
│   ├── __init__.py
│   ├── form_checkbox.py              # FormCheckBoxLegacy, FormCheckBoxModern
│   ├── text_replacement.py           # FormTextReplacement
│   └── text_image_replacement.py     # TextImageReplacement
├── objetos/                          # Paquete principal
│   ├── __init__.py
│   ├── docx_document.py              # Coordinador principal (107 líneas)
│   ├── docx_document_old.py          # Backup original
│   └── test_objetos.py               # Script de pruebas
├── requirements.txt                  # Dependencias Python
├── CLAUDE.md                         # Instrucciones del proyecto
└── README.md                         # Este archivo
```

## Funcionalidades Implementadas

### 1. Gestión de Checkboxes
- ✅ Detección de checkboxes legacy y modern
- ✅ XPaths únicos para elementos duplicados
- ✅ Activación/desactivación de checkboxes

### 2. Reemplazo de Texto por Texto
- ✅ Búsqueda en body, headers, footers, tablas y textboxes
- ✅ Preservación de formato original
- ✅ Múltiples ocurrencias

### 3. Reemplazo de Texto por Imagen
- ✅ Búsqueda de texto en párrafos completos
- ✅ Inserción de imágenes con dimensiones personalizables
- ✅ Reconstrucción de párrafos preservando formato

## Uso Básico

### Checkboxes
```python
from objetos import docx_document

# Cargar documento
with open("documento.docx", "rb") as f:
    doc = docx_document.DocxDocument(f.read())

# Obtener checkboxes
checkboxes = doc.get_fields_checkbox()

# Modificar checkbox
for cb in checkboxes:
    if cb.name == "mi_checkbox":
        doc.set_field_checkbox_value(cb, True)

# Guardar
doc.save_to_file("resultado.docx")
```

### Reemplazo de Texto
```python
# Buscar texto
occurrences = doc.get_text_occurrences("{{NOMBRE}}")

# Reemplazar
for occ in occurrences:
    occ.replace_text = "Juan Pérez"
    doc.replace_text_occurrence(occ)

doc.save_to_file("resultado.docx")
```

### Reemplazo de Texto por Imagen
```python
# Cargar imagen
with open("logo.png", "rb") as f:
    image_data = f.read()

# Buscar texto para reemplazar
replacements = doc.get_text_for_image_replacement("{{LOGO}}")

# Configurar y reemplazar
for repl in replacements:
    repl.image_data = image_data
    repl.width = 100
    repl.height = 50
    doc.replace_text_with_image(repl)

doc.save_to_file("resultado.docx")
```

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar tests:
```bash
cd objetos
python test_objetos.py
```

## Arquitectura

### Patrón de Diseño
- **DocxDocument**: Coordinador principal que delega a managers
- **Managers**: Especializados por funcionalidad (checkbox, text, image)
- **Models**: Objetos de datos tipados para cada operación
- **BaseManager**: Clase base con funcionalidad común

### Beneficios
- ✅ **Responsabilidad única** por manager
- ✅ **Código mantenible** y escalable
- ✅ **Fácil testing** de componentes individuales
- ✅ **Consistencia** en APIs públicas

## Historial de Versiones

### v2 (Actual)
- Arquitectura refactorizada con managers
- Funcionalidad de reemplazo texto→imagen
- XPaths únicos para elementos duplicados
- Estructura modular y escalable

### v1 (Original)
- Código monolítico en un solo archivo
- Funcionalidades básicas de checkbox y texto
- Migración de chilkat2 a python-docx

---

**Desarrollado con Claude AI - 2025**
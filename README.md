# DocX Manipulation Project

Proyecto para manipular documentos Microsoft Word (.docx) usando Python y python-docx.

## Organización de Versiones

Este proyecto está organizado en dos versiones principales:

### 📁 **v1/** - Versión Original (Legacy)
- **Arquitectura**: Monolítica
- **Código**: Distribuido en archivos individuales
- **Estado**: ✅ Funcional pero legacy
- **Uso**: Desarrollo histórico y referencia

**Características:**
- Código original con migración de chilkat2 a python-docx
- Estructura basada en actions/
- Funcionalidades completas pero no organizadas

### 📁 **v2/** - Versión Refactorizada (Recomendada)
- **Arquitectura**: Managers especializados
- **Código**: Modular y escalable
- **Estado**: ✅ Activa para desarrollo
- **Uso**: **Versión recomendada para nuevo desarrollo**

**Características:**
- Arquitectura limpia con separación de responsabilidades
- Managers especializados (CheckboxManager, TextManager, ImageManager)
- Modelos tipados para cada operación
- Fácil extensibilidad y mantenimiento

## Funcionalidades Implementadas

### ✅ Gestión de Checkboxes
- Checkboxes legacy (Form Fields)
- Checkboxes modern (Content Controls)
- XPaths únicos para elementos duplicados
- Activación/desactivación programática

### ✅ Reemplazo de Texto
- Texto por texto (preservando formato)
- Texto por imagen (con dimensiones personalizables)
- Búsqueda en body, headers, footers, tablas, textboxes

### ✅ Procesamiento Avanzado
- Reconstrucción de párrafos
- Preservación de formato
- Manejo de múltiples ocurrencias

## Inicio Rápido

### Para usuarios nuevos (Recomendado: v2)
```bash
cd v2/objetos
python test_objetos.py
```

### Para usuarios existentes (v1)
```bash
cd v1
python main.py ./action.xml
```

## Estructura Completa

```
python/
├── v1/                    # 📦 Versión original
│   ├── actions/           # Acciones específicas
│   ├── data/              # Archivos de test
│   ├── main.py            # Punto de entrada
│   └── ...
├── v2/                    # 🚀 Versión refactorizada
│   ├── managers/          # Managers especializados
│   ├── models/            # Modelos de datos
│   ├── objetos/           # Coordinador principal
│   └── ...
└── README.md              # Este archivo
```

## Migración Completada

✅ **De chilkat2 → python-docx**: Eliminadas dependencias externas  
✅ **De monolítico → modular**: Arquitectura limpia y escalable  
✅ **Funcionalidad preservada**: Todas las características originales  
✅ **Nuevas funcionalidades**: Reemplazo texto→imagen agregado  

## Recomendaciones

- **🎯 Para desarrollo nuevo**: Usar **v2/**
- **📚 Para referencia histórica**: Consultar **v1/**
- **🔧 Para mantenimiento**: Migrar gradualmente a **v2/**

---

**Desarrollado con Claude AI - 2025**  
**Migración completada: v1 → v2**
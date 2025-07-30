# TextFieldManager - Guía de Campos de Texto en Word

## Introducción

El `TextFieldManager` es responsable de detectar y manipular campos de texto en documentos Microsoft Word (.docx). Word ofrece varios tipos de campos de texto con diferentes características y capacidades.

## Tipos de Campos de Texto Soportados

### 1. LEGACY - Campos de Formulario Antiguos

**Origen**: Word 97-2003 y compatibilidad hacia atrás  
**Estructura XML**: `w:fldChar/w:ffData/w:textInput`

#### Características:
- Campos de formulario básicos heredados
- Solo admiten texto plano sin formato
- Identificados por atributo `name`
- Limitaciones de presentación y formato
- Aún ampliamente utilizados por compatibilidad

#### Estructura XML:
```xml
<w:fldChar w:fldCharType="begin">
  <w:ffData>
    <w:name w:val="apellido_usuario"/>
    <w:textInput>
      <w:default w:val="Escriba su apellido aquí"/>
      <w:maxLength w:val="50"/>
    </w:textInput>
  </w:ffData>
</w:fldChar>
<w:instrText>FORMTEXT</w:instrText>
<w:fldChar w:fldCharType="end"/>
```

#### Propiedades del Manager:
- **Identificación**: `text_field_obj.name`
- **Valor**: `text_field_obj.default`
- **XPath**: Basado en `name` y posición

---

### 2. MODERN - Structured Document Tags (SDT)

Los campos modernos utilizan la estructura `w:sdt` (Structured Document Tag) introducida en Word 2007.

#### 2A. Campo de Texto Plano (`w:text`)

**Estructura XML**: `w:sdt/w:sdtPr/w:text`

##### Características:
- **RESTRINGIDO** a texto plano únicamente
- Típicamente una sola línea
- No permite formato rich text (negrita, cursiva, etc.)
- Control específico para entrada de texto simple
- Ideal para campos como números de teléfono, códigos, etc.

##### Estructura XML:
```xml
<w:sdt>
  <w:sdtPr>
    <w:tag w:val="numero_telefono"/>
    <w:alias w:val="Número de teléfono"/>
    <w:text/>  <!-- RESTRICCIÓN: solo texto plano -->
    <w:placeholder>
      <w:docPart w:val="DefaultPlaceholder_12345"/>
    </w:placeholder>
  </w:sdtPr>
  <w:sdtContent>
    <w:r>
      <w:t>555-1234</w:t>
    </w:r>
  </w:sdtContent>
</w:sdt>
```

---

#### 2B. Campo de Contenido Libre (Sin Restricciones)

**Estructura XML**: `w:sdt` sin elementos restrictivos

##### Características:
- **SIN RESTRICCIONES** de tipo de contenido
- Permite múltiples párrafos
- Admite formato básico de texto
- Más flexible que campos `w:text`
- Comportamiento similar a un área de texto libre

##### Estructura XML:
```xml
<w:sdt>
  <w:sdtPr>
    <w:tag w:val="first_name"/>
    <w:alias w:val="El nombre de la persona"/>
    <w:placeholder>
      <w:docPart w:val="DefaultPlaceholder_-1854013440"/>
    </w:placeholder>
    <!-- NO hay elementos restrictivos como <w:text> -->
  </w:sdtPr>
  <w:sdtContent>
    <w:p>
      <w:r>
        <w:t>Juan Carlos</w:t>
      </w:r>
    </w:p>
  </w:sdtContent>
</w:sdt>
```

---

#### 2C. Campo de Texto Enriquecido (`w:richText`)

**Estructura XML**: `w:sdt/w:sdtPr/w:richText`

##### Características:
- **PERMITE** formato completo (negrita, cursiva, colores, estilos)
- Múltiples párrafos con diferentes estilos
- Capacidades completas de edición rich text
- Más potente que el contenido libre básico

##### Estructura XML:
```xml
<w:sdt>
  <w:sdtPr>
    <w:tag w:val="descripcion_detallada"/>
    <w:alias w:val="Descripción con formato"/>
    <w:richText/>  <!-- PERMITE: formato completo -->
  </w:sdtPr>
  <w:sdtContent>
    <w:p>
      <w:r>
        <w:rPr>
          <w:b/>  <!-- Negrita -->
        </w:rPr>
        <w:t>Texto en negrita</w:t>
      </w:r>
      <w:r>
        <w:t> y texto normal</w:t>
      </w:r>
    </w:p>
  </w:sdtContent>
</w:sdt>
```

---

## Comparación de Tipos

| Tipo | Flexibilidad | Formato | Párrafos | Identificación | Uso Recomendado |
|------|-------------|---------|----------|----------------|------------------|
| **Legacy** | Baja | Solo texto plano | No | `name` | Compatibilidad |
| **Text** | Baja | Solo texto plano | No | `tag`/`alias` | Campos simples |
| **Contenido Libre** | Media | Básico | Sí | `tag`/`alias` | Campos generales |
| **Rich Text** | Alta | Completo | Sí | `tag`/`alias` | Contenido rico |

---

## Estado Actual del TextFieldManager

### ✅ Tipos Actualmente Soportados:

1. **LEGACY** - `w:fldChar/w:ffData/w:textInput`
2. **MODERN Text** - `w:sdt/w:sdtPr/w:text`

### ❌ Tipos Pendientes de Implementar:

3. **MODERN Contenido Libre** - `w:sdt` sin elementos restrictivos
4. **MODERN Rich Text** - `w:sdt/w:sdtPr/w:richText`

---

## Funcionalidades del Manager

### `get_text_fields(includeBody=True, includeHeaders=True, includeFooters=True)`

Busca y retorna todos los campos de texto en el documento.

**Retorna**: Lista de objetos `FormTextField` (Legacy o Modern)

**Propiedades de los objetos retornados**:
- **Legacy**: `name`, `default`, `xpath`
- **Modern**: `tag`, `alias`, `text`, `placeholder`, `xpath`

### `set_text_field_value(text_field_obj, value: str)`

Modifica el valor de un campo de texto específico.

**Parámetros**:
- `text_field_obj`: Objeto FormTextField obtenido de `get_text_fields()`
- `value`: Nuevo valor de texto a asignar

**Retorna**: `bool` - True si la modificación fue exitosa

---

## Identificación de Campos

### Campos Legacy
- **Identificador**: Atributo `name` en `w:ffData/w:name/@w:val`
- **Ejemplo**: `name="apellido_usuario"`

### Campos Modern
- **Identificador primario**: Atributo `tag` en `w:sdtPr/w:tag/@w:val`
- **Identificador secundario**: Atributo `alias` en `w:sdtPr/w:alias/@w:val`
- **Prioridad**: Se usa `tag` si existe, sino `alias`
- **Ejemplo**: `tag="first_name"` o `alias="El nombre de la persona"`

---

## Lógica de Detección Actual

### Para Campos Legacy:
```python
# Buscar w:fldChar con w:ffData/w:textInput
fld_chars = element.findall('.//w:fldChar', namespaces)
for fld_char in fld_chars:
    ff_data = fld_char.find('w:ffData', namespaces)
    if ff_data is not None and ff_data.find('w:textInput', namespaces) is not None:
        # Es un campo de texto legacy
```

### Para Campos Modern:
```python
# Buscar w:sdt con w:sdtPr/w:text
sdts = element.findall('.//w:sdt', namespaces)
for sdt in sdts:
    sdt_pr = sdt.find('w:sdtPr', namespaces)
    if sdt_pr is not None and sdt_pr.find('w:text', namespaces) is not None:
        # Es un campo de texto modern con restricción w:text
```

---

## Modificación de Valores

### Campos Legacy:
- **Elemento a modificar**: `w:textInput/w:default/@w:val`
- **Comportamiento**: Establece el valor por defecto del campo

### Campos Modern:
- **Elemento a modificar**: Contenido dentro de `w:sdtContent`
- **Comportamiento**: 
  - Limpia todos los `w:r` (runs) existentes
  - Crea nuevos `w:r` con el texto especificado
  - Mantiene la estructura de párrafos

---

## Limitación Actual Identificada

**Problema**: El manager actual solo detecta campos modern que tienen explícitamente `<w:text/>` en su estructura, pero muchos campos de texto modernos (como "first_name") son de **contenido libre** y no tienen este elemento.

**Solución Propuesta**: Modificar la lógica de detección para incluir `w:sdt` que:
- Tengan `w:tag` o `w:alias`
- NO sean checkboxes (`w14:checkbox`)
- NO sean otros controles específicos (listas, fechas, etc.)

---

## Casos de Uso

### XML de Configuración
```xml
<action name="setFormText" id="5">
    <form tag="first_name">Juan Carlos</form>
    <form tag="apellido_usuario">González</form>
    <form tag="numero_telefono">555-1234</form>
</action>
```

### Procesamiento
1. El sistema busca campos con `tag="first_name"`, `tag="apellido_usuario"`, etc.
2. Asigna los valores especificados usando `set_text_field_value()`
3. Los campos se actualizan en el documento Word

---

## Archivos Relacionados

- **Manager**: `managers/text_field_manager.py`
- **Modelos**: `models/form_text_field.py`
- **Integración**: `core/docx_document.py`
- **Tests**: `tests/test_text_field_manager.py`

---

*Documentación generada para el proyecto DocX Manipulation - Python v2*
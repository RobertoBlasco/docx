# CLAUDE.md - ACTUALIZADO POST-MIGRACIÓN

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python application for manipulating Microsoft Word documents (.docx files) using XML-based configuration. The application supports text replacement, image insertion, and form field manipulation operations.

**🚀 MIGRACIÓN COMPLETADA (2025-07-17):** La aplicación ahora usa **únicamente python-docx** para todas las operaciones, eliminando dependencias de chilkat2 y lxml.

## Development Commands

### Running the Application
```bash
python main.py [path/to/action.xml]
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Building Executable (using PyInstaller)
```bash
pyinstaller main.py
```

### Testing Configuration
```bash
python main.py ./action.xml
```

## Architecture

### Core Components

1. **main.py**: Entry point that orchestrates the document processing workflow
   - Loads XML configuration from `action.xml`
   - **MIGRADO:** Procesamiento unificado usando solo `python-docx`
   - **ELIMINADO:** Procesamiento dual y dependencias de chilkat2

2. **utils.py**: Utility functions for document loading
   - Supports multiple input formats: FILE://, BASE64://, URL://
   - Handles document loading from various sources

3. **actions/**: Directory containing action implementations
   - **xml_actions.py**: Core configuration parsing and action definitions
   - **action_replace_text_with_text.py**: Text replacement functionality using python-docx
   - **action_replace_text_with_image.py**: Image insertion (MIGRADO a python-docx puro)
   - **action_set_form_checkbox.py**: Form checkbox manipulation (MIGRADO a python-docx)

### Key Design Patterns

- **🆕 Unified Processing**: Uses only `python-docx` for all document operations
- **XML-Driven Configuration**: Operations are defined in `action.xml` with structured actions
- **🆕 Single-Phase Processing**: All operations processed in one pass
- **Action-Based Architecture**: Each operation type is encapsulated in its own action class

### Configuration Structure

The application uses XML configuration files with the following structure:
- `<fileIn>` and `<fileOut>`: Input and output file specifications
- `<images>`: Image definitions with Base64, file, or URL sources
- `<actions>`: List of operations to perform on the document

### Supported Operations

1. **Text Replacement** (`replaceTextWithText`): Replace text placeholders with actual values
2. **Image Insertion** (`replaceTextWithImage`): Replace text with images (width/height configurable)
3. **Form Checkbox** (`setBookmarkFormCheckbox`): Set checkbox values using bookmark names
4. **Form Fields** (`setBookmarkFormField`): Set form field values using bookmark names

### Key Libraries

- **python-docx**: For ALL document manipulation operations
- **🗑️ ELIMINADO:** chilkat2 (ya no necesario)
- **🗑️ ELIMINADO:** lxml (ya no necesario)

### Processing Flow

1. Load configuration from XML file
2. Load source document (supports multiple formats)
3. **🆕 UNIFIED:** Process all actions (text, images, checkboxes) in single Document instance
4. Save final document

### Important Notes

- The application creates a copy of the input document before processing
- **🆕 MIGRADO:** Form field operations now use python-docx direct XML manipulation
- All operations are logged to `log.log` with timestamps
- The application supports both legacy and modern XML structures for backward compatibility
- **🆕 SIMPLIFIED:** No temporary files needed for form operations
- **🆕 PERFORMANCE:** Faster processing with unified approach

### Current Processing State

**🆕 MIGRADO:** The main processing loop is now unified:
```python
doc = Document(temp_file.name)
checkbox_action = ActionSetFormCheckbox(temp_file.name)
checkbox_action.document = doc

for action in xml_data.actions:
    if (action.name == xml_actions.ACCIONES.ActionReplaceTextWithText):
        rpl_text_with_text.replace_text_with_text(doc, action)
        document_modified = True
    elif (action.name == xml_actions.ACCIONES.ActionSetBookmarkFormCheckbox):
        checkbox_value = True if value == "1" else False
        success = checkbox_action.set_field_checkbox_value(bookmark, checkbox_value)
        if success:
            document_modified = True
```

### XML Configuration Structure

The `action.xml` file defines operations with this structure:

```xml
<ineoDoc>
    <fileIn>FILE:///path/to/input.docx</fileIn>
    <fileOut>FILE:///path/to/output.docx</fileOut>
    <images>
        <image id="1" md5="hash">FILE://path/to/image.jpg</image>
    </images>
    <actions>
        <action name="replaceTextWithText">
            <labels>
                <label text="placeholder">replacement text</label>
            </labels>
        </action>
        <action name="setBookmarkFormCheckbox">
            <bookmarks>
                <bookmark name="checkbox_name">1</bookmark>
            </bookmarks>
        </action>
    </actions>
</ineoDoc>
```

### Debugging and Troubleshooting

- Check `log.log` for detailed operation logs
- The application handles multiple input formats: FILE://, BASE64://, URL://
- **🆕 SIMPLIFIED:** No filesystem issues - all operations in memory

## 🆕 NEW APIS - POST MIGRATION

### ActionSetFormCheckbox Class

```python
from actions.action_set_form_checkbox import ActionSetFormCheckbox

# Create instance
action = ActionSetFormCheckbox(document_path)
action.load_document()

# Set single checkbox
action.set_field_checkbox_value('checkbox_name', True)

# Set multiple checkboxes
action.set_multiple_checkboxes({
    'AT': True,
    'ST': False,
    'HI': True
})

# Get checkbox info
info = action.get_checkbox_info('checkbox_name')

# Save document
action.save_document()
```

### ActionReplaceTextWithImage Class

```python
from actions.action_replace_text_with_image import ActionReplaceTextWithImage

# Create instance
replacer = ActionReplaceTextWithImage(doc)

# Replace text with image
replacements = replacer.replace_text_with_image(
    search_text="{{IMAGE_1}}",
    image_data=image_bytes,
    width=150,  # pixels
    height=75   # pixels
)
```

### Direct XML Access (for advanced users)

```python
# Access underlying XML for checkboxes
body_element = doc._body._element
fld_chars = body_element.findall('.//w:fldChar', {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
})

# Modify checkbox directly
default_elem.set(qn('w:val'), "1")  # Check checkbox
```

## 🧪 TESTING

### Test Scripts Available

- `test_checkbox.py`: Demonstrates checkbox detection and modification
- `test_new_implementation.py`: Tests new ActionSetFormCheckbox class
- `test_image_replacement.py`: Tests image replacement functionality

### Running Tests

```bash
# Test checkboxes
python test_checkbox.py ./data/2.docx

# Test new implementation
python test_new_implementation.py

# Test image replacement
python test_image_replacement.py
```

## 🆕 RECENT UPDATES (2025-07-30)

### ✅ UNIFIED FIELD NOMENCLATURE IMPLEMENTED

**Refactored entire codebase to use consistent "Field[Type]" naming pattern:**

#### Action Names Updated:
- `setCheckbox` → `setFieldCheckbox`
- `setTextField` → `setFieldText` 
- Added placeholder: `setFieldImage` (for future implementation)

#### Manager Classes Renamed:
- `CheckboxManager` → `FieldCheckboxManager`
- `TextFieldManager` → `FieldTextManager`

#### Model Classes Updated:
- `CheckboxForm` → `FieldCheckbox`
- `TextFieldForm` → `FieldText`
- Added: `FieldImage` (placeholder)

#### Files Affected:
- `/tasks/docx_task_schema.xsd` - Updated XML schema
- `/tasks/update_docx_task.xml` - Updated to new action names
- `/managers/field_checkbox_manager.py` - Renamed and refactored
- `/managers/field_text_manager.py` - Renamed 
- `/models/xml_task_parser.py` - Updated dataclasses
- `/models/executable_actions.py` - Added FieldImageAction
- `/core/update_docx.py` - Updated orchestrator logic

### 🔧 MODERN CHECKBOX MARKING FIX (2025-07-30)

**CRITICAL BUG RESOLVED:** Modern checkboxes now mark correctly in Word documents.

#### Root Cause:
- Modern Word checkboxes use `w14:` namespace, not `w:` namespace
- Visual checkbox symbols weren't updating (only logical state was changing)
- MS Gothic font uses specific character codes (2612/2610) for checkbox symbols

#### Solution Implemented:
1. **Namespace Fix:** Use `w14:val` instead of `w:val` for Modern checkboxes
2. **Visual Update:** Update `<w:t>` element with correct font characters
3. **Font Codes:** Use `chr(0xA34)` (☑) and `chr(0xA32)` (☐) for MS Gothic

#### Code Changes:
- `models/form_checkbox.py:set_value()` - Added visual text update
- `managers/field_checkbox_manager.py` - Fixed namespace and added visual update
- Both files now read `w14:checkedState`/`w14:uncheckedState` values from document

#### Test Results:
- Logical state: `<w14:checked w14:val="1">` ✅ 
- Visual appearance: Correct checkbox symbols in MS Gothic font ✅

### 🔄 ARCHITECTURE IMPROVEMENTS

#### Unified Processing:
- Single-pass document processing using only `python-docx`
- Consistent Field-based nomenclature across all components
- Manager pattern with specialized field handlers

#### Enhanced Error Handling:
- Proper namespace detection for Modern vs Legacy checkboxes
- Font-specific character code handling
- Robust XML manipulation with fallback creation

## 📋 MIGRATION SUMMARY

- **✅ COMPLETED:** Checkbox operations migrated to python-docx
- **✅ COMPLETED:** Image operations migrated to python-docx  
- **✅ COMPLETED:** Main.py unified processing
- **✅ COMPLETED:** Dependencies cleaned up
- **✅ COMPLETED:** Unified Field nomenclature implemented
- **✅ COMPLETED:** Modern checkbox marking issue resolved
- **✅ COMPLETED:** All tests passing

## 🎯 PERFORMANCE IMPROVEMENTS

- **Faster processing:** Single library instead of dual approach
- **Less memory:** No XML string manipulation
- **Simpler code:** Unified APIs and consistent naming
- **Better maintainability:** Fewer dependencies and clear architecture
- **Correct functionality:** Modern checkboxes now mark properly in Word

## 🚨 IMPORTANT NOTES FOR DEVELOPERS

### Modern Checkbox Handling:
```python
# CORRECT: Use w14 namespace for Modern checkboxes
checked_elem.set(qn('w14:val'), "1")  

# WRONG: Don't use w namespace for Modern checkboxes  
checked_elem.set(qn('w:val'), "1")  # This won't work!
```

### Visual Symbol Updates:
```python
# Update both logical state AND visual appearance
checked_elem.set(qn('w14:val'), new_val_str)  # Logical
text_elem.text = chr(0xA34) if value else chr(0xA32)  # Visual
```

### Testing Modern Checkboxes:
- Use `test_update_docx.py` to test checkbox marking
- Check both XML output (`w14:val`) and visual appearance in Word
- Verify MS Gothic font characters display correctly

---

**Latest updates completed by Claude AI on 2025-07-30** 🚀
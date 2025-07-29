import os
import time

from docx import Document
from docx.shared import Inches
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


"""
 <w:fldChar w:fldCharType="begin">
    <w:ffData>
      <w:name w:val="checkbox_name"/>
      <w:checkBox>                    <!-- ← Elemento específico para checkbox -->
        <w:default w:val="0"/>        <!-- 0=unchecked, 1=checked -->
        <w:size w:val="10"/>          <!-- Tamaño opcional -->
      </w:checkBox>
    </w:ffData>
  </w:fldChar>
"""

def set_form_checkbox(doc: Document, action) :

    start_time = time.time()
    for section in doc.sections:
         process_part(doc, action)               # Body del documento
         process_part(section.header, action)    # Headers
         process_part(section.footer, action)    # Footers
    end_time = time.time()
    elapsed = end_time - start_time
    num_seconds = float(f"{elapsed:.4f}")
    return num_seconds


def set_form_checkbox2(doc: Document, action) -> float:
    
    found_checkboxes = []


    start_time = time.time()
    checkboxes = find_form_by_name(doc, action.form_name)
    for checkbox_data in checkboxes :
        set_checkbox_value(checkbox_data, action.form_name, action.checkbox_value)
    end_time = time.time()
    elapsed = end_time - start_time
    num_seconds = float(f"{elapsed:.4f}")
    return num_seconds
    
    # start_time = time.time()
    # for section in doc.sections:
    #      process_part(doc, action)               # Body del documento
    #      process_part(section.header, action)    # Headers
    #      process_part(section.footer, action)    # Footers
    # end_time = time.time()
    # elapsed = end_time - start_time
    # num_seconds = float(f"{elapsed:.2f}")
    # return num_seconds

"""
    Procesamos Headers, Footers y Body
"""
def process_part(part, action):
    process_paragraphs(part.paragraphs, action) # Párrafos
    process_tables(part.tables, action)         # Tablas
    process_textboxes(part, action)             # TextBoxes
    
def process_paragraphs(paragraphs, action) :
    for paragraph in paragraphs :
        pass

def process_tables(tables, action) :
    for table in tables :
        pass

def process_textboxes(textboxes, action) :
    for textbox in textboxes :
        pass


def find_form_checkboxes_by_name(doc: Document, checkbox_name: str) :

    found_checkboxes_legacy = []
    found_checkboxes_modern = []
    found_checkboxes_legacy = find_form_checkboxes_by_name_legacy(doc, checkbox_name)
    found_checkboxes_modern = find_form_checkboxes_by_name_modern(doc, checkbox_name)

def find_form_checkboxes_by_name_legacy(doc: Document, checkbox_name) :
    pass

def find_form_checkboxes_by_name_modern(doc: Document, checkbox_name) :
    pass

def find_form_by_name(doc: Document, checkbox_name: str):
    found_checkboxes = []


    
    # Buscar en todo el documento
    body_element = doc._body._element
    
    
    # Encontrar todos los elementos fldChar
    fld_chars = body_element.findall('.//w:fldChar', {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    })
    
    for fld_char in fld_chars:
        # Verificar que sea un campo de inicio
        fld_char_type = fld_char.get(qn('w:fldCharType'))
        
        if fld_char_type == 'begin':
            # Buscar datos del campo de formulario
            ff_data = fld_char.find(qn('w:ffData'))
            
            if ff_data is not None:
                # Verificar que sea un checkbox
                checkbox = ff_data.find(qn('w:checkBox'))
                
                if checkbox is not None:
                    # Obtener el nombre del checkbox
                    name_elem = ff_data.find(qn('w:name'))
                    current_name = name_elem.get(qn('w:val')) if name_elem is not None else ""
                    
                    if current_name == checkbox_name:
                        found_checkboxes.append({
                            'fld_char': fld_char,
                            'ff_data': ff_data,
                            'checkbox': checkbox,
                            'name': current_name
                        })
    return found_checkboxes
    
def set_checkbox_value(checkbox_data, checkbox_name: str, value: bool) -> float :
    
    modifications_made = 0
    new_val_str = "1" if value else "0"
    
    checkbox = checkbox_data['checkbox']
        
    # Obtener el elemento default actual
    default_elem = checkbox.find(qn('w:default'))
    current_val = default_elem.get(qn('w:val')) if default_elem is not None else "0"
    
    if current_val != new_val_str:
        # Modificar el valor
        if default_elem is not None:
            default_elem.set(qn('w:val'), new_val_str)
        else:
            # Crear nuevo elemento default si no existe
            default_elem = OxmlElement('w:default')
            default_elem.set(qn('w:val'), new_val_str)
            checkbox.append(default_elem)
        
        # logger.info(f"Checkbox '{checkbox_name}' modificado: {current_val} -> {new_val_str}")
        modifications_made += 1
    else:
        pass
        # logger.info(f"Checkbox '{checkbox_name}' ya tiene el valor {new_val_str}")
    
    #return modifications_made > 0
    return 0.0
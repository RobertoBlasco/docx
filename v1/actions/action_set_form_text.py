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
      <w:name w:val="text_field_name"/>
      <w:textInput>                   <!-- ← Elemento específico para texto -->
        <w:default w:val="texto por defecto"/>
        <w:maxLength w:val="50"/>     <!-- Longitud máxima opcional -->
        <w:type w:val="regular"/>     <!-- Tipo: regular, number, date, etc. -->
      </w:textInput>
    </w:ffData>
  </w:fldChar>
"""

def set_form_text(doc: Document, action) -> float:
    
    start_time = time.time()
    checkboxes = find_form_by_name(doc, action.form_name)
    for checkbox_data in checkboxes :
        pass
        #set_checkbox_value(checkbox_data, action.form_name, action.checkbox_value)
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

def find_form_by_name(doc: Document, textinput_name: str):

    found_textinputs = []

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
                # Verificar que sea un form textInput
                text_input = ff_data.find(qn('w:textInput'))
                
                if text_input is not None:
                    # Obtener el nombre del checkbox
                    name_elem = ff_data.find(qn('w:name'))
                    current_name = name_elem.get(qn('w:val')) if name_elem is not None else ""
                    if current_name == textinput_name:
                        found_textinputs.append({
                            'fld_char': fld_char,
                            'ff_data': ff_data,
                            'text_input': text_input,
                            'name': current_name
                        })

    return found_textinputs
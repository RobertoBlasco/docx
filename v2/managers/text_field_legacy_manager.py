"""
Manager especializado para campos de texto Legacy (w:fldChar/w:textInput)
"""

from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from .base_manager import BaseManager
from models import form_text_field


class TextFieldLegacyManager(BaseManager):
    def __init__(self, docx_document):
        super().__init__(docx_document)
    
    def get_fields(self, includeBody=True, includeHeaders=True, includeFooters=True):
        """
        Encuentra todos los campos de texto Legacy en el documento
        
        Args:
            includeBody: Buscar en el cuerpo del documento
            includeHeaders: Buscar en headers
            includeFooters: Buscar en footers
        
        Returns:
            List[FormTextFieldLegacy]: Lista de campos legacy encontrados
        """
        text_fields_found = []
        
        # Obtener elementos donde buscar
        elements_to_search = self._get_elements_to_search(includeBody, includeHeaders, includeFooters)
        
        # Contador para posiciones únicas por nombre
        name_counters = {}
        
        for element in elements_to_search:
            # Buscar LEGACY text fields: w:fldChar/w:ffData/w:textInput
            fld_chars = element.findall('.//w:fldChar', self.namespaces)
            
            for fld_char in fld_chars:
                ff_data = fld_char.find('w:ffData', self.namespaces)
                if ff_data is not None and ff_data.find('w:textInput', self.namespaces) is not None:
                    # Es un text field legacy
                    text_field_obj = form_text_field.FormTextFieldLegacy()
                    
                    # xml_node = todo el contenido de w:fldChar
                    text_field_obj.xml_node = fld_char
                    
                    # name = valor de w:name/@w:val
                    name_elem = ff_data.find('w:name', self.namespaces)
                    text_field_obj.name = name_elem.get(qn('w:val')) if name_elem is not None else ""
                    
                    if text_field_obj.name and text_field_obj.name.strip():
                        # Incrementar contador para este nombre
                        if text_field_obj.name not in name_counters:
                            name_counters[text_field_obj.name] = 0
                        name_counters[text_field_obj.name] += 1
                        
                        # xpath = ruta ÚNICA al w:fldChar por nombre y posición
                        position = name_counters[text_field_obj.name]
                        text_field_obj.xpath = f"(//w:fldChar[w:ffData/w:name/@w:val='{text_field_obj.name}' and w:ffData/w:textInput])[{position}]"
                        
                        # default = valor actual del campo de texto
                        text_input = ff_data.find('w:textInput', self.namespaces)
                        default_elem = text_input.find('w:default', self.namespaces) if text_input is not None else None
                        text_field_obj.default = default_elem.get(qn('w:val')) if default_elem is not None else ""
                        
                        text_fields_found.append(text_field_obj)
        
        return text_fields_found
    
    def set_field_value(self, text_field_obj, value: str):
        """
        Establece el valor de un campo de texto legacy
        
        Args:
            text_field_obj: Objeto FormTextFieldLegacy
            value: Nuevo valor para el campo de texto
        
        Returns:
            bool: True si se modificó correctamente, False si hubo error
        """
        try:
            # Localizar el elemento usando xpath (simulado con find)
            # Buscar por nombre en todo el documento
            body_element = self.docx._body._element
            fld_chars = body_element.findall('.//w:fldChar', self.namespaces)
            
            found_count = 0
            target_position = int(text_field_obj.xpath.split('[')[-1].split(']')[0])  # Extraer posición del xpath
            
            for fld_char in fld_chars:
                ff_data = fld_char.find('w:ffData', self.namespaces)
                if ff_data is not None:
                    text_input = ff_data.find('w:textInput', self.namespaces)
                    if text_input is not None:
                        name_elem = ff_data.find('w:name', self.namespaces)
                        if name_elem is not None and name_elem.get(qn('w:val')) == text_field_obj.name:
                            found_count += 1
                            
                            if found_count == target_position:
                                # Este es el text field correcto
                                default_elem = text_input.find('w:default', self.namespaces)
                                
                                if default_elem is not None:
                                    default_elem.set(qn('w:val'), value)
                                else:
                                    # Crear elemento default si no existe
                                    default_elem = OxmlElement('w:default')
                                    default_elem.set(qn('w:val'), value)
                                    text_input.append(default_elem)
                                
                                return True
            
            return False  # No se encontró el text field
            
        except Exception as e:
            print(f"Error al modificar text field legacy: {e}")
            return False
"""
Manager especializado para campos de texto Free/Libre (w:sdt sin restricciones)
Este manager detecta campos como "first_name" que no tienen elementos restrictivos
"""

from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from .base_manager import BaseManager
from models import field_text_model as form_text_field


class FieldTextFreeManager(BaseManager):
    def __init__(self, docx_document):
        super().__init__(docx_document)
    
    def get_fields_text(self, includeBody=True, includeHeaders=True, includeFooters=True):
        """
        Encuentra todos los campos de texto Free (contenido libre) en el documento
        
        Args:
            includeBody: Buscar en el cuerpo del documento
            includeHeaders: Buscar en headers
            includeFooters: Buscar en footers
        
        Returns:
            List[FormTextFieldModern]: Lista de campos free text encontrados
        """
        text_fields_found = []
        
        # Obtener elementos donde buscar
        elements_to_search = self._get_elements_to_search(includeBody, includeHeaders, includeFooters)
        
        # Contador para posiciones únicas por identificador
        name_counters = {}
        
        for element in elements_to_search:
            # Buscar MODERN SDT que NO sean de tipos específicos
            sdts = element.findall('.//w:sdt', self.namespaces)
            
            for sdt in sdts:
                sdt_pr = sdt.find('w:sdtPr', self.namespaces)
                if sdt_pr is not None:
                    # Verificar que NO tenga elementos restrictivos
                    has_text = sdt_pr.find('w:text', self.namespaces) is not None
                    has_richText = sdt_pr.find('w:richText', self.namespaces) is not None
                    has_checkbox = sdt_pr.find('w14:checkbox', self.namespaces) is not None
                    has_dropDownList = sdt_pr.find('w:dropDownList', self.namespaces) is not None
                    has_comboBox = sdt_pr.find('w:comboBox', self.namespaces) is not None
                    has_date = sdt_pr.find('w:date', self.namespaces) is not None
                    has_picture = sdt_pr.find('w:picture', self.namespaces) is not None
                    
                    # Es campo libre si NO tiene elementos restrictivos Y tiene tag/alias
                    if not (has_text or has_richText or has_checkbox or has_dropDownList or has_comboBox or has_date or has_picture):
                        # Es un text field libre (sin restricciones)
                        text_field_obj = form_text_field.FormTextFieldModern()
                        
                        # xml_node = todo el contenido de w:sdt
                        text_field_obj.xml_node = sdt
                        
                        # tag = valor de w:tag/@w:val
                        tag_elem = sdt_pr.find('w:tag', self.namespaces)
                        text_field_obj.tag = tag_elem.get(qn('w:val')) if tag_elem is not None else ""
                        
                        # alias = valor de w:alias/@w:val
                        alias_elem = sdt_pr.find('w:alias', self.namespaces)
                        text_field_obj.alias = alias_elem.get(qn('w:val')) if alias_elem is not None else None
                        
                        # placeholder = valor de w:placeholder/@w:val
                        placeholder_elem = sdt_pr.find('w:placeholder', self.namespaces)
                        if placeholder_elem is not None:
                            doc_part = placeholder_elem.find('w:docPart', self.namespaces)
                            text_field_obj.placeholder = doc_part.get(qn('w:val')) if doc_part is not None else None
                        
                        # Solo procesar si tiene tag
                        if text_field_obj.tag and text_field_obj.tag.strip():
                            # Usar tag como identificador
                            identifier = text_field_obj.tag
                            
                            # Incrementar contador para este identificador
                            if identifier not in name_counters:
                                name_counters[identifier] = 0
                            name_counters[identifier] += 1
                            
                            # xpath = ruta ÚNICA al w:sdt por tag y posición
                            position = name_counters[identifier]
                            text_field_obj.xpath = f"(//w:sdt[w:sdtPr/w:tag/@w:val='{text_field_obj.tag}' and not(w:sdtPr/w:text or w:sdtPr/w:richText or w:sdtPr/w14:checkbox)])[{position}]"
                            
                            # text = contenido actual del campo
                            sdt_content = sdt.find('w:sdtContent', self.namespaces)
                            if sdt_content is not None:
                                # Extraer texto de todos los runs
                                text_content = ""
                                for paragraph in sdt_content.findall('.//w:p', self.namespaces):
                                    for run in paragraph.findall('w:r', self.namespaces):
                                        for text_elem in run.findall('w:t', self.namespaces):
                                            if text_elem.text:
                                                text_content += text_elem.text
                                text_field_obj.text = text_content
                            
                            text_fields_found.append(text_field_obj)
        
        return text_fields_found
    
    def set_field_text_value(self, text_field_obj, value: str):
        """
        Establece el valor de un campo de texto libre
        
        Args:
            text_field_obj: Objeto FormTextFieldModern
            value: Nuevo valor para el campo de texto
        
        Returns:
            bool: True si se modificó correctamente, False si hubo error
        """
        try:
            # Localizar el elemento sdt
            body_element = self.docx._body._element
            sdts = body_element.findall('.//w:sdt', self.namespaces)
            
            found_count = 0
            identifier = text_field_obj.tag
            target_position = int(text_field_obj.xpath.split('[')[-1].split(']')[0])  # Extraer posición del xpath
            
            for sdt in sdts:
                sdt_pr = sdt.find('w:sdtPr', self.namespaces)
                if sdt_pr is not None:
                    # Verificar que sea un campo libre (sin restricciones)
                    has_text = sdt_pr.find('w:text', self.namespaces) is not None
                    has_richText = sdt_pr.find('w:richText', self.namespaces) is not None
                    has_checkbox = sdt_pr.find('w14:checkbox', self.namespaces) is not None
                    
                    if not (has_text or has_richText or has_checkbox):
                        # Verificar tag
                        tag_elem = sdt_pr.find('w:tag', self.namespaces)
                        current_identifier = tag_elem.get(qn('w:val')) if tag_elem is not None else None
                        
                        if current_identifier == identifier:
                            found_count += 1
                            
                            if found_count == target_position:
                                # Este es el text field correcto
                                sdt_content = sdt.find('w:sdtContent', self.namespaces)
                                
                                if sdt_content is not None:
                                    # Limpiar contenido existente
                                    for paragraph in sdt_content.findall('w:p', self.namespaces):
                                        for run in paragraph.findall('w:r', self.namespaces):
                                            paragraph.remove(run)
                                    
                                    # Crear nuevo contenido
                                    first_paragraph = sdt_content.find('w:p', self.namespaces)
                                    if first_paragraph is None:
                                        first_paragraph = OxmlElement('w:p')
                                        sdt_content.append(first_paragraph)
                                    
                                    if value:  # Solo crear run si hay texto
                                        new_run = OxmlElement('w:r')
                                        new_text = OxmlElement('w:t')
                                        new_text.text = value
                                        new_run.append(new_text)
                                        first_paragraph.append(new_run)
                                
                                return True
            
            return False  # No se encontró el text field
            
        except Exception as e:
            print(f"Error al modificar text field libre: {e}")
            return False
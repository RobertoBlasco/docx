"""
Manager para gestionar checkboxes (legacy y modern) en documentos Word
"""

from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from .base_manager import BaseManager
from models import form_checkbox as form_checkbox


class FieldCheckboxManager(BaseManager):
    def __init__(self, docx_document):
        super().__init__(docx_document)
    
    def get_fields_checkbox(self, includeBody=True, includeHeaders=True, includeFooters=True):
        """
        Encuentra todos los checkboxes (legacy y modern) en el documento
        
        Args:
            includeBody: Buscar en el cuerpo del documento
            includeHeaders: Buscar en headers
            includeFooters: Buscar en footers
        
        Returns:
            List[FormCheckBox]: Lista de objetos checkbox encontrados
        """
        checkboxes_found = []
        
        # Obtener elementos donde buscar
        elements_to_search = self._get_elements_to_search(includeBody, includeHeaders, includeFooters)
        
        # Contador para posiciones únicas por nombre
        name_counters = {}
        
        for element in elements_to_search:
            # 1. Buscar LEGACY checkboxes: w:fldChar/w:ffData/w:checkBox
            fld_chars = element.findall('.//w:fldChar', self.namespaces)
            
            for fld_char in fld_chars:
                ff_data = fld_char.find('w:ffData', self.namespaces)
                if ff_data is not None and ff_data.find('w:checkBox', self.namespaces) is not None:
                    # Es un checkbox legacy
                    checkbox_obj = form_checkbox.FormCheckBoxLegacy()
                    
                    # xml_node = todo el contenido de w:fldChar
                    checkbox_obj.xml_node = fld_char
                    
                    # name = valor de w:name/@w:val
                    name_elem = ff_data.find('w:name', self.namespaces)
                    checkbox_obj.name = name_elem.get(qn('w:val')) if name_elem is not None else ""
                    
                    if checkbox_obj.name and checkbox_obj.name.strip():
                        # Incrementar contador para este nombre
                        if checkbox_obj.name not in name_counters:
                            name_counters[checkbox_obj.name] = 0
                        name_counters[checkbox_obj.name] += 1
                        
                        # xpath = ruta ÚNICA al w:fldChar por nombre y posición
                        position = name_counters[checkbox_obj.name]
                        checkbox_obj.xpath = f"(//w:fldChar[w:ffData/w:name/@w:val='{checkbox_obj.name}' and w:ffData/w:checkBox])[{position}]"
                        
                        # default = estado actual del checkbox
                        checkbox = ff_data.find('w:checkBox', self.namespaces)
                        default_elem = checkbox.find('w:default', self.namespaces) if checkbox is not None else None
                        checkbox_obj.default = 1 if (default_elem is not None and default_elem.get(qn('w:val')) == "1") else 0
                        
                        checkboxes_found.append(checkbox_obj)
            
            # 2. Buscar MODERN checkboxes: w:sdt/w:sdtPr/w14:checkbox
            sdts = element.findall('.//w:sdt', self.namespaces)
            
            for sdt in sdts:
                sdt_pr = sdt.find('w:sdtPr', self.namespaces)
                if sdt_pr is not None and sdt_pr.find('w14:checkbox', self.namespaces) is not None:
                    # Es un checkbox moderno
                    checkbox_obj = form_checkbox.FormCheckBoxModern()
                    
                    # xml_node = todo el contenido de w:sdt
                    checkbox_obj.xml_node = sdt
                    
                    # tag = valor de w:tag/@w:val
                    tag_elem = sdt_pr.find('w:tag', self.namespaces)
                    checkbox_obj.tag = tag_elem.get(qn('w:val')) if tag_elem is not None else ""
                    
                    # alias = valor de w:alias/@w:val
                    alias_elem = sdt_pr.find('w:alias', self.namespaces)
                    checkbox_obj.alias = alias_elem.get(qn('w:val')) if alias_elem is not None else None
                    
                    if (checkbox_obj.tag and checkbox_obj.tag.strip()) or (checkbox_obj.alias and checkbox_obj.alias.strip()):
                        # Usar tag o alias como identificador
                        identifier = checkbox_obj.tag if checkbox_obj.tag and checkbox_obj.tag.strip() else checkbox_obj.alias
                        
                        # Incrementar contador para este identificador
                        if identifier not in name_counters:
                            name_counters[identifier] = 0
                        name_counters[identifier] += 1
                        
                        # xpath = ruta ÚNICA al w:sdt por identificador y posición
                        position = name_counters[identifier]
                        if checkbox_obj.tag and checkbox_obj.tag.strip():
                            checkbox_obj.xpath = f"(//w:sdt[w:sdtPr/w:tag/@w:val='{checkbox_obj.tag}' and w:sdtPr/w14:checkbox])[{position}]"
                        else:
                            checkbox_obj.xpath = f"(//w:sdt[w:sdtPr/w:alias/@w:val='{checkbox_obj.alias}' and w:sdtPr/w14:checkbox])[{position}]"
                        
                        # checked = estado actual del checkbox
                        checkbox_elem = sdt_pr.find('w14:checkbox', self.namespaces)
                        checked_elem = checkbox_elem.find('w14:checked', self.namespaces) if checkbox_elem is not None else None
                        # Para Modern checkboxes, leer el namespace w14:val
                        checkbox_obj.checked = 1 if (checked_elem is not None and checked_elem.get(qn('w14:val')) == "1") else 0
                        
                        # Leer los valores de estado del checkbox (checked/unchecked states)
                        checked_state_elem = checkbox_elem.find('w14:checkedState', self.namespaces) if checkbox_elem is not None else None
                        unchecked_state_elem = checkbox_elem.find('w14:uncheckedState', self.namespaces) if checkbox_elem is not None else None
                        
                        if checked_state_elem is not None:
                            checkbox_obj.checked_state = checked_state_elem.get(qn('w14:val'))
                        if unchecked_state_elem is not None:
                            checkbox_obj.unchecked_state = unchecked_state_elem.get(qn('w14:val'))
                        
                        checkboxes_found.append(checkbox_obj)
        
        return checkboxes_found
    
    def set_field_checkbox_value(self, checkbox_obj, value: bool):
        """
        Activa o desactiva un checkbox modificando directamente el XML del documento
        
        Args:
            checkbox_obj: Objeto FormCheckBoxLegacy o FormCheckBoxModern  
            value: True para activar, False para desactivar
        
        Returns:
            bool: True si se modificó correctamente, False si hubo error
        """
        try:
            new_val_str = "1" if value else "0"
            
            # Determinar si es legacy o modern
            if hasattr(checkbox_obj, 'name'):  # Legacy
                # Localizar el elemento usando xpath (simulado con find)
                # Buscar por nombre en todo el documento
                body_element = self.docx._body._element
                fld_chars = body_element.findall('.//w:fldChar', self.namespaces)
                
                found_count = 0
                target_position = int(checkbox_obj.xpath.split('[')[-1].split(']')[0])  # Extraer posición del xpath
                
                for fld_char in fld_chars:
                    ff_data = fld_char.find('w:ffData', self.namespaces)
                    if ff_data is not None:
                        checkbox = ff_data.find('w:checkBox', self.namespaces)
                        if checkbox is not None:
                            name_elem = ff_data.find('w:name', self.namespaces)
                            if name_elem is not None and name_elem.get(qn('w:val')) == checkbox_obj.name:
                                found_count += 1
                                
                                if found_count == target_position:
                                    # Este es el checkbox correcto
                                    default_elem = checkbox.find('w:default', self.namespaces)
                                    
                                    if default_elem is not None:
                                        default_elem.set(qn('w:val'), new_val_str)
                                    else:
                                        # Crear elemento default si no existe
                                        default_elem = OxmlElement('w:default')
                                        default_elem.set(qn('w:val'), new_val_str)
                                        checkbox.append(default_elem)
                                    
                                    return True
            
            else:  # Modern (tiene tag/alias)
                # Localizar el elemento sdt
                body_element = self.docx._body._element
                sdts = body_element.findall('.//w:sdt', self.namespaces)
                
                found_count = 0
                identifier = checkbox_obj.tag if checkbox_obj.tag else checkbox_obj.alias
                target_position = int(checkbox_obj.xpath.split('[')[-1].split(']')[0])  # Extraer posición del xpath
                
                for sdt in sdts:
                    sdt_pr = sdt.find('w:sdtPr', self.namespaces)
                    if sdt_pr is not None:
                        checkbox_elem = sdt_pr.find('w14:checkbox', self.namespaces)
                        if checkbox_elem is not None:
                            # Verificar tag o alias
                            tag_elem = sdt_pr.find('w:tag', self.namespaces)
                            alias_elem = sdt_pr.find('w:alias', self.namespaces)
                            
                            current_identifier = None
                            if tag_elem is not None:
                                current_identifier = tag_elem.get(qn('w:val'))
                            elif alias_elem is not None:
                                current_identifier = alias_elem.get(qn('w:val'))
                            
                            if current_identifier == identifier:
                                found_count += 1
                                
                                if found_count == target_position:
                                    # Este es el checkbox correcto
                                    checked_elem = checkbox_elem.find('w14:checked', self.namespaces)
                                    
                                    if checked_elem is not None:
                                        # Para Modern checkboxes usar namespace w14
                                        checked_elem.set(qn('w14:val'), new_val_str)
                                    else:
                                        # Crear elemento checked si no existe
                                        checked_elem = OxmlElement('w14:checked')
                                        checked_elem.set(qn('w14:val'), new_val_str)
                                        checkbox_elem.append(checked_elem)
                                    
                                    # CRÍTICO: También actualizar el texto visual del checkbox
                                    text_elem = sdt.find('.//w:t', self.namespaces)
                                    if text_elem is not None:
                                        # Usar códigos de caracteres Unicode estándar para checkboxes
                                        if value:
                                            text_elem.text = chr(0x2612)  # ☒ BALLOT BOX WITH X
                                        else:
                                            text_elem.text = chr(0x2610)  # ☐ BALLOT BOX
                                    
                                    return True
            
            return False  # No se encontró el checkbox
            
        except Exception as e:
            print(f"Error al modificar checkbox en documento: {e}")
            return False
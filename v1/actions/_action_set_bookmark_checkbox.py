#!/usr/bin/env python3
"""
ActionSetFormCheckbox - Implementación usando solo python-docx
Reemplaza la implementación anterior que usaba lxml y chilkat2
"""

import logging
import time

from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# logger = logging.getLogger("IneoDocx")

# class ActionSetFormCheckbox:
#     """
#     Acción para establecer el valor de checkboxes de formulario usando python-docx
#     """
    
#     def __init__(self, document_path: str):
#         """
#         Inicializa la acción con el documento a modificar
        
#         Args:
#             document_path: Ruta al documento .docx
#         """
#         self.document_path = document_path
#         self.document = None
        
#     def load_document(self):
#         """Carga el documento Word"""
#         try:
#             self.document = Document(self.document_path)
#             logger.info(f"Documento cargado: {self.document_path}")
#             return True
#         except Exception as e:
#             logger.error(f"Error cargando documento: {e}")
#             return False
    
#     def find_checkbox_by_name(self, checkbox_name: str):
#         """
#         Busca un checkbox por su nombre
        
#         Args:
#             checkbox_name: Nombre del checkbox a buscar
            
#         Returns:
#             list: Lista de elementos checkbox encontrados
#         """
#         if not self.document:
#             logger.error("Documento no cargado")
#             return []
            
#         found_checkboxes = []
        
#         # Buscar en todo el documento
#         body_element = self.document._body._element
        
#         # Encontrar todos los elementos fldChar
#         fld_chars = body_element.findall('.//w:fldChar', {
#             'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
#         })
        
#         for fld_char in fld_chars:
#             # Verificar que sea un campo de inicio
#             fld_char_type = fld_char.get(qn('w:fldCharType'))
            
#             if fld_char_type == 'begin':
#                 # Buscar datos del campo de formulario
#                 ff_data = fld_char.find(qn('w:ffData'))
                
#                 if ff_data is not None:
#                     # Verificar que sea un checkbox
#                     checkbox = ff_data.find(qn('w:checkBox'))
                    
#                     if checkbox is not None:
#                         # Obtener el nombre del checkbox
#                         name_elem = ff_data.find(qn('w:name'))
#                         current_name = name_elem.get(qn('w:val')) if name_elem is not None else ""
                        
#                         if current_name == checkbox_name:
#                             found_checkboxes.append({
#                                 'fld_char': fld_char,
#                                 'ff_data': ff_data,
#                                 'checkbox': checkbox,
#                                 'name': current_name
#                             })
#                             logger.info(f"Checkbox encontrado: {checkbox_name}")
        
#         return found_checkboxes
    
#     def set_checkbox_value(self, checkbox_name: str, value: bool):
#         """
#         Establece el valor de un checkbox
        
#         Args:
#             checkbox_name: Nombre del checkbox
#             value: Valor booleano (True = marcado, False = desmarcado)
            
#         Returns:
#             bool: True si se modificó al menos un checkbox
#         """
#         checkboxes = self.find_checkbox_by_name(checkbox_name)
        
#         if not checkboxes:
#             logger.warning(f"No se encontró checkbox con nombre: {checkbox_name}")
#             return False
        
#         modifications_made = 0
#         new_val_str = "1" if value else "0"
        
#         for checkbox_data in checkboxes:
#             checkbox = checkbox_data['checkbox']
            
#             # Obtener el elemento default actual
#             default_elem = checkbox.find(qn('w:default'))
#             current_val = default_elem.get(qn('w:val')) if default_elem is not None else "0"
            
#             if current_val != new_val_str:
#                 # Modificar el valor
#                 if default_elem is not None:
#                     default_elem.set(qn('w:val'), new_val_str)
#                 else:
#                     # Crear nuevo elemento default si no existe
#                     default_elem = OxmlElement('w:default')
#                     default_elem.set(qn('w:val'), new_val_str)
#                     checkbox.append(default_elem)
                
#                 logger.info(f"Checkbox '{checkbox_name}' modificado: {current_val} -> {new_val_str}")
#                 modifications_made += 1
#             else:
#                 logger.info(f"Checkbox '{checkbox_name}' ya tiene el valor {new_val_str}")
        
#         return modifications_made > 0
    
#     def set_multiple_checkboxes(self, checkbox_values: dict):
#         """
#         Establece múltiples checkboxes de una vez
        
#         Args:
#             checkbox_values: Diccionario con nombres de checkbox y valores
#                            Ejemplo: {'AT': True, 'ST': False, 'HI': True}
                           
#         Returns:
#             dict: Resultado de las modificaciones
#         """
#         results = {}
#         total_modifications = 0
        
#         for checkbox_name, value in checkbox_values.items():
#             success = self.set_checkbox_value(checkbox_name, value)
#             results[checkbox_name] = success
#             if success:
#                 total_modifications += 1
        
#         logger.info(f"Total de checkboxes modificados: {total_modifications}")
#         return {
#             'results': results,
#             'total_modifications': total_modifications
#         }
    
#     def save_document(self, output_path: str = None):
#         """
#         Guarda el documento modificado
        
#         Args:
#             output_path: Ruta de salida. Si es None, sobrescribe el original
            
#         Returns:
#             bool: True si se guardó correctamente
#         """
#         if not self.document:
#             logger.error("No hay documento para guardar")
#             return False
            
#         try:
#             save_path = output_path or self.document_path
#             self.document.save(save_path)
#             logger.info(f"Documento guardado en: {save_path}")
#             return True
#         except Exception as e:
#             logger.error(f"Error guardando documento: {e}")
#             return False
    
#     def get_checkbox_info(self, checkbox_name: str = None):
#         """
#         Obtiene información sobre checkboxes
        
#         Args:
#             checkbox_name: Nombre específico del checkbox. Si es None, devuelve todos
            
#         Returns:
#             list: Lista con información de los checkboxes
#         """
#         if not self.document:
#             logger.error("Documento no cargado")
#             return []
            
#         checkboxes_info = []
        
#         # Buscar en todo el documento
#         body_element = self.document._body._element
        
#         # Encontrar todos los elementos fldChar
#         fld_chars = body_element.findall('.//w:fldChar', {
#             'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
#         })
        
#         for fld_char in fld_chars:
#             # Verificar que sea un campo de inicio
#             fld_char_type = fld_char.get(qn('w:fldCharType'))
            
#             if fld_char_type == 'begin':
#                 # Buscar datos del campo de formulario
#                 ff_data = fld_char.find(qn('w:ffData'))
                
#                 if ff_data is not None:
#                     # Verificar que sea un checkbox
#                     checkbox = ff_data.find(qn('w:checkBox'))
                    
#                     if checkbox is not None:
#                         # Obtener información del checkbox
#                         name_elem = ff_data.find(qn('w:name'))
#                         current_name = name_elem.get(qn('w:val')) if name_elem is not None else ""
                        
#                         # Filtrar por nombre si se especificó
#                         if checkbox_name is None or current_name == checkbox_name:
#                             # Obtener valor actual
#                             default_elem = checkbox.find(qn('w:default'))
#                             current_val = default_elem.get(qn('w:val')) if default_elem is not None else "0"
                            
#                             # Obtener estado habilitado
#                             enabled_elem = ff_data.find(qn('w:enabled'))
#                             enabled_val = enabled_elem.get(qn('w:val')) if enabled_elem is not None else "1"
                            
#                             checkbox_info = {
#                                 'name': current_name,
#                                 'value': current_val,
#                                 'is_checked': current_val == "1",
#                                 'enabled': enabled_val
#                             }
                            
#                             checkboxes_info.append(checkbox_info)
        
#         return checkboxes_info

# # Función standalone para compatibilidad con la implementación anterior
# def set_bookmark_field_checkbox(document_path: str, bookmark_name: str, value: bool) -> bool:
#     """
#     Función standalone para establecer checkbox por nombre de bookmark
    
#     Args:
#         document_path: Ruta al documento
#         bookmark_name: Nombre del bookmark/checkbox
#         value: Valor booleano
        
#     Returns:
#         bool: True si se modificó correctamente
#     """
#     action = ActionSetFormCheckbox(document_path)
    
#     if not action.load_document():
#         return False
        
#     success = action.set_checkbox_value(bookmark_name, value)
    
#     if success:
#         action.save_document()
        
#     return success

def create_paragraph_from_xml(xml_element, part):
    from docx.text.paragraph import Paragraph
    return Paragraph(xml_element, part)


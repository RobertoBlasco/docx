"""
Clases de acciones ejecutables que pueden procesar documentos usando managers
"""

from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass


class ExecutableAction(ABC):
    """Clase base para todas las acciones ejecutables"""
    
    def __init__(self, action_id: str):
        self.action_id = action_id
    
    @abstractmethod
    def execute(self, docx_document) -> bool:
        """Ejecuta la acción en el documento"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Devuelve descripción de la acción"""
        pass


class TextReplacementAction(ExecutableAction):
    """Acción para reemplazar texto por texto"""
    
    def __init__(self, action_id: str, manager, replacements: List):
        super().__init__(action_id)
        self.manager = manager
        self.replacements = replacements  # Lista de TextReplacementItem
    
    def execute(self, docx_document) -> bool:
        """Ejecuta todos los reemplazos de texto"""
        success_count = 0
        
        for replacement in self.replacements:
            # Buscar ocurrencias del texto
            occurrences = docx_document.get_text_occurrences(replacement.search_text)
            
            # Reemplazar cada ocurrencia
            for occurrence in occurrences:
                occurrence.replace_text = replacement.replacement_text
                if docx_document.replace_text_occurrence(occurrence):
                    success_count += 1
        
        return success_count > 0
    
    def get_description(self) -> str:
        return f"TextReplacement: {len(self.replacements)} reemplazos"


class TextToImageAction(ExecutableAction):
    """Acción para reemplazar texto por imagen"""
    
    def __init__(self, action_id: str, manager, replacements: List, images_dict: dict):
        super().__init__(action_id)
        self.manager = manager
        self.replacements = replacements  # Lista de ImageReplacementItem
        self.images_dict = images_dict    # Diccionario {id: ruta_imagen}
    
    def execute(self, docx_document) -> bool:
        """Ejecuta todos los reemplazos de texto por imagen"""
        success_count = 0
        
        for replacement in self.replacements:
            # Obtener datos de la imagen
            if replacement.img_id not in self.images_dict:
                print(f"⚠️  Imagen {replacement.img_id} no encontrada")
                continue
            
            image_path = self.images_dict[replacement.img_id]
            
            # Cargar imagen
            try:
                with open(image_path.replace('FILE://', ''), 'rb') as img_file:
                    image_data = img_file.read()
            except Exception as e:
                print(f"❌ Error cargando imagen {image_path}: {e}")
                continue
            
            # Buscar texto para reemplazar
            image_replacements = docx_document.get_text_for_image_replacement(replacement.search_text)
            
            # Reemplazar cada ocurrencia
            for img_replacement in image_replacements:
                img_replacement.image_data = image_data
                img_replacement.width = replacement.width
                img_replacement.height = replacement.height
                
                if docx_document.replace_text_with_image(img_replacement):
                    success_count += 1
        
        return success_count > 0
    
    def get_description(self) -> str:
        return f"TextToImage: {len(self.replacements)} reemplazos por imagen"


class FieldCheckboxAction(ExecutableAction):
    """Acción para establecer valores de checkboxes"""
    
    def __init__(self, action_id: str, manager, checkboxes: List):
        super().__init__(action_id)
        self.manager = manager
        self.checkboxes = checkboxes  # Lista de FieldCheckbox
    
    def execute(self, docx_document) -> bool:
        """Ejecuta todos los cambios de checkbox"""
        success_count = 0
        
        # Obtener todos los checkboxes del documento
        document_checkboxes = docx_document.get_fields_checkbox()
        
        # Crear diccionario para búsqueda rápida (tanto name como tag)
        checkboxes_by_identifier = {}
        for cb in document_checkboxes:
            # Legacy checkboxes tienen 'name'
            if hasattr(cb, 'name') and cb.name:
                checkboxes_by_identifier[cb.name] = cb
            # Modern checkboxes tienen 'tag'
            if hasattr(cb, 'tag') and cb.tag:
                checkboxes_by_identifier[cb.tag] = cb
        
        for checkbox_form in self.checkboxes:
            if checkbox_form.name in checkboxes_by_identifier:
                checkbox_obj = checkboxes_by_identifier[checkbox_form.name]
                if docx_document.set_field_checkbox_value(checkbox_obj, checkbox_form.value):
                    success_count += 1
            else:
                print(f"⚠️  Checkbox '{checkbox_form.name}' no encontrado en documento")
        
        return success_count > 0
    
    def get_description(self) -> str:
        return f"Checkbox: {len(self.checkboxes)} checkboxes"


class FieldTextAction(ExecutableAction):
    """Acción para establecer valores de campos de texto"""
    
    def __init__(self, action_id: str, manager, text_fields: List):
        super().__init__(action_id)
        self.manager = manager
        self.text_fields = text_fields  # Lista de FieldText
    
    def execute(self, docx_document) -> bool:
        """Ejecuta todos los cambios de campos de texto"""
        success_count = 0
        
        # Obtener todos los campos de texto del documento
        document_fields = docx_document.get_fields_text()
        
        # Crear diccionario por tag para búsqueda rápida
        fields_by_tag = {}
        for field in document_fields:
            if hasattr(field, 'name'):  # Legacy
                if field.name:
                    fields_by_tag[field.name] = field
            else:  # Modern
                if field.tag:
                    fields_by_tag[field.tag] = field
        
        for text_field_form in self.text_fields:
            if text_field_form.tag in fields_by_tag:
                field_obj = fields_by_tag[text_field_form.tag]
                if docx_document.set_field_text_value(field_obj, text_field_form.value):
                    success_count += 1
            else:
                print(f"⚠️  Campo de texto '{text_field_form.tag}' no encontrado en documento")
        
        return success_count > 0
    
    def get_description(self) -> str:
        return f"TextField: {len(self.text_fields)} campos de texto"





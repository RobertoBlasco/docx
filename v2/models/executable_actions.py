"""
Clases de acciones ejecutables que pueden procesar documentos usando managers
"""

from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass
from utils.content_loader import load_content


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
            
            # Cargar imagen usando content_loader
            try:
                image_data = load_content(image_path)
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


class FieldImageAction(ExecutableAction):
    """Acción para insertar imágenes en campos de imagen"""
    
    def __init__(self, action_id: str, manager, image_fields: List, images_dict: dict):
        super().__init__(action_id)
        self.manager = manager
        self.image_fields = image_fields  # Lista de FieldImage del XML
        self.images_dict = images_dict    # Diccionario {id: ruta_imagen}
    
    def execute(self, docx_document) -> bool:
        """
        Ejecuta la inserción de imágenes en campos
        
        Args:
            docx_document: DocxDocument con managers inicializados
        
        Returns:
            bool: True si al menos una inserción fue exitosa
            
        # ESTRUCTURA LISTA - TU LÓGICA DE ORQUESTACIÓN AQUÍ
        # 1. Obtener campos de imagen del documento
        # 2. Hacer matching con configuración XML
        # 3. Cargar imágenes desde archivos
        # 4. Llamar a manager para insertar cada imagen
        # 5. Contar éxitos/fallos y reportar
        """
        success_count = 0
        total_count = len(self.image_fields)
        
        print(f"INFO: Ejecutando FieldImageAction con {total_count} campos configurados")
        
        # Obtener todos los campos de imagen del documento
        image_fields_in_doc = docx_document.get_fields_image()
        print(f"INFO: Detectados {len(image_fields_in_doc)} campos de imagen en documento")
        
        for field_config in self.image_fields:
            # TU LÓGICA AQUÍ:
            # 1. Buscar campo correspondiente en documento por tag
            # 2. Cargar imagen desde self.images_dict usando field_config.img_id
            # 3. Llamar docx_document.set_field_image_value()
            # 4. Incrementar success_count si exitoso
            
            print(f"INFO: Configurado para insertar imagen en campo '{field_config.tag}' - IMG:{field_config.img_id} ({field_config.width}x{field_config.height})")
            
            # Placeholder - reemplazar con tu implementación
            # success = self._process_single_image_field(docx_document, field_config, image_fields_in_doc)
            # if success:
            #     success_count += 1
        
        print(f"INFO: FieldImageAction completada - {success_count}/{total_count} éxitos")
        return success_count > 0
    
    def _process_single_image_field(self, docx_document, field_config, image_fields_in_doc):
        """
        Procesa un solo campo de imagen
        
        Args:
            docx_document: DocxDocument
            field_config: FieldImage del XML con configuración
            image_fields_in_doc: Lista de campos detectados en documento
        
        Returns:
            bool: True si exitoso
            
        # TU LÓGICA AQUÍ para procesar un campo individual
        """
        # Buscar matching field
        matching_field = None
        for doc_field in image_fields_in_doc:
            if hasattr(doc_field, 'tag') and doc_field.tag == field_config.tag:
                matching_field = doc_field
                break
                
        if not matching_field:
            print(f"ERROR: Campo '{field_config.tag}' no encontrado en documento")
            return False
            
        # Cargar imagen
        if field_config.img_id not in self.images_dict:
            print(f"ERROR: Imagen ID {field_config.img_id} no encontrada")
            return False
            
        image_path = self.images_dict[field_config.img_id]
        
        try:
            image_data = load_content(image_path)
        except Exception as e:
            print(f"ERROR: No se pudo cargar imagen {image_path}: {e}")
            return False
            
        # Insertar imagen
        success = docx_document.set_field_image_value(
            matching_field,
            image_data,
            field_config.width,
            field_config.height
        )
        
        if success:
            print(f"OK: Imagen insertada en campo '{field_config.tag}'")
        else:
            print(f"ERROR: Falló inserción en campo '{field_config.tag}'")
            
        return success
    
    def get_description(self) -> str:
        return f"FieldImage: {len(self.image_fields)} campos de imagen"





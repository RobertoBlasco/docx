"""
DocxDocument - Coordinador principal para manipular documentos Word
Refactorizado para usar managers especializados
"""

import io
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from docx import Document
from managers.checkbox_manager import CheckboxManager
from managers.text_manager import TextManager
from managers.image_manager import ImageManager


class DocxDocument:
    def __init__(self, bytes):
        """
        Inicializa el documento Word y sus managers
        
        Args:
            bytes: Bytes del archivo .docx
        """
        self.docx = None
        if bytes is not None:
            self.docx = Document(io.BytesIO(bytes))
            
            # Inicializar managers especializados
            self.checkbox_manager = CheckboxManager(self.docx)
            self.text_manager = TextManager(self.docx)
            self.image_manager = ImageManager(self.docx)
    
    # === MÉTODOS DE CHECKBOXES ===
    def get_checkboxes(self, includeBody=True, includeHeaders=True, includeFooters=True):
        """
        Encuentra todos los checkboxes (legacy y modern) en el documento
        
        Args:
            includeBody: Buscar en el cuerpo del documento
            includeHeaders: Buscar en headers
            includeFooters: Buscar en footers
        
        Returns:
            List[FormCheckBox]: Lista de objetos checkbox encontrados
        """
        return self.checkbox_manager.get_checkboxes(includeBody, includeHeaders, includeFooters)
    
    def set_checkbox_value(self, checkbox_obj, value: bool):
        """
        Activa o desactiva un checkbox modificando directamente el XML del documento
        
        Args:
            checkbox_obj: Objeto FormCheckBoxLegacy o FormCheckBoxModern  
            value: True para activar, False para desactivar
        
        Returns:
            bool: True si se modificó correctamente, False si hubo error
        """
        return self.checkbox_manager.set_checkbox_value(checkbox_obj, value)
    
    # === MÉTODOS DE TEXTO ===
    def get_text_occurrences(self, search_text: str, includeBody=True, includeHeaders=True, includeFooters=True):
        """
        Encuentra todas las ocurrencias de un texto en el documento
        
        Args:
            search_text: Texto a buscar
            includeBody: Buscar en el cuerpo del documento
            includeHeaders: Buscar en headers
            includeFooters: Buscar en footers
        
        Returns:
            List[FormTextReplacement]: Lista de objetos con las ocurrencias encontradas
        """
        return self.text_manager.get_text_occurrences(search_text, includeBody, includeHeaders, includeFooters)
    
    def replace_text_occurrence(self, replacement_obj):
        """
        Reemplaza texto en un run específico usando el objeto FormTextReplacement
        
        Args:
            replacement_obj: Objeto FormTextReplacement con run_node, search_text y replace_text
        
        Returns:
            bool: True si se reemplazó correctamente, False si hubo error
        """
        return self.text_manager.replace_text_occurrence(replacement_obj)
    
    # === MÉTODOS DE IMAGEN ===
    def get_text_for_image_replacement(self, search_text: str, includeBody=True, includeHeaders=True, includeFooters=True):
        """
        Encuentra todas las ocurrencias de texto que pueden ser reemplazadas por imagen
        
        Args:
            search_text: Texto a buscar
            includeBody: Buscar en el cuerpo del documento
            includeHeaders: Buscar en headers
            includeFooters: Buscar en footers
        
        Returns:
            List[TextImageReplacement]: Lista de objetos con las ocurrencias encontradas
        """
        return self.image_manager.get_text_for_image_replacement(search_text, includeBody, includeHeaders, includeFooters)
    
    def replace_text_with_image(self, replacement_obj):
        """
        Reemplaza texto por imagen en un párrafo específico
        
        Args:
            replacement_obj: Objeto TextImageReplacement con datos del reemplazo
        
        Returns:
            bool: True si se reemplazó correctamente, False si hubo error
        """
        return self.image_manager.replace_text_with_image(replacement_obj)
    
    # === MÉTODOS DEL DOCUMENTO ===
    def save_to_file(self, file_path):
        """Guarda el documento con las modificaciones"""
        if self.docx:
            self.docx.save(file_path)
        else:
            raise ValueError("Documento no inicializado")
    
    def get_bytes(self):
        """
        Obtiene los bytes del documento modificado
        
        Returns:
            bytes: Documento en formato bytes
        """
        if self.docx:
            doc_stream = io.BytesIO()
            self.docx.save(doc_stream)
            doc_stream.seek(0)
            return doc_stream.read()
        else:
            raise ValueError("Documento no inicializado")
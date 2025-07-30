"""
Manager unificado para gestionar todos los tipos de campos de texto en documentos Word
Orquesta managers especializados para cada tipo de campo
"""

from .base_manager import BaseManager
from .field_text_legacy_manager import FieldTextLegacyManager
from .field_text_plain_manager import FieldTextPlainManager
from .field_text_free_manager import FieldTextFreeManager  
from .field_text_rich_manager import FieldTextRichManager


class FieldTextManager(BaseManager):
    def __init__(self, docx_document):
        super().__init__(docx_document)
        
        # Inicializar managers especializados
        self.legacy_manager = FieldTextLegacyManager(docx_document)
        self.plain_manager = FieldTextPlainManager(docx_document)
        self.free_manager = FieldTextFreeManager(docx_document)
        self.rich_manager = FieldTextRichManager(docx_document)
    
    def get_fields_text(self, includeBody=True, includeHeaders=True, includeFooters=True):
        """
        Encuentra todos los campos de texto (todos los tipos) en el documento
        
        Args:
            includeBody: Buscar en el cuerpo del documento
            includeHeaders: Buscar en headers
            includeFooters: Buscar en footers
        
        Returns:
            List[FormTextField]: Lista de objetos text field encontrados de todos los tipos
        """
        all_text_fields = []
        
        # Recopilar campos de todos los managers especializados
        all_text_fields.extend(self.legacy_manager.get_fields_text(includeBody, includeHeaders, includeFooters))
        all_text_fields.extend(self.plain_manager.get_fields_text(includeBody, includeHeaders, includeFooters))
        all_text_fields.extend(self.free_manager.get_fields_text(includeBody, includeHeaders, includeFooters))
        all_text_fields.extend(self.rich_manager.get_fields_text(includeBody, includeHeaders, includeFooters))
        
        return all_text_fields
    
    def set_field_text_value(self, text_field_obj, value: str):
        """
        Establece el valor de un campo de texto delegando al manager especializado apropiado
        
        Args:
            text_field_obj: Objeto FormTextFieldLegacy o FormTextFieldModern  
            value: Nuevo valor para el campo de texto
        
        Returns:
            bool: True si se modificó correctamente, False si hubo error
        """
        try:
            # Determinar el tipo de campo y delegar al manager apropiado
            if hasattr(text_field_obj, 'name'):
                # Es un campo Legacy
                return self.legacy_manager.set_field_text_value(text_field_obj, value)
            else:
                # Es un campo Modern - necesitamos determinar el subtipo
                # Analizamos el xpath para determinar el tipo
                xpath = text_field_obj.xpath
                
                if 'w:text]' in xpath:
                    # Campo Plain (con restricción w:text)
                    return self.plain_manager.set_field_text_value(text_field_obj, value)
                elif 'w:richText]' in xpath:
                    # Campo Rich (con capacidades de formato)
                    return self.rich_manager.set_field_text_value(text_field_obj, value)
                else:
                    # Campo Free (sin restricciones)
                    return self.free_manager.set_field_text_value(text_field_obj, value)
            
        except Exception as e:
            print(f"Error al modificar text field en documento: {e}")
            return False
    
    # Métodos de acceso directo a managers especializados (opcional)
    def get_legacy_fields_text(self, includeBody=True, includeHeaders=True, includeFooters=True):
        """Obtiene solo campos Legacy"""
        return self.legacy_manager.get_fields_text(includeBody, includeHeaders, includeFooters)
    
    def get_plain_fields_text(self, includeBody=True, includeHeaders=True, includeFooters=True):
        """Obtiene solo campos Plain (w:text)"""
        return self.plain_manager.get_fields_text(includeBody, includeHeaders, includeFooters)
    
    def get_free_fields_text(self, includeBody=True, includeHeaders=True, includeFooters=True):
        """Obtiene solo campos Free (contenido libre)"""
        return self.free_manager.get_fields_text(includeBody, includeHeaders, includeFooters)
    
    def get_rich_fields_text(self, includeBody=True, includeHeaders=True, includeFooters=True):
        """Obtiene solo campos Rich (w:richText)"""
        return self.rich_manager.get_fields_text(includeBody, includeHeaders, includeFooters)
    
    def get_fields_text_by_type(self):
        """
        Obtiene campos organizados por tipo
        
        Returns:
            dict: Diccionario con campos organizados por tipo
        """
        return {
            'legacy': self.get_legacy_fields(),
            'plain': self.get_plain_fields(),
            'free': self.get_free_fields(),
            'rich': self.get_rich_fields()
        }
    
    def get_field_text_statistics(self):
        """
        Obtiene estadísticas de campos por tipo
        
        Returns:
            dict: Diccionario con conteos por tipo
        """
        fields_by_type = self.get_fields_text_by_type()
        
        return {
            'legacy_count': len(fields_by_type['legacy']),
            'plain_count': len(fields_by_type['plain']),
            'free_count': len(fields_by_type['free']),
            'rich_count': len(fields_by_type['rich']),
            'total_count': sum(len(fields) for fields in fields_by_type.values())
        }
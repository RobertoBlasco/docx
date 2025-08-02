"""
Modelos para campos de imagen en documentos Word
Base classes para representar campos de imagen (modernos y legacy)
"""

class FieldImage:
    """
    Clase base para campos de imagen en documentos Word
    Representa un campo que puede contener una imagen
    """
    
    def __init__(self):
        self.tag = None          # Tag del campo (modern)
        self.alias = None        # Alias del campo (modern)
        self.name = None         # Nombre del campo (legacy)
        self.xpath = None        # XPath para localizar el campo
        self.xml_node = None     # Nodo XML del campo
        
    def get_current_image_info(self):
        """
        Obtiene información de la imagen actual en el campo
        
        Returns:
            dict: {
                'has_image': bool,
                'width': int,
                'height': int,
                'format': str,
                'relation_id': str
            } o None si no hay imagen
        
        # TU LÓGICA AQUÍ
        # Analizar el contenido del campo para determinar si tiene imagen
        # Extraer dimensiones, formato y relación si existe
        """
        pass
    
    def has_image(self):
        """
        Verifica si el campo contiene actualmente una imagen
        
        Returns:
            bool: True si tiene imagen, False si está vacío
            
        # TU LÓGICA AQUÍ
        # Analizar el XML del campo para detectar presencia de imagen
        """
        return False
    
    def get_value(self):
        """
        Alias para has_image() para consistencia con otros field types
        
        Returns:
            bool: True si tiene imagen
        """
        return self.has_image()
    
    def is_empty(self):
        """
        Verifica si el campo está vacío (sin imagen)
        
        Returns:
            bool: True si no tiene imagen
        """
        return not self.has_image()


class FieldImageModern(FieldImage):
    """
    Campo de imagen moderno (SDT - Structured Document Tag)
    Para documentos Word modernos que usan controles de contenido
    """
    
    def __init__(self):
        super().__init__()
        self.sdt_id = None       # ID del SDT
        self.is_picture_sdt = None  # Indica si es específicamente un SDT de imagen
        
    def get_current_image_info(self):
        """
        Implementación específica para campos modernos (SDT)
        
        Returns:
            dict: Información de la imagen o None
            
        # TU LÓGICA AQUÍ
        # 1. Verificar que el SDT es de tipo imagen (w:picture)
        # 2. Buscar w:drawing dentro del w:sdtContent
        # 3. Extraer información de wp:inline, dimensiones, etc.
        # 4. Obtener relation_id del a:blip r:embed
        """
        pass
    
    def has_image(self):
        """
        Verifica si el SDT contiene una imagen
        
        Returns:
            bool: True si contiene imagen
            
        # TU LÓGICA AQUÍ
        # Buscar elementos w:drawing dentro del w:sdtContent
        # Verificar que existe estructura completa de imagen
        """
        return False
    
    def get_sdt_content_element(self):
        """
        Obtiene el elemento w:sdtContent del SDT
        
        Returns:
            xml.etree.ElementTree.Element: Elemento sdtContent o None
            
        # TU LÓGICA AQUÍ
        # Navegar por el XML hasta encontrar w:sdtContent
        """
        pass
    
    def is_image_control(self):
        """
        Verifica si el SDT está configurado específicamente para imágenes
        
        Returns:
            bool: True si es un control de imagen
            
        # TU LÓGICA AQUÍ
        # Verificar en w:sdtPr si existe w:picture elemento
        # Esto indica que es un control específico para imágenes
        """
        return False


class FieldImageLegacy(FieldImage):
    """
    Campo de imagen legacy (para compatibilidad futura)
    Para documentos Word antiguos con controles ActiveX o similares
    """
    
    def __init__(self):
        super().__init__()
        # Por ahora no implementado - placeholder para futuro
        
    def get_current_image_info(self):
        """
        Implementación para campos legacy (no implementado)
        
        # TU LÓGICA AQUÍ si necesitas soportar campos legacy
        """
        return None
    
    def has_image(self):
        """
        Verificación para campos legacy (no implementado)
        
        # TU LÓGICA AQUÍ si necesitas soportar campos legacy
        """
        return False
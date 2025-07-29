"""
Clase base para todos los managers de DocxDocument
"""

class BaseManager:
    def __init__(self, docx_document):
        """
        Inicializa el manager base
        
        Args:
            docx_document: Instancia de Document de python-docx
        """
        self.docx = docx_document
        
        # Namespaces comunes para XML
        self.namespaces = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            'w14': 'http://schemas.microsoft.com/office/word/2010/wordml'
        }
    
    def _get_elements_to_search(self, includeBody=True, includeHeaders=True, includeFooters=True):
        """
        Obtiene los elementos del documento donde buscar
        
        Returns:
            list: Lista de elementos XML para procesar
        """
        elements_to_search = []
        
        if includeBody:
            elements_to_search.append(self.docx._body._element)
        
        if includeHeaders:
            for section in self.docx.sections:
                if section.header._element is not None:
                    elements_to_search.append(section.header._element)
        
        if includeFooters:
            for section in self.docx.sections:
                if section.footer._element is not None:
                    elements_to_search.append(section.footer._element)
        
        return elements_to_search
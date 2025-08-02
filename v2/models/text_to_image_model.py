"""
Modelo para representar reemplazo de texto por imagen en documentos Word
"""


class TextImageReplacement:
    def __init__(self):
        """
        Inicializa un objeto para reemplazar texto por imagen
        """
        self.search_text = None      # Texto a buscar y reemplazar
        self.image_data = None       # Bytes de la imagen (bytes)
        self.width = None            # Ancho de la imagen en píxeles
        self.height = None           # Alto de la imagen en píxeles
        self.paragraph_node = None   # Referencia al párrafo que contiene el texto
        self.xpath = None            # XPath para localizar el párrafo específico
        self.location = None         # Ubicación: "body", "header", "footer", "table", "textbox"
        
    def __str__(self):
        image_size = f"{self.width}x{self.height}" if self.width and self.height else "auto"
        return f"TextImageReplacement(search='{self.search_text}', size={image_size}, location='{self.location}')"
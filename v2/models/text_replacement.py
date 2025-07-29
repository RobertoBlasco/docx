class FormTextReplacement:
    def __init__(self):
        self.search_text = None      # Texto a buscar
        self.replace_text = None     # Texto de reemplazo  
        self.run_node = None         # Nodo run donde está el texto (paragraph.runs[i])
        self.xpath = None            # XPath para localizar el run específico
        self.location = None         # "body", "header", "footer", "table", "textbox"
    
    def __str__(self):
        return f"FormTextReplacement(search='{self.search_text}', location='{self.location}')"
    
    
    
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

class FormTextField:
    def __init__(self):
        self.xpath = None
        self.xml_node = None
    
    def get_value(self):
        """Método abstracto para obtener valor"""
        raise NotImplementedError

    def set_value(self, value: str):
        """Método abstracto para establecer valor"""
        raise NotImplementedError


class FormTextFieldLegacy(FormTextField):
    def __init__(self):
        super().__init__()
        self.name = None
        self.default = ""
    
    def __str__(self):
        return f"FormTextFieldLegacy(name='{self.name}', default='{self.default}')"
    
    def get_value(self) -> str:
        return self.default

    def set_value(self, value: str):
        """Modifica el valor del campo de texto legacy en el XML"""
        if self.xml_node is None:
            raise ValueError("xml_node no está inicializado")

        # Buscar el elemento w:textInput dentro del nodo
        textinput_elem = self.xml_node.find('.//w:textInput', {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        })

        if textinput_elem is not None:
            # Buscar el elemento w:default
            default_elem = textinput_elem.find('w:default', {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            })

            if default_elem is not None:
                # Modificar el valor existente
                default_elem.set(qn('w:val'), value)
            else:
                # Crear nuevo elemento w:default si no existe
                default_elem = OxmlElement('w:default')
                default_elem.set(qn('w:val'), value)
                textinput_elem.append(default_elem)

            # Actualizar el atributo interno
            self.default = value
        else:
            raise ValueError("No se encontró elemento w:textInput en el nodo XML")


class FormTextFieldModern(FormTextField):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.alias = None
        self.tag = None
        self.placeholder = None
    
    def __str__(self):
        tag_info = f"tag='{self.tag}'" if self.tag else "tag=None"
        alias_info = f"alias='{self.alias}'" if self.alias else "alias=None"
        return f"FormTextFieldModern({tag_info}, {alias_info}, text='{self.text}')"

    def get_value(self) -> str:
        return self.text

    def set_value(self, value: str):
        """Modifica el valor del campo de texto moderno en el XML"""
        if self.xml_node is None:
            raise ValueError("xml_node no está inicializado")

        # Buscar el elemento w:sdtContent dentro del nodo sdt
        sdt_content = self.xml_node.find('.//w:sdtContent', {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        })

        if sdt_content is not None:
            # Buscar el primer párrafo dentro del contenido
            paragraph = sdt_content.find('w:p', {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            })

            if paragraph is not None:
                # Limpiar contenido existente
                for run in paragraph.findall('w:r', {
                    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
                }):
                    paragraph.remove(run)

                # Crear nuevo run con el texto
                if value:  # Solo crear run si hay texto
                    new_run = OxmlElement('w:r')
                    new_text = OxmlElement('w:t')
                    new_text.text = value
                    new_run.append(new_text)
                    paragraph.append(new_run)

                # Actualizar el atributo interno
                self.text = value
            else:
                # Crear párrafo si no existe
                paragraph = OxmlElement('w:p')
                if value:  # Solo crear run si hay texto
                    new_run = OxmlElement('w:r')
                    new_text = OxmlElement('w:t')
                    new_text.text = value
                    new_run.append(new_text)
                    paragraph.append(new_run)
                sdt_content.append(paragraph)
                self.text = value
        else:
            raise ValueError("No se encontró elemento w:sdtContent en el nodo XML")
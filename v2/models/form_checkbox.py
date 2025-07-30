from docx.oxml.ns import qn
from docx.oxml import OxmlElement

class FormCheckBox :
    def __init__(self) :
        self.xpath = None
        self.xml_node = None
    
    def get_value(self):
          """Método abstracto para obtener valor"""
          raise NotImplementedError

    def set_value(self, value: bool):
        """Método abstracto para establecer valor"""
        raise NotImplementedError


class FormCheckBoxLegacy (FormCheckBox) :
    def __init__(self) :
        super().__init__()
        self.name = None
        self.default = 0
    
    def __str__(self):
      return f"FormCheckBoxLegacy(name='{self.name}', default={self.default})"
    
    def get_value(self) -> bool:
          return self.default == 1

    def set_value(self, value: bool):
        """Modifica el valor del checkbox legacy en el XML"""
        if self.xml_node is None:
            raise ValueError("xml_node no está inicializado")

        # Convertir bool a string
        new_val_str = "1" if value else "0"

        # Buscar el elemento w:checkBox dentro del nodo
        checkbox_elem = self.xml_node.find('.//w:checkBox', {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        })

        if checkbox_elem is not None:
            # Buscar el elemento w:default
            default_elem = checkbox_elem.find(qn('w:default'))

            if default_elem is not None:
                # Modificar el valor existente
                default_elem.set(qn('w:val'), new_val_str)
            else:
                # Crear nuevo elemento w:default si no existe
                default_elem = OxmlElement('w:default')
                default_elem.set(qn('w:val'), new_val_str)
                checkbox_elem.append(default_elem)

            # Actualizar el atributo interno
            self.default = 1 if value else 0
        else:
            raise ValueError("No se encontró elemento w:checkBox en el nodo XML")

class FormCheckBoxModern(FormCheckBox) :

    def __init__(self) :
        super().__init__()
        self.checked = 0
        self.alias = None
        self.tag = None
        self.checked_state = 2612
        self.unchecked_state = 2610
    
    def __str__(self):
      tag_info = f"tag='{self.tag}'" if self.tag else "tag=None"
      alias_info = f"alias='{self.alias}'" if self.alias else "alias=None"
      return f"FormCheckBoxModern({tag_info}, {alias_info}, checked={self.checked})"

    def get_value(self) -> bool:
          return self.checked == 1

    def set_value(self, value: bool):
        """Modifica el valor del checkbox moderno en el XML"""
        if self.xml_node is None:
            raise ValueError("xml_node no está inicializado")

        # Convertir bool a string
        new_val_str = "1" if value else "0"

        # Buscar el elemento w14:checkbox dentro del nodo sdt
        checkbox_elem = self.xml_node.find('.//w14:checkbox', {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            'w14': 'http://schemas.microsoft.com/office/word/2010/wordml'
        })

        if checkbox_elem is not None:
            # Buscar el elemento w14:checked
            checked_elem = checkbox_elem.find('w14:checked', {
                'w14': 'http://schemas.microsoft.com/office/word/2010/wordml'
            })

            if checked_elem is not None:
                # Modificar el valor existente
                checked_elem.set(qn('w:val'), new_val_str)
            else:
                # Crear nuevo elemento w14:checked si no existe
                checked_elem = OxmlElement('w14:checked')
                checked_elem.set(qn('w:val'), new_val_str)
                checkbox_elem.append(checked_elem)

            # Actualizar el atributo interno
            self.checked = 1 if value else 0
        else:
            raise ValueError("No se encontró elemento w14:checkbox en el nodo XML")
"""
Parser robusto para archivos XML de tareas usando xmlschema
"""

import xmlschema
from dataclasses import dataclass
from typing import List, Optional, Union
import os
import logging

logger = logging.getLogger("IneoDocx")

@dataclass
class DataOut:
    path: str
    overwrite: bool = False


@dataclass 
class Image:
    id: str
    path: str
    md5: Optional[str] = None

@dataclass
class TextReplacementItem:
    search_text: str
    replacement_text: str


@dataclass
class ImageReplacementItem:
    search_text: str
    img_id: str
    width: int
    height: int

@dataclass
class FieldCheckbox:
    name: str
    value: bool  # Convertido de "0"/"1" a bool


@dataclass
class FieldText:
    tag: str
    value: str




@dataclass
class Action:
    name: str
    id: str
    items: List[Union[
        TextReplacementItem, 
        ImageReplacementItem, 
        FieldCheckbox, 
        FieldText
    ]]


@dataclass
class DocxTask:
    task: str
    data_in: str
    data_out: DataOut
    images: List[Image]
    actions: List[Action]


class XmlTaskParser:
    def __init__(self, schema_path: str = None):
        """
        Inicializa el parser con validación XSD
        
        Args:
            schema_path: Ruta al archivo .xsd (opcional)
        """
        if schema_path is None:
            # Buscar schema en el mismo directorio
            current_dir = os.path.dirname(__file__)
            schema_path = os.path.join(current_dir, '..', 'tasks', 'docx_task_schema.xsd')
        
        if os.path.exists(schema_path):
            self.schema = xmlschema.XMLSchema(schema_path)
        else:
            logger.warning(f"Schema no encontrado en {schema_path}, usando validación básica")
            self.schema = None
    
    def parse_xml_file(self, xml_file_path: str) -> DocxTask:
        """
        Parsea un archivo XML y lo convierte a objeto DocxTask
        
        Args:
            xml_file_path: Ruta al archivo XML
            
        Returns:
            DocxTask: Objeto con todos los datos parseados
            
        Raises:
            xmlschema.XMLSchemaException: Si el XML no es válido
            FileNotFoundError: Si el archivo no existe
        """
        if not os.path.exists(xml_file_path):
            raise FileNotFoundError(f"Archivo XML no encontrado: {xml_file_path}")
        
        # Validar y convertir a diccionario
        if self.schema:
            try:
                # Validación automática
                xml_dict = self.schema.to_dict(xml_file_path)
                logger.info("XML validado correctamente según el schema")
                
                # DEBUG: Mostrar estructura del diccionario (comentado)
                # print(f"\n🔍 DEBUG - Estructura del diccionario:")
                # import json
                # print(json.dumps(xml_dict, indent=2, ensure_ascii=False)[:1000] + "...")
                
            except xmlschema.XMLSchemaException as e:
                logger.error(f"Error de validación XML: {e}")
                raise
        else:
            # Parseo sin validación
            import xml.etree.ElementTree as ET
            tree = ET.parse(xml_file_path)
            xml_dict = self._xml_to_dict_basic(tree.getroot())
        
        # Convertir diccionario a objetos Python
        return self._dict_to_docx_task(xml_dict)
    
    def _xml_to_dict_basic(self, element):
        """Conversión básica XML a dict (fallback)"""
        result = {}
        
        # Atributos
        if element.attrib:
            result.update(element.attrib)
        
        # Contenido de texto
        if element.text and element.text.strip():
            if len(element) == 0:  # No tiene hijos
                return element.text.strip()
            else:
                result['#text'] = element.text.strip()
        
        # Elementos hijos
        for child in element:
            child_data = self._xml_to_dict_basic(child)
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        return result
    
    def _dict_to_docx_task(self, xml_dict) -> DocxTask:
        """
        Convierte diccionario a objeto DocxTask
        
        Args:
            xml_dict: Diccionario resultante del parsing XML
            
        Returns:
            DocxTask: Objeto tipado
        """
        # xmlschema devuelve el contenido directamente, no anidado en 'ineoDoc'
        root = xml_dict
        
        # DataOut
        data_out_dict = root.get('dataOut', {})
        if isinstance(data_out_dict, str):
            data_out = DataOut(path=data_out_dict)
        else:
            data_out = DataOut(
                path=data_out_dict.get('$', ''),  # xmlschema usa '$' para contenido
                overwrite=data_out_dict.get('@overwrite', False)  # xmlschema usa '@' para atributos
            )
        
        # Images
        images = []
        images_dict = root.get('images', {})
        if images_dict:
            image_list = images_dict.get('image', [])
            if not isinstance(image_list, list):
                image_list = [image_list]
            
            for img_dict in image_list:
                if isinstance(img_dict, str):
                    continue  # Skip malformed entries
                images.append(Image(
                    id=img_dict.get('@id', ''),  # Atributo con @
                    path=img_dict.get('$', ''),  # Contenido con $
                    md5=img_dict.get('@md5')     # Atributo opcional
                ))
        
        # Actions (con generación automática de IDs)
        actions = []
        actions_dict = root.get('actions', {})
        if actions_dict:
            action_list = actions_dict.get('action', [])
            if not isinstance(action_list, list):
                action_list = [action_list]
            
            action_counter = 1
            for action_dict in action_list:
                action = self._parse_action(action_dict, action_counter)
                if action:
                    actions.append(action)
                    action_counter += 1
        
        return DocxTask(
            task=root.get('@task', ''),     # Atributo con @
            data_in=root.get('dataIn', ''), # Elemento normal
            data_out=data_out,
            images=images,
            actions=actions
        )
    
    def _parse_action(self, action_dict, action_counter: int) -> Optional[Action]:
        """
        Parsea una acción específica
        
        Args:
            action_dict: Diccionario con datos de la acción
            action_counter: Contador para generar IDs automáticos
            
        Returns:
            Action: Objeto Action parseado
        """
        action_name = action_dict.get('@name', '')  # Atributo con @
        
        # Generar ID automático siempre
        action_id = f"action_{action_counter}"
            
        items = []
        
        if action_name == 'replaceTextWithText':
            item_list = action_dict.get('item', [])
            if not isinstance(item_list, list):
                item_list = [item_list]
            
            for item in item_list:
                items.append(TextReplacementItem(
                    search_text=item.get('@searchText', ''),  # Atributo con @
                    replacement_text=item.get('$', '')        # Contenido con $
                ))
        
        elif action_name == 'replaceTextWithImage':
            item_list = action_dict.get('item', [])
            if not isinstance(item_list, list):
                item_list = [item_list]
            
            for item in item_list:
                items.append(ImageReplacementItem(
                    search_text=item.get('@searchText', ''),  # Atributo con @
                    img_id=item.get('imgId', ''),              # Elemento normal
                    width=int(item.get('width', 0)),           # Elemento normal
                    height=int(item.get('height', 0))          # Elemento normal
                ))
        
        elif action_name == 'setFieldCheckbox':
            form_list = action_dict.get('form', [])
            if not isinstance(form_list, list):
                form_list = [form_list]
            
            for form in form_list:
                items.append(FieldCheckbox(
                    name=form.get('@name', ''),           # Atributo con @
                    value=form.get('$', '0') == '1'       # Contenido con $
                ))
        
        elif action_name == 'setFieldText':
            form_list = action_dict.get('form', [])
            if not isinstance(form_list, list):
                form_list = [form_list]
            
            for form in form_list:
                items.append(FieldText(
                    tag=form.get('@tag', ''),       # Atributo con @
                    value=form.get('$', '')         # Contenido con $
                ))
        
        
        return Action(name=action_name, id=action_id, items=items) if items else None
    
    def validate_xml_file(self, xml_file_path: str) -> bool:
        """
        Valida un archivo XML contra el schema
        
        Returns:
            bool: True si es válido, False si no
        """
        if not self.schema:
            logger.warning("No hay schema disponible para validación")
            return True
        
        try:
            self.schema.validate(xml_file_path)
            return True
        except xmlschema.XMLSchemaException as e:
            logger.error(f"Error de validación XML: {e}")
            return False
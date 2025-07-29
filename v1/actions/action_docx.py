# import utils
# import logging
# import re
# import base64
# import os

# from enum import StrEnum
# from lxml import etree
# from action_docx import Document
# import data_storage as data_storage

# logger = logging.getLogger("IneoDocx")
# from action_docx import Document
# class ACCIONES(StrEnum):
#     ActionReplaceTextWithText   = "ActionReplaceTextWithText"
#     ActionReplaceTextWithImage  = "ActionReplaceTextWithImage"
#     ActionSetFormCheckbox       = "ActionSetFormCheckbox"
#     ActionSetBookmarkFormCheckbox = "ActionSetBookmarkFormCheckbox"
#     ActionSetBookmarkFormField = "ActionSetBookmarkFormField"
#     ActionSetBookmarkImage      = "ActionSetBookmarkImage"

# class Action :

#     def __init__(self, name) :
#         self.name = name
    
#     def __str__(self):
#         return f"Action({self.name})"
    
#     def __repr__(self):
#         return self.__str__()

# class ActionReplaceTextWithText(Action) :
    
#     def __init__(self, label=None, text=None) :
#         super().__init__(ACCIONES.ActionReplaceTextWithText)
#         self.label = label
#         self.text = text
    
#     def set_label(self, label) :
#         self.label = label

#     def set_text(self, text) :
#         self.text = text
    
#     def __str__(self):
#       return f'{{"action": "{self.name}", "searchText": "{self.label}", "replaceText": "{self.text}"}}'


# class ActionReplaceTextWithImage(Action) :
    
#     def __init__(self, search_text=None, image_id=None, width=None, height=None) :
#         super().__init__(ACCIONES.ActionReplaceTextWithImage)
#         self.search_text = search_text
#         self.image_id = image_id
#         self.width = width
#         self.height = height
    
#     def set_search_text(self, search_text) :
#         self.search_text = search_text

#     def set_image_id(self, image_id) :
#         self.image_id = image_id
        
#     def set_width(self, width : float) :
#         self.width = width
    
#     def set_height(self, height: float) :
#         self.height = height
    
#     def __str__(self):
#         return f'{{"action": "{self.name}", "searchText": "{self.search_text}", "imgId": "{self.image_id}", "width": "{self.width}", "height": "{self.height}"}}'

# # class ActionSetFormCheckbox(Action) : 

# #     def __init__(self, bookmark=None, value=None) :
# #         super().__init__(ACCIONES.ActionSetFormCheckbox)
# #         self.bookmark = bookmark
# #         self.valueId = value
    
# #     def setSearchValue(self, bookmark) :
# #         self.bookmark = bookmark

# #     def setValueId(self, value : str) :
# #         self.value = value
    
# #     def __str__(self):
# #         return f'{{"action": "{self.name}", "boomark": "{self.bookmark}", "value": "{self.value}"}}'

# class ActionSetBookmarkFormCheckbox(Action):
    
#     def __init__(self, bookmark=None, value=None):
#         super().__init__(ACCIONES.ActionSetBookmarkFormCheckbox)
#         self.bookmark = bookmark
#         self.value = value
    
#     def set_bookmark_name(self, bookmark):
#         self.bookmark = bookmark
    
#     def set_value(self, value):
#         self.value = value
    
#     def __str__(self):
#         return f'{{"action": "{self.name}", "boomark": "{self.bookmark}", "value": "{self.value}"}}'

# class ActionSetBookmarkFormField(Action):
    
#     def __init__(self, bookmark_name=None, value=None):
#         super().__init__(ACCIONES.ActionSetBookmarkFormField)
#         self.bookmark_name = bookmark_name
#         self.value = value
    
#     def set_bookmark_name(self, bookmark_name):
#         self.bookmark_name = bookmark_name
    
#     def set_value(self, value):
#         self.value = value
    
#     def __str__(self):
#         return f"SetBookmarkFormField('{self.bookmark_name}' → '{self.value}')"

# class ActionSetBookmarkImage(Action):
    
#     def __init__(self, bookmark_name=None, image_id=None, width=None, height=None):
#         super().__init__(ACCIONES.ActionSetBookmarkImage)
#         self.bookmark_name = bookmark_name
#         self.image_id = image_id
#         self.width = width
#         self.height = height
    
#     def set_bookmark_name(self, bookmark_name):
#         self.bookmark_name = bookmark_name
    
#     def set_image_id(self, image_id):
#         self.image_id = image_id
        
#     def set_width(self, width: float):
#         self.width = width
    
#     def set_height(self, height: float):
#         self.height = height
    
#     def __str__(self):
#         return f"SetBookmarkImage('{self.bookmark_name}' → img_id={self.image_id}, {self.width}x{self.height})"

# class Image:
#     def __init__(self, id, md5, path):
#         self.id = id
#         self.md5 = md5
#         self.path = path
    
#     def __str__(self):
#         path_type = "FILE" if self.path.startswith("FILE://") else "BASE64"
#         return f"Image(id={self.id}, path={self.path}, type={path_type}, md5={self.md5[:8]}...)"
    
#     def __repr__(self):
#         return self.__str__()

# # class Value:
# #     def __init__(self, id, content):
# #         self.id = id
# #         self.content = content
    
# #     def __str__(self):base64_encode_file
# #         return f"Value(id={self.id}, content='{self.content}')"
    
# #     def __repr__(self):
# #         return self.__str__()

# class XMLUpdateDocx :
    
#     def __init__(self, data: bytes) :
#         self.xml = None
#         self.data_in = None
#         self.data_out = None
#         self.actions = []
#         self.images = []
    
#     def _convert_data_to_bytes (self, data: bytes) :
#         self.xml = data.decode("utf-8")
    
#     def _process_data_in (self) :
#         dataIn = etree.fromstring(self.xml).find("dataIn")
#         if dataIn[:len("FILE://")] == "FILE://" :
#             file_path = dataIn[len("FILE://"):]
#             if os.path.exists(file_path) == False :
#                 return False
#             with open(file_path, 'rb') as file:
#               file_bytes = file.read()
#             self.data_in.file_bytes


# class Data :

#     def __init__(self, data: bytes):
        
#         self.file_in = None
#         self.file_out = None    # Puede ser FILE://mi_fichero.docx o BASE64
#         self.datastorage_dir = "datastorage"
#         self.doc : Document = None
#         self.file_in_data = None
#         self.file_in_format = None
#         self.actions : list = []
#         self.images : list = []
#         self.temp_file = None
        
#         """Creamos directorio data_storage si no existe"""
#         data_storage.ensure_datastorage_dir(self.datastorage_dir)
        
#         """Procesamos fileIn en {xml_action}"""
#         file_in_node = etree.fromstring(data).find("fileIn")
#         file_in_node_content = file_in_node.text
#         file_in_node_md5 = file_in_node.get("md5", None)
#         file_in_node_md5 = data_storage.save_to_datastorage(self.datastorage_dir, file_in_node_content, file_in_node_md5)
        
#         """Procesamos las imágenes"""
#         # images_nodes = etree.fromstring(data).find("image")
#         # for image in images_nodes :
#         #     print (image)
        
#         """Transformamos XML para convertir FILE:// en BASE64:// y comprobamos MD5"""
#         # xml_action_file_transformed = self._transform_xml(xml_action_file)
#         # print (xml_action_file_transformed)
        
#         """Procesamos XML previamente transformado"""
#         # success = self.load_xml(xml_action_file)
#         # self.load_document()
    
#     # 
#     def _procesar_file_element(self, element) -> str:
#         """Si el elemento (nodo) tiene contenido. Guardamos en data_storage y devolvemos su MD5"""
        
#         """Si el elemento (nodo) no tiene contenido, devolvemos la propiedad MD5"""
        
        
#         """Procesamos un {Eif content[:len("FILE://")] == "FILE://" :
#             file_path = content[len("FILE://"):]
#             if os.path.exists(file_path) == False :
#                 return False
#             with open(file_path, 'rb') as file:
#               file_bytes = file.read()
#             md5 = utils.md5_bytes(file_bytes)
#             data_storage.save_to_datastorage(self.data_storage_dir, element.text)
#             self.data_storage._save_to_datastorage(md5, file_bytes)
#             return md5lement} que hacer referencia a un fichero {FILE://}, {BASE64://}, {URL://}"""
#         content = element.text
#         file_bytes = None
#         """Si el content es FILE:/// guardamos en data_storage el fichero con su MD5 (se calcula)"""
#         """Retornamos el MD5 del fichero almacenado en data_storage                              """
        
    
    
#     def _transform_xml(self, xml_action_file : str) -> str :
        
#         """Si los nodos tienen un content"""
#         """ - Si el content es FILE:// convertimos el content a BASE64:/// y calculamos MD5"""
#         """ - Si el content es BASE64:// guardamos físicamente en DataStorage y calculamos MD5"""
#         """Si el nodo fileIn no tiene content"""
#         """ - Si tiene la propiedad MD5 comprobamos en dataStorage. Si falla comprobacion dataStorage devolvemos error"""
#         """ - Si no tiene propiedad MD5 devolvemos error"""
        
#         with open(xml_action_file, 'r', encoding='utf-8') as file:
#             action_xml_str = file.read()
            
#             def file_to_base64(match):
#                 """Convierte un match de FILE:// a BASE64://"""
#                 file_path = match.group(1)
#                 with open(file_path, 'rb') as f:
#                     file_data = f.read()
#                 base64_data = base64.b64encode(file_data).decode('utf-8')
#                 return f"BASE64://{base64_data}"
#                 return match.group(0)  # Retorna el original si hay error
    
#             # Patrón para encontrar FILE://ruta_archivo dentro de nodos XML
#             pattern = r'FILE://([^<>\s]+)'
            
#             # Reemplazar todas las ocurrencias
#             transformed_xml = re.sub(pattern, file_to_base64, action_xml_str)
            
#             return transformed_xml
            
#             #self.xml_action_file = utils.transform_xml_action(action_xml_str) 
            
    
#     def load_document(self):
        
#         """Carga el documento desde los datos de entrada y lo almacena en self.doc"""
#         if self.file_in_data is None or self.file_in_format is None:
#             logger.error("No hay datos de entrada para cargar el documento")
#             return False
            
#         # Crear archivo temporal con el documento
#         self.temp_file = utils.createSourceData(self)
#         if self.temp_file is None:
#             logger.error("Error creando archivo temporal para el documento")
#             return False
            
#         # Cargar documento con python-docx
#         try:
#             self.doc = Document(self.temp_file.name)
#             logger.info(f"Documento cargado correctamente: {self.temp_file.name}")
#             return True
#         except Exception as e:
#             logger.error(f"Error cargando documento: {e}")
#             return False
    
#     def save_document(self, output_path=None):
#         """Guarda el documento. Si no se especifica ruta, guarda en el archivo temporal"""
#         if self.doc is None:
#             logger.error("No hay documento cargado para guardar")
#             return False
            
#         try:
#             save_path = output_path if output_path else self.temp_file.name
#             self.doc.save(save_path)
#             logger.info(f"Documento guardado en: {save_path}")
#             return True
#         except Exception as e:
#             logger.error(f"Error guardando documento: {e}")
#             return False

#     def load_config(self, xml) :
#         if xml.startswith("XML://"):
#             return self.load_xml(xml[6:])
#         elif xml.startswith("FILE://"):
#             return self.load_xml(xml[7:])
#         else:
#             return self.load_xml(xml)

#     def load_xml(self, xml_string: str) -> bool:
#         try:
#             root = etree.fromstring(xml_string.encode("utf-8"))
#             return self._parse_xml(root)
#         except etree.XMLSyntaxError as e:
#             print(f"Error parsing XML: {e}")
#             return False
    
#     def _parse_xml(self, root) -> bool:
        
#         if root.tag != "ineoDoc":
#             print("El fichero de configuración debe tener como nodo root ineoDoc")
#             return False
        
#         # Parse images
#         images_node = root.find("images")
#         if images_node is not None:
#             for image_node in images_node.findall("image"):
#                 image_id = image_node.get("id")
#                 md5 = image_node.get("md5")
#                 path = image_node.text
#                 self.images.append(Image(image_id, md5, path))
        
#         # Parseamos y procesamos fileIn, almacenamos en dataStorage
#         file_in_node = root.find("fileIn")
#         if file_in_node is not None:
#             success, format, source = utils.format_source(file_in_node.text)
#             print (f"format : {format}")
#             print (f"source : {source[:10]}")
#             if (success == True) :
#                 self.file_in_data = source
#                 self.file_in_format = format
        
#         # Parse actions
#         actions_node = root.find("actions")
#         if actions_node is not None:
#             for action_node in actions_node.findall("action"):
#                 self._parse_action(action_node)
        
#         return True
    
#     def _parse_action(self, action_node):
#         action_name = action_node.get("name")
        
        
#         if action_name  == "replaceTextWithText" :
#             labels_node = action_node.find("labels")
#             if labels_node is not None:
#                 for label_node in labels_node.findall("label"):
#                     text = label_node.get("text")
#                     value = label_node.text
#                     action = ActionReplaceTextWithText(text, value)
#                     self.actions.append(action)
#         elif action_name  == "replaceTextWithImage" :
#             labels_node = action_node.find("labels")
#             if labels_node is not None:
#                 for label_node in labels_node.findall("label"):
#                     text = label_node.get("text")
                    
#                     # Extraer image_id del elemento hijo
#                     image_id_node = label_node.find("imgId")
#                     image_id = image_id_node.text if image_id_node is not None else None
                    
#                     # Extraer width del elemento hijo
#                     width_node = label_node.find("width")
#                     width = float(width_node.text) if width_node is not None and width_node.text else None
                    
#                     # Extraer height del elemento hijo
#                     height_node = label_node.find("height")
#                     height = float(height_node.text) if height_node is not None and height_node.text else None
                    
#                     action = ActionReplaceTextWithImage(text, image_id, width, height)
#                     self.actions.append(action)
#         elif action_name ==  "setBookmarkFormCheckbox" :
#             bookmarks_node = action_node.find("bookmarks")
#             if bookmarks_node is not None:
#                 for bookmark_node in bookmarks_node.findall("bookmark"):
#                     bookmark_name = bookmark_node.get("name")
#                     value = bookmark_node.text
#                     action = ActionSetBookmarkFormCheckbox(bookmark_name, value)
#                     self.actions.append(action)
#         elif action_name == "setBookmarkImage":
#             bookmarks_node = action_node.find("bookmarks")
#             if bookmarks_node is not None:
#                 for bookmark_node in bookmarks_node.findall("bookmark"):
#                     bookmark_name = bookmark_node.get("name")
                    
#                     # Extraer image_id del elemento hijo
#                     image_id_node = bookmark_node.find("imgId")
#                     image_id = image_id_node.text if image_id_node is not None else None
                    
#                     # Extraer width del elemento hijo
#                     width_node = bookmark_node.find("width")
#                     width = float(width_node.text) if width_node is not None and width_node.text else None
                    
#                     # Extraer height del elemento hijo
#                     height_node = bookmark_node.find("height")
#                     height = float(height_node.text) if height_node is not None and height_node.text else None
                    
#                     action = ActionSetBookmarkImage(bookmark_name, image_id, width, height)
#                     self.actions.append(action)
                    
        
#         # # Handle legacy structure with items (for backward compatibility)
#         # else:
#         #     items_node = action_node.find("items")
#         #     if items_node is None:
#         #         return
                
#         #     for item_node in items_node.findall("item"):
#         #         if action_name == "replaceTextWithText":
#         #             search_value_node = item_node.find("searchValue")
#         #             search_value = search_value_node.text if search_value_node is not None else None
                    
#         #             value_node = item_node.find("value")
#         #             value_id = value_node.get("id") if value_node is not None else None
                    
#         #             action = ActionReplaceTextWithText(search_value, value_id)
#         #             self.actions.append(action)
                    
#         #         elif action_name == "replaceTextWithImage":
#         #             search_value_node = item_node.find("searchValue")
#         #             search_value = search_value_node.text if search_value_node is not None else None
                    
#         #             img_node = item_node.find("img")
#         #             img_id = img_node.get("id") if img_node is not None else None
                    
#         #             width_node = item_node.find("width")
#         #             width = float(width_node.text) if width_node is not None and width_node.text else None
                    
#         #             height_node = item_node.find("height")
#         #             height = float(height_node.text) if height_node is not None and height_node.text else None
                    
#         #             action = ActionReplaceTextWithImage(search_value, img_id, width, height)
#         #             self.actions.append(action)
                    
#         #         elif action_name == "setFormCheckbox":
#         #             search_value_node = item_node.find("searchValue")
#         #             search_value = search_value_node.text if search_value_node is not None else None
                    
#         #             value_node = item_node.find("value")
#         #             value_id = value_node.get("id") if value_node is not None else None
                    
#         #             action = ActionSetFormCheckbox(search_value, value_id)
#         #             self.actions.append(action)
    
#     def getImage(self, id):
#         return self.images.get(id)
    
#     def getValue(self, id):
#         return self.values.get(id)
    
#     def getValueContent(self, id):
#         value = self.values.get(id)
#         return value.content if value else None
    
#     # Método alternativo usando XPath para parsing más eficiente
#     # def _parseXML_xpath(self, root) -> bool:
#     #     """Versión alternativa usando XPath - más eficiente para XMLs grandes"""
#     #     if root.tag != "ineoDoc":
#     #         print("El fichero de configuración debe tener como nodo root ineoDoc")
#     #         return False
        
#     #     # Parse images usando XPath
#     #     for img in root.xpath("//images/image"):
#     #         id = img.get("id")
#     #         md5 = img.get("md5")
#     #         path = img.text
#     #         self.images[id] = Image(id, md5, path)
        
#     #     # Parse values usando XPath
#     #     for val in root.xpath("//values/value"):
#     #         id = val.get("id")
#     #         content = val.text
#     #         self.values[id] = Value(id, content)
        
#     #     # Parse fileIn y fileOut
#     #     file_in = root.xpath("//fileIn/text()")
#     #     self.fileIn = file_in[0] if file_in else None
        
#     #     file_out = root.xpath("//fileOut/text()")
#     #     self.fileOut = file_out[0] if file_out else None
        
#     #     # Parse actions
#     #     for action in root.xpath("//actions/action"):
#     #         action_name = action.get("name")
#     #         for item in action.xpath("items/item"):
#     #             if action_name == "replaceTextWithText":
#     #                 search_value = item.xpath("searchValue/text()")
#     #                 search_value = search_value[0] if search_value else None
#     #                 value_id = item.xpath("value/@id")
#     #                 value_id = value_id[0] if value_id else None
#     #                 self.actions.append(ActionReplaceTextWithText(search_value, value_id))
                    
#     #             elif action_name == "replaceTextWithImage":
#     #                 search_value = item.xpath("searchValue/text()")
#     #                 search_value = search_value[0] if search_value else None
#     #                 img_id = item.xpath("img/@id")
#     #                 img_id = img_id[0] if img_id else None
#     #                 width = item.xpath("width/text()")
#     #                 width = float(width[0]) if width and width[0] else None
#     #                 height = item.xpath("height/text()")
#     #                 height = float(height[0]) if height and height[0] else None
#     #                 self.actions.append(ActionReplaceTextWithImage(search_value, img_id, width, height))
                    
#     #             elif action_name == "setFormCheckbox":
#     #                 search_value = item.xpath("searchValue/text()")
#     #                 search_value = search_value[0] if search_value else None
#     #                 value_id = item.xpath("value/@id")
#     #                 value_id = value_id[0] if value_id else None
#     #                 self.actions.append(ActionSetBookmarkFormCheckbox(search_value, value_id))
        
#     #     return True

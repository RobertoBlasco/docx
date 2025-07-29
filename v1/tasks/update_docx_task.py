import os
import logging
import enum
import time
import lxml
import lxml.etree
import io
from docx import Document

import utils
import actions.action_replace_text_with_text as action_replace_text_with_text
import actions.action_replace_text_with_image as action_replacet_text_with_image
import actions.action_set_form_checkbox as action_set_form_checkbox

logger = logging.getLogger("IneoDocx")

class EnumActions(enum.Enum):
    REPLACE_TEXT_WITH_TEXT = "replaceTextWithText"
    REPLACE_TEXT_WITH_IMAGE = "replaceTextWithImage"
    SET_FORM_CHECKBOX = "setFormCheckbox"
    SET_FORM_TEXT = "setFormText"
    SET_BOOKMARK_IMAGE = "setBookmarkImage"

class UpdateDocxTask:
    
    def __init__(self, xml):
        
        self.xml = xml
        self.document = None
        self.data_out = None
        self.actions = []
        self.images = []
        
        self._validate_xml()
        self._process_data_in()
        self._process_data_out()
        self._process_actions()
        self._validate_actions()
        self._execute_actions()
    
    def _set_data_out(self, data_out: str) :
        if data_out is None or len(data_out.strip()) <= 0 :
            self.data_out = "BASE64"
        elif data_out[:len("FILE://")] == "FILE://" :
            self.data_out = data_out[len("FILE://"):]
        else :
            self.data_out = data_out
    
    def _validate_actions(self) :
        pass
        
    def _validate_xml(self) -> bool:
        return True
    
    def _execute_actions(self) :
        if self.actions and len(self.actions) > 0 :
            logger.info("# Ejecución de acciones")
            for action in self.actions :
                if action.name == EnumActions.REPLACE_TEXT_WITH_TEXT.value :
                    num_seconds = action_replace_text_with_text.replace_text_with_text(self.document, action)
                    logger.info(f"Ejecutada accion {action.name} en {num_seconds} segundos.")
                elif action.name == EnumActions.SET_FORM_CHECKBOX.value :
                    num_seconds = action_set_form_checkbox.set_form_checkbox(self.document, action)
                    logger.info(f"Ejecutada accion {action.name} en {num_seconds} segundos.")
                elif action.name == EnumActions.REPLACE_TEXT_WITH_IMAGE.value :
                    num_seconds = action_replacet_text_with_image.replace_text_with_image(self.document, action)
                    logger.info(f"Ejecutada accion {action.name} en {num_seconds} segundos.")
                
            if (self.data_out == "BASE64") :
                # Deberíamos guardarlo en un fichero temporal para su conversión a base64
                pass
            else :
                try :
                    self.document.save(self.data_out)
                    logger.info(f"# Documento de salida guardado en {self.data_out}")
                except Exception as e :
                    logger.info(f"{e}")
                    
                
                    
    def _process_data_in(self):
        logger.info("# Procesando fichero de entrada")
        dataIn = self.xml.find("dataIn")
        if dataIn is not None and dataIn.text is not None:
            if dataIn.text.startswith("FILE://"):
                file_path = dataIn.text[len("FILE://"):]
                if not os.path.exists(file_path):
                    logger.error(f"{file_path} no existe.")
                    return False
                logger.info(f"FileIn : \"{file_path}\"")
                with open(file_path, 'rb') as file:
                    file_bytes = file.read()
                    docx_props = utils.get_docx_properties(file_bytes)
                    if docx_props is not None :
                        logger.info(f"Autor documento : {docx_props.author}")
                        logger.info(f"Fecha modificación documento : {docx_props.modified}")
                        self.document = Document(io.BytesIO(file_bytes))
        
    def _process_data_out(self):
        logger.info("# Procesando fichero de salida")
        node_dataout = self.xml.find("dataOut")
        if node_dataout is not None :
            self._set_data_out(node_dataout.text)
        logger.info(f"DataOut : {self.data_out}")
            
    def _process_actions(self):
        logger.info("# Procesando Acciones")
        actions = self.xml.find("actions")
        if actions is not None:
            for action in actions:
                action_name = action.get("name")
                if action_name == EnumActions.REPLACE_TEXT_WITH_IMAGE.value:
                    items = action.findall("item")
                    if (items is not None and len(items) > 0) :
                        for item in items :
                            if item.text :
                                action_obj = ActionReplaceTextWithImage(item)
                                if action_obj is not None :
                                    self.actions.append(action_obj)
                                    logger.info(action_obj)
                elif action_name == EnumActions.REPLACE_TEXT_WITH_TEXT.value:
                    items = action.findall("item")
                    if items is not None and len(items) > 0 :
                        for item in items :
                            action_obj = ActionReplaceTextWithText(item)
                            if action_obj is not None :
                                self.actions.append(action_obj)
                                logger.info(action_obj)
                elif action_name == EnumActions.SET_FORM_CHECKBOX.value:
                    forms = action.findall("form")
                    if forms is not None :
                        for form in forms :
                            if form.get("name", None) is not None :
                                action_obj = SetFormCheckBox(form)
                                if action_obj is not None :
                                    self.actions.append(action_obj)
                                    logger.info(action_obj)
                # elif action_name == EnumActions.SET_BOOKMARK_IMAGE.value:
                #     forms = action.findall("bookmark")
                #     if forms is not None :
                #         for form in forms :
                #             if form.get("name", None) is not None :
                #                 action_obj = SetBookmarkImage(form)
                #                 if action_obj is not None :
                #                     self.actions.append(action_obj)
                #                     logger.info(action_obj)
                elif action_name == EnumActions.SET_FORM_TEXT.value:
                    forms = action.findall("form")
                    if forms is not None :
                        for form in forms :
                            if form.get("name", None) is not None :
                                action_obj = SetFormText(form)
                                if action_obj is not None :
                                    self.actions.append(action_obj)
                                    logger.info(action_obj)
        else :
            logger.error("No se han encontrado acciones")

class Action:
    def __init__(self, name):
        self.name = name
    
    def __str__(self) :
        return self.name

class ActionReplaceTextWithText(Action):
    def __init__(self, action_node):
        super().__init__(EnumActions.REPLACE_TEXT_WITH_TEXT.value)
        self.search_text = None
        self.replace_text = None
        self._parse_labels(action_node)
    
    def _parse_labels(self, action_node):
        self.search_text = action_node.get("searchText", None)
        self.replace_text = action_node.text if action_node.text is not None and len(action_node.text) > 0 else None
                
    def __str__(self):
        return f"{super().__str__()} : SearchText=\"{self.search_text}\", ReplaceText=\"{self.replace_text}\""

class ActionReplaceTextWithImage(Action):
    def __init__(self, action_node):
        super().__init__(EnumActions.REPLACE_TEXT_WITH_IMAGE.value)
        self.search_text = None
        self.img_id = None
        self.width = 0
        self.height = 0
        self._parse_labels(action_node)
    
    def _parse_labels(self, action_node):
        self.search_text = action_node.get("searchText", None)
        img_id_node = action_node.find("imgId")
        if img_id_node is not None :
            self.img_id = img_id_node.text
        width_node = action_node.find("width")
        if width_node is not None :
            self.width = utils.safe_int(width_node.text)
        height_node = action_node.find("height")
        if height_node is not None :
            self.height = utils.safe_int(height_node.text)
    
    def __str__(self):
        return f"{super().__str__()} : searchText=\"{self.search_text}\", imgId={self.img_id}, width={self.width}, height={self.height}"

class SetFormCheckBox(Action):
    def __init__(self, action_node):
        super().__init__(EnumActions.SET_FORM_CHECKBOX.value)
        self.form_name = None
        self.checkbox_value = False
        self._parse_forms(action_node)
    
    def _parse_forms(self, action_node):
        self.form_name = action_node.get("name")
        self.checkbox_value = True if action_node.text and action_node.text == "1" else False
        
    def __str__(self):
        return f"{super().__str__()} : formName=\"{self.form_name}\", checkboxValue=\"{self.checkbox_value}\""

class SetBookmarkImage(Action):
    def __init__(self, action_node):
        super().__init__(EnumActions.SET_BOOKMARK_IMAGE.value)
        self.bookmark_name = None
        self.img_id = 0
        self.width = 0
        self.height = 0
        self._parse_bookmarks(action_node)
    
    def _parse_bookmarks(self, action_node):
        self.bookmark_name = action_node.get("name")    # Ya controlamos que exista el atributo name en UpdateDocxTask
        img_id_node = action_node.find("imgId")
        if img_id_node is not None:
            self.img_id = utils.safe_int(img_id_node.text)
        width_node = action_node.find("width")
        if width_node is not None:
            self.width = utils.safe_int(width_node.text)
        height_node = action_node.find("height")
        if height_node is not None:
            self.height = utils.safe_int(height_node.text)
    
    def __str__(self):
        return f"{super().__str__()} : imgId={self.img_id}, width={self.width}, height={self.height}"  
            
class SetFormText(Action):
    def __init__(self, action_node):
        super().__init__(EnumActions.SET_FORM_TEXT.value)
        self.form_name = None
        self.text_value = None
        self._parse_forms(action_node)
    
    def _parse_forms(self, action_node):
        self.form_name = action_node.get("name", None)
        self.text_value = action_node.text
    
    def __str__(self):
        return f"{super().__str__()} : formName=\"{self.form_name}\", textValue=\"{self.text_value}\"" 


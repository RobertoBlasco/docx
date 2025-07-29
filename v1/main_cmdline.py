# Librerías python
import time
import logging
from enum import StrEnum
import sys
from lxml import etree

# Clases
import tasks.update_docx_task as update_docx_task

# Log eventos de la aplicación
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("./log.log", mode='w'),
        logging.StreamHandler()  # Para mostrar en consola
    ]
)
logger = logging.getLogger("IneoDocx")                       

def main() :
    
    ###################################################
    # Timestamp de inicio
    ###################################################
    start_time = time.time()
    
    xml_action_file = "update_docx_task.xml"
    if len(sys.argv) > 1:
        xml_action_file = sys.argv[1]
        
    root = etree.parse(xml_action_file).getroot()
    task = root.get("task")
    match task:
        case "updateDocx" :
            logger.info("Iniciada tarea updateDocx")
            task = update_docx_task.UpdateDocxTask(root)
        case _ :
            logger.error("No se ha encontrado una tarea valida.")
        
    # Timestamp de fin 
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Tiempo total de ejecución: {elapsed:.2f} segundos")
        
    # """Paso 2. Procesamos fichero XML de acciones"""
    # with open (xml_action_file, 'r', encoding="utf-8") as file :
    #data = action_docx.da


    #     """2.1 Procesamos FileIn. MD5 y data_storage"""
    #     """2.2 Procesamos las Imágenes. MD5 y data_storage"""
    #     """2.3 Procesamos las Acciones"""
    #     data = docx.Data(file.read())
    
    
    
    ###################################################
    # Procesamiento unificado con python-docx
    ###################################################
    # document_modified = False
    
    # # Crear instancia de ActionSetFormCheckbox para manejar checkboxes
    # checkbox_action = ActionSetFormCheckbox(temp_file.name)
    # checkbox_action.document = doc  # Reutilizar el documento ya cargado
    
    # # Crear instancia de ActionSetBookmarkImage para manejar imágenes en marcadores
    # bookmark_image_action = ActionSetBookmarkImage(temp_file.name)
    # bookmark_image_action.document = doc  # Reutilizar el documento ya cargado
    
    # Procesar todas las acciones
    # for action in data.actions :
    #     if (action.name == docx.ACCIONES.ActionReplaceTextWithText) :
    #         rpl_text_with_text.replace_text_with_text(data.doc, action)
    #         document_modified = True
    #     elif (action.name == docx.ACCIONES.ActionSetBookmarkFormCheckbox) :
    #         bookmark = action.bookmark
    #         value = action.value
    #         if (bookmark is not None and value is not None) :
    #             checkbox_value = True if value == "1" else False
    #             success = set_form_checkbox.set_checkbox_value(bookmark, checkbox_value)
    #             if success:
    #                 document_modified = True
    #     elif (action.name == docx.ACCIONES.ActionReplaceTextWithImage) :
    #         rpl_text_with_img.replace_text_with_image(data.doc, action, data)
    #         document_modified = True
    #     elif (action.name == docx.ACCIONES.ActionSetBookmarkImage) :
    #         bookmark_name = action.bookmark_name
    #         image_id = action.image_id
    #         width = action.width
    #         height = action.height
            
    #         if (bookmark_name is not None and image_id is not None) :
    #             # Buscar la imagen en data.images
    #             image_data = None
    #             for img in data.images:
    #                 if img.id == image_id:
    #                     # Obtener datos de la imagen
    #                     image_data = data_storage.get_image_data(img.path)
    #                     break
                
    #             if image_data is not None:
    #                 # Establecer dimensiones por defecto si no se especificaron
    #                 width = width if width is not None else 100
    #                 height = height if height is not None else 50
                    
    #                 success = set_bookmark_image.set_image_at_bookmark(
    #                     data.doc,
    #                     bookmark_name, 
    #                     image_data, 
    #                     int(width), 
    #                     int(height)
    #                 )
    #                 if success:
    #                     document_modified = True
    #                     logger.info(f"Imagen establecida en marcador {bookmark_name}")
    #                 else:
    #                     logger.warning(f"No se pudo establecer imagen en marcador {bookmark_name}")
    #             else:
    #                 logger.warning(f"No se encontró imagen con ID {image_id}")
    #         else:
    #             logger.warning(f"Acción ActionSetBookmarkImage incompleta: bookmark_name={bookmark_name}, image_id={image_id}")
    
    # # Guardar documento si se realizaron modificaciones
    # if document_modified:
    #     data.save_document()
    # else:
    #     logger.info("No se realizaron modificaciones en el documento")
        
    
    # # fileOut eliminado - el sistema devuelve el documento procesado
    # logger.info(f"Documento procesado correctamente: {data.temp_file.name}")
    
    # # Convertir documento procesado a base64 y devolver como XML
    # processed_doc_base64 = response.convert_file_to_base64(data.temp_file.name)
    # if processed_doc_base64:
    #     response_xml = response.create_response_xml(processed_doc_base64)
    #     print (data.temp_file.name)
    #     #print(response_xml)
    # else:
    #     error_xml = response.create_error_response_xml("Error al procesar el documento")
    #     print(error_xml)
    
    # # Timestamp de fin 
    # end_time = time.time()
    # elapsed = end_time - start_time
    # print(f"Tiempo total de ejecución: {elapsed:.2f} segundos")



if __name__ == "__main__" :
    main()
    
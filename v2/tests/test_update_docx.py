#!/usr/bin/env python3
"""
Test para la clase UpdateDocx - Orquestador principal
"""

import sys
import os
import logging


# Log eventos de la aplicación
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("D:/dev/ineodocx/ejemplos/ineoDocx.log", mode='w')
        # StreamHandler removido - solo archivo de log
    ]
)
logger = logging.getLogger("IneoDocx")


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.update_docx import UpdateDocx

def read_task_xml():
    """
    Lee el XML y muestra las acciones configuradas
    
    Returns:
        UpdateDocx: Objeto orquestador creado
    """
    # Ruta al XML de configuración
    xml_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tasks', 'update_docx_task.xml')
    
    if not os.path.exists(xml_file):
        logger.error(f"Error: No se encontró el archivo XML en {xml_file}")
        return None
    
    logger.info(f"Leyendo configuración XML desde {xml_file}")
    
    try:
        # Crear orquestador (esto carga y parsea el XML)
        updater = UpdateDocx(xml_file)
        
        logger.info("Imágenes configuradas:")
        for img in updater.task_data.images:
            logger.info(f"\tID {img.id}: {img.path}")
        
        logger.info(f"Acciones configuradas ({len(updater.task_data.actions)}):")
        for i, action in enumerate(updater.task_data.actions, 1):
            logger.info(f"{action.name} (ID generado: {action.id})")
            logger.info(f"{action.name}[{action.id}] Items: {len(action.items)}")
            
            # Mostrar detalles según el tipo
            for j, item in enumerate(action.items, 1):
                if action.name == 'replaceTextWithText':
                    logger.info(f"{action.name}[{action.id}] '{item.search_text}' -> '{item.replacement_text}'")
                elif action.name == 'replaceTextWithImage':
                    logger.info(f"{action.name}[{action.id}] IMG:{item.img_id} ({item.width}x{item.height})")
                elif action.name == 'setFieldCheckbox':
                    logger.info(f"{action.name}[{action.id}] Checkbox '{item.name}' = {item.value}")
                elif action.name == 'setFieldText':
                    logger.info(f"{action.name}[{action.id}] TextField '{item.tag}' = '{item.value}'")
                # elif action.name == 'setBookmarkImage':
                #     print(f"         {j}. Bookmark '{item.name}' → IMG:{item.img_id} ({item.width}x{item.height})")
        
        logger.info("XML leído correctamente")
        logger.info(f"Total: {len(updater.task_data.actions)} acciones configuradas")
        
        return updater
        
    except Exception as e:
        logger.error(f"Error leyendo XML: {e}")
        import traceback
        traceback.print_exc()
        return None

def update_task_xml(updater):
    """
    Ejecuta las acciones configuradas en el documento
    
    Args:
        updater: Objeto UpdateDocx con las acciones configuradas
    """
    if updater is None:
        logger.error("No se pudo crear el orquestador. Verifica el XML.")
        return
    
    logger.info("Iniciando ejecución de acciones en documento...")
    
    try:
        xml_response = updater.process_document()
        
        # Solo mostrar la respuesta XML sin información adicional
        print(xml_response)
                
    except Exception as e:
        print(f"Error ejecutando acciones: {e}")
        import traceback
        traceback.print_exc()

def main():
    """
    Función principal: lee XML y ejecuta acciones
    """
    logger.info("Iniciando test completo de UpdateDocx...")
    
    # 1. Leer y analizar XML
    updater = read_task_xml()
    
    # 2. Ejecutar acciones en documento
    if updater:
        update_task_xml(updater)

if __name__ == "__main__":
    main()
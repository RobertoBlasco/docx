import base64
import logging
from datetime import datetime

logger = logging.getLogger("IneoDocx")

def convert_file_to_base64(file_path: str) -> str:
    """
    Convierte un archivo a base64
    
    Args:
        file_path: Ruta del archivo a convertir
        
    Returns:
        str: Contenido del archivo en base64
    """
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
            base64_content = base64.b64encode(file_content).decode('utf-8')
            logger.info(f"Archivo convertido a base64: {file_path}")
            return base64_content
    except Exception as e:
        logger.error(f"Error al convertir archivo a base64: {e}")
        return None

def create_response_xml(document_base64: str) -> str:
    """
    Crea el XML de respuesta con el documento procesado
    
    Args:
        document_base64: Documento procesado en formato base64
        
    Returns:
        str: XML de respuesta
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<ineoDocResponse>
    <timestamp>{timestamp}</timestamp>
    <status>success</status>
    <processedDocument>
        <format>docx</format>
        <encoding>base64</encoding>
        <content>{document_base64}</content>
    </processedDocument>
</ineoDocResponse>"""
    
    logger.info("XML de respuesta creado correctamente")
    return response_xml

def create_error_response_xml(error_message: str) -> str:
    """
    Crea el XML de respuesta para errores
    
    Args:
        error_message: Mensaje de error
        
    Returns:
        str: XML de respuesta de error
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    error_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<ineoDocResponse>
    <timestamp>{timestamp}</timestamp>
    <status>error</status>
    <error>
        <message>{error_message}</message>
    </error>
</ineoDocResponse>"""
    
    logger.error(f"Error en procesamiento: {error_message}")
    return error_xml
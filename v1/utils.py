import base64
import tempfile
import requests
import logging
import shutil
import re
import hashlib
import io

from docx import Document

logger = logging.getLogger("IneoDocx")

class ENUM_SOURCES :
    BASE64  = "BASE64://"
    FILE    = "FILE://"
    URL     = "URL://"

def file_encode_base64(file_path:str) -> str :
    """Codifica a base64 un fichero dada su ruta"""
    with open(file_path, 'rb') as f:
        file_data = f.read()
        base64_data = base64.b64encode(file_data).decode('utf-8')
        return base64_data
    
"""Codifica a base64 una secuencia de bytes y lo devuelve en formato hexadecimal"""
def md5_bytes(data) -> str:
    md5_hash = hashlib.md5(data).hexdigest()
    return md5_hash

"""Codifica a base64 un fichero (filepath) y lo devuelve en formato hexadecimal"""
def md5_file(file_path) -> str:
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

"""Codifica a base64 una cadena de texto y lo devuelve en formato hexadecimal"""
def md5_str(text:str) -> str:
    text_bytes = text.encode('utf-8')
    md5_hash = hashlib.md5(text_bytes).hexdigest()
    return md5_hash

def format_source(source: str) -> list :
    
    _format = ""
    _source = ""
    if source.startswith(ENUM_SOURCES.BASE64):
        _format = source[:len(ENUM_SOURCES.BASE64)]
        _source = source[len(ENUM_SOURCES.BASE64):]
    elif source.startswith(ENUM_SOURCES.FILE):
        _format = source[:len(ENUM_SOURCES.FILE)]
        _source = source[len(ENUM_SOURCES.FILE):]
    elif source.startswith(ENUM_SOURCES.URL):
        _format = source[:len(ENUM_SOURCES.URL)]
        _source = source[len(ENUM_SOURCES.URL):]
    else :
        return False, None, None
    
    return True, _format, _source


def createSourceData (actionData)-> tempfile :
    
    logging.info("=== CREACIÓN DEL FICHERO PARA COPIA DE TRABAJO ===")
    source = actionData.file_in_data
    format = actionData.file_in_format
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    if format == ENUM_SOURCES.BASE64 :
        decoded = base64.b64decode(source)
        temp.write(decoded)
        temp.close()
    elif format == ENUM_SOURCES.FILE :
        shutil.copy2(source, temp.name)
    elif format == ENUM_SOURCES.URL :
        resp = requests.get(source)
        resp.raise_for_status()
        temp.write(resp.content)
        temp.close()
    logging.info(f"Fichero {temp.name} creado como copia de trabajo.")
    logging.info("=== FINALIZADA CREACIÓN DEL FICHERO PARA COPIA DE TRABAJO ===")
    return temp

def getTempFilePath(fileSuffix: str) -> str :
    
    tempPath = None
    with tempfile.NamedTemporaryFile(delete=False, suffix=fileSuffix) as temp :
        tempPath = temp.name
    return tempPath
        
def transform_xml_action(xml_content: str) -> str:
    """
    Transforma un XML de acción convirtiendo todos los nodos FILE:// a BASE64://
    
    Args:
        xml_content (str): Contenido XML completo
        
    Returns:
        str: XML transformado con FILE:// convertidos a BASE64://
    """
    
    def file_to_base64(match):
        """Convierte un match de FILE:// a BASE64://"""
        file_path = match.group(1)
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
            base64_data = base64.b64encode(file_data).decode('utf-8')
            logger.info(f"Archivo convertido a BASE64: {file_path}")
            return f"BASE64://{base64_data}"
        except Exception as e:
            logger.error(f"Error convirtiendo archivo {file_path} a BASE64: {e}")
            return match.group(0)  # Retorna el original si hay error
    
    # Patrón para encontrar FILE://ruta_archivo dentro de nodos XML
    pattern = r'FILE://([^<>\s]+)'
    
    # Reemplazar todas las ocurrencias
    transformed_xml = re.sub(pattern, file_to_base64, xml_content)
    
    return transformed_xml

def safe_int(value, default=0) :
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
    
def get_docx_properties(file_bytes):
      try:
          doc_stream = io.BytesIO(file_bytes)
          doc = Document(doc_stream)
          return doc.core_properties
      except:
          return None
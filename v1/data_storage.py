import os
import logging
import shutil
import base64
import requests
import hashlib
import time
import lxml

import utils as utils

# Usar logger centralizado

def ensure_datastorage_dir(data_storage: str):
    """
    Crea el directorio dataStorage si no existe.
    Returns: True si el directorio existe o se creó correctamente, False en caso de error
    """
    if data_storage is None :
        data_storage = "data_storage"
    
    try:
        if not os.path.exists(data_storage):
            os.makedirs(data_storage)
            logging.info(f"Directorio {data_storage} creado correctamente")
        else:
            logging.debug(f"Directorio {data_storage} ya existe")
        return True
    except Exception as e:
        logging.error(f"Error creando directorio {data_storage}: {e}")
        return False

def save_to_datastorage(datastorage_dir: str, element: lxml.etree._Element, md5: str) -> str:
    """
    Guarda contenido en dataStorage usando el MD5 como nombre de archivo.
    
    Args:
        content (str): Contenido con formato FILE://, BASE64://, URL://
        md5 (str): Hash MD5 que será el nombre del archivo
    
    Returns:
        str: Retorna el MD5 del fichero que ha sido guardado
    """
    if not isinstance(element, lxml.etree._Element):
        logging.info(f"Se esperaba un Element de lxml, se recibió {type(element)}")
        return None
    if not ensure_datastorage_dir():
        logging.info(f"No existe o no se ha podido crear el directorio para datastorage : {datastorage_dir}")
        return False
    
    target_path = os.path.join(datastorage_dir, md5)
    md5_hex = element.get("md5", None)
    node_content = element.text
    try:
        if node_content is not None :
            if node_content.startswith("FILE://"):
                # Copiar archivo local
                source_path = node_content[7:]  # Remover FILE://
                if not os.path.exists(source_path):
                    logging.error(f"Archivo fuente no existe: {source_path}")
                    return False
                md5_hex = utils.md5_file(source_path)
                shutil.copy2(source_path, target_path)
                logging.info(f"Archivo copiado de {source_path} a {target_path}, MD5 : {md5_hex}")
                return md5_hex
            elif node_content.startswith("BASE64://"):
                # Decodificar BASE64
                base64_data = node_content[9:]  # Remover BASE64://
                try:
                    decoded_data = base64.b64decode(base64_data)
                    with open(target_path, 'wb') as f:
                        f.write(decoded_data)
                    logging.info(f"Archivo BASE64 guardado en {target_path}")
                except Exception as e:
                    logging.error(f"Error decodificando BASE64: {e}")
                    return False
            elif node_content.startswith("URL://"):
                # Descargar desde URL
                url = node_content[6:]  # Remover URL://
                try:
                    response = requests.get(url, timeout=30)
                    response.raise_for_status()
                    with open(target_path, 'wb') as f:
                        f.write(response.content)
                    logging.info(f"Archivo descargado de {url} a {target_path}")
                except Exception as e:
                    logging.error(f"Error descargando desde {url}: {e}")
                    return False
            else:
                logging.error(f"Formato de contenido no soportado: {node_content}")
                return False
        elif md5_hex is not None :
            return md5_hex
        else :
            return None
        
    except Exception as e:
        logging.error(f"Error guardando archivo en dataStorage: {e}")
        return None

def load_from_datastorage(data_storage:str, md5:str):
    """
    Carga un archivo desde dataStorage usando su MD5.
    
    Args:
        md5 (str): Hash MD5 del archivo a cargar
    
    Returns:
        str: Ruta del archivo (FILE://path) o None si no existe
    """
    target_path = os.path.join(data_storage, md5)
    
    if os.path.exists(target_path):
        logging.info(f"Archivo encontrado en dataStorage: {target_path}")
        return f"FILE://{os.path.abspath(target_path)}"
    else:
        logging.warning(f"Archivo no encontrado en dataStorage: {md5}")
        return None

def resolve_path(data_storage:str, content, md5:str):
    """
    Resuelve la ruta final de un archivo aplicando la lógica de dataStorage.
    
    Lógica:
    - Si hay contenido: volcarlo a dataStorage/MD5 y devolver esa ruta
    - Si no hay contenido: buscar en dataStorage/MD5
    - Si no existe nada: error
    
    Args:
        content (str): Contenido del nodo (puede ser None o vacío)
        md5 (str): Hash MD5 del archivo
    
    Returns:
        str: Ruta final del archivo (FILE://path)
    
    Raises:
        FileNotFoundError: Si no se puede resolver la ruta
        ValueError: Si no se proporciona MD5
    """
    if not md5:
        raise ValueError("MD5 es requerido para resolver la ruta")
    
    logging.debug(f"Resolviendo ruta para MD5: {md5}, contenido: {content}")
    
    # Si hay contenido, volcarlo a dataStorage
    if content and content.strip():
        logging.info(f"Contenido presente, volcando a dataStorage: {md5}")
        if save_to_datastorage(content, md5):
            target_path = os.path.abspath(os.path.join(data_storage, md5))
            return f"FILE://{target_path}"
        else:
            raise FileNotFoundError(f"Error volcando contenido a dataStorage para MD5: {md5}")
    
    # Si no hay contenido, buscar en dataStorage
    else:
        logging.info(f"Sin contenido, buscando en dataStorage: {md5}")
        result = load_from_datastorage(md5)
        if result:
            return result
        else:
            raise FileNotFoundError(f"Archivo no encontrado en dataStorage para MD5: {md5}")

def calculate_file_md5(file_path):
    """
    Calcula el MD5 de un archivo y mide el tiempo que tarda.
    
    Args:
        file_path (str): Ruta del archivo
        
    Returns:
        tuple: (md5_hash, elapsed_time_seconds)
    """
    start_time = time.time()
    
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        
        elapsed_time = time.time() - start_time
        md5_result = hash_md5.hexdigest().upper()
        
        logging.info(f"MD5 calculado para {file_path}: {md5_result} (tiempo: {elapsed_time:.4f}s)")
        return md5_result, elapsed_time
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        logging.error(f"Error calculando MD5 para {file_path}: {e} (tiempo: {elapsed_time:.4f}s)")
        return None, elapsed_time

def process_xml_data(data_storage:str, data):
    
    """
    Procesa todo el contenido de un XML aplicando la lógica dataStorage.
    Resuelve fileIn, fileOut e imágenes automáticamente.
    
    Args:
        data: Objeto Data con XML parseado (debe tener .images, .fileInData, etc.)
        
    Returns:
        bool: True si todo se procesó correctamente, False si hubo errores
    """
    logging.info("=== INICIANDO PROCESAMIENTO XML CON dataStorage ===")
    
    success = True
    processed_count = 0
    
    # Procesar imágenes
    if hasattr(data, 'images') and data.images:
        logging.info(f"Procesando {len(data.images)} imágenes")
        
        for image in data.images:
            try:
                logging.info(f"Procesando imagen ID:{image.id}, MD5 original:{image.md5}")
                
                # Si hay contenido, regenerar MD5 y guardar archivo
                if image.path and image.path.strip():
                    logging.info(f"Contenido presente, regenerando MD5 para imagen {image.id}")
                    
                    # Primero guardar el archivo en dataStorage
                    if save_to_datastorage(image.path, image.md5):
                        # Calcular MD5 real del archivo guardado
                        saved_file_path = os.path.join(data_storage, image.md5)
                        real_md5, calculation_time = calculate_file_md5(saved_file_path)
                        
                        if real_md5:
                            # Si el MD5 real es diferente, renombrar archivo
                            if real_md5 != image.md5:
                                new_file_path = os.path.join(data_storage, real_md5)
                                os.rename(saved_file_path, new_file_path)
                                logging.info(f"MD5 actualizado: {image.md5} → {real_md5} (tiempo cálculo: {calculation_time:.4f}s)")
                                image.md5 = real_md5
                            else:
                                logging.info(f"MD5 verificado correcto: {real_md5} (tiempo cálculo: {calculation_time:.4f}s)")
                            
                            # Actualizar ruta final
                            image.path = f"FILE://{os.path.abspath(os.path.join(data_storage, image.md5))}"
                        else:
                            logging.error(f"Error calculando MD5 real para imagen {image.id}")
                            success = False
                            continue
                    else:
                        logging.error(f"Error guardando contenido para imagen {image.id}")
                        success = False
                        continue
                else:
                    # Sin contenido, buscar en dataStorage
                    logging.info(f"Sin contenido, buscando en dataStorage para imagen {image.id}")
                    resolved_path = resolve_path(None, image.md5)
                    image.path = resolved_path
                
                processed_count += 1
                logging.info(f"Imagen {image.id} procesada correctamente")
                
            except Exception as e:
                logging.error(f"Error procesando imagen {image.id}: {e}")
                success = False
    
    # TODO: Procesar fileIn cuando se añada soporte para MD5 en fileIn
    # if hasattr(data, 'fileInData') and hasattr(data, 'fileInMd5'):
    #     try:
    #         logging.info(f"Procesando fileIn con MD5: {data.fileInMd5}")
    #         resolved_path = resolve_path(data.fileInData, data.fileInMd5)
    #         data.fileInData = resolved_path
    #         processed_count += 1
    #         logging.info("✓ FileIn procesado correctamente")
    #     except Exception as e:
    #         logging.error(f"✗ Error procesando fileIn: {e}")
    #         success = False
    
    # Resumen final
    if success:
        logging.info(f"=== PROCESAMIENTO COMPLETADO: {processed_count} elementos procesados ===")
    else:
        logging.warning(f"=== PROCESAMIENTO COMPLETADO CON ERRORES: {processed_count} elementos procesados ===")
    
    return success
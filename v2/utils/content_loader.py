"""
Utilidad simple para cargar contenido desde diferentes fuentes
Función abstracta que maneja FILE://, BASE64:// y URL:// de forma transparente
"""

import os
import base64
import requests


def load_content(source: str) -> bytes:
    """
    Carga contenido y devuelve bytes de forma transparente
    
    Args:
        source: Contenido que puede ser:
            - FILE://ruta/archivo.ext -> Carga desde archivo
            - BASE64://contenido_base64 -> Decodifica Base64
            - URL://https://ejemplo.com/archivo -> Descarga desde URL
            - ruta_directa -> Carga directamente (compatibilidad)
    
    Returns:
        bytes: Contenido en bytes
        
    Raises:
        FileNotFoundError: Si archivo no existe
        ValueError: Si Base64 es inválido
        requests.RequestException: Si falla descarga URL
        Exception: Otros errores
    """
    
    if source.startswith('FILE://'):
        # Cargar desde archivo
        file_path = source.replace('FILE://', '')
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        with open(file_path, 'rb') as f:
            return f.read()
    
    elif source.startswith('BASE64://'):
        # Decodificar Base64
        base64_content = source.replace('BASE64://', '')
        # Limpiar espacios y saltos de línea
        clean_content = base64_content.replace('\n', '').replace('\r', '').replace(' ', '')
        return base64.b64decode(clean_content)
    
    elif source.startswith('URL://'):
        # Descargar desde URL
        url = source.replace('URL://', '')
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Lanza excepción si hay error HTTP
        return response.content
    
    else:
        # Compatibilidad: ruta directa
        if not os.path.exists(source):
            raise FileNotFoundError(f"Archivo no encontrado: {source}")
        
        with open(source, 'rb') as f:
            return f.read()
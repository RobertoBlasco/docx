#!/usr/bin/env python3
"""
IneoDocx Command Line Interface
Procesador de documentos Word basado en configuración XML

Uso:
    python ineoDocxCmdLine.py <archivo_xml>

Ejemplo:
    python ineoDocxCmdLine.py tasks/update_docx_task.xml
"""

import sys
import os
import logging

# Configurar logging solo a archivo, sin salida por consola
def setup_logging():
    """Configurar logging solo para archivo"""
    # Crear directorio de logs si no existe
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, 'ineoDocx.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='w')
            # Sin StreamHandler - no mostrar logs en consola
        ]
    )

def validate_xml_file(xml_file_path):
    """
    Valida que el archivo XML existe y es accesible
    
    Args:
        xml_file_path: Ruta al archivo XML
        
    Returns:
        bool: True si es válido, False si no
    """
    if not xml_file_path:
        print("ERROR: No se especificó archivo XML", file=sys.stderr)
        return False
    
    if not os.path.exists(xml_file_path):
        print(f"ERROR: Archivo XML no encontrado: {xml_file_path}", file=sys.stderr)
        return False
    
    if not xml_file_path.lower().endswith('.xml'):
        print(f"ERROR: El archivo debe tener extensión .xml: {xml_file_path}", file=sys.stderr)
        return False
    
    return True

def main():
    """
    Función principal del comando
    """
    # Verificar argumentos
    if len(sys.argv) != 2:
        print("Uso: python ineoDocxCmdLine.py <archivo_xml>", file=sys.stderr)
        print("Ejemplo: python ineoDocxCmdLine.py tasks/update_docx_task.xml", file=sys.stderr)
        sys.exit(1)
    
    xml_file_path = sys.argv[1]
    
    # Validar archivo XML
    if not validate_xml_file(xml_file_path):
        sys.exit(1)
    
    # Configurar logging
    setup_logging()
    
    try:
        # Importar después de configurar logging
        from core.update_docx import UpdateDocx
        
        # Procesar documento
        updater = UpdateDocx(xml_file_path)
        xml_response = updater.process_document()
        
        # Mostrar respuesta XML en stdout
        print(xml_response)
        
        # Salir con código 0 (éxito)
        sys.exit(0)
        
    except ImportError as e:
        print(f"ERROR: No se pudieron importar los módulos necesarios: {e}", file=sys.stderr)
        print("Verifique que esté ejecutando desde el directorio correcto", file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        print(f"ERROR: Error procesando documento: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
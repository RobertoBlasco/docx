"""
Memory Log Handler para capturar logs en memoria y generar XML
"""

import logging
from datetime import datetime
from typing import List
import xml.etree.ElementTree as ET


class MemoryLogHandler(logging.Handler):
    """Handler que captura logs en memoria para incluir en respuesta XML"""
    
    def __init__(self):
        super().__init__()
        self.log_entries: List[dict] = []
        self.setLevel(logging.DEBUG)
        
        # Formato personalizado para capturar toda la información
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        self.setFormatter(formatter)
    
    def emit(self, record):
        """Captura cada entrada de log"""
        try:
            log_entry = {
                'level': record.levelname,
                'message': record.getMessage(),
                'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                'logger': record.name
            }
            self.log_entries.append(log_entry)
        except Exception:
            # Si hay error capturando log, no queremos que rompa la aplicación
            pass
    
    def get_logs(self) -> List[dict]:
        """Obtiene todas las entradas de log capturadas"""
        return self.log_entries.copy()
    
    def clear_logs(self):
        """Limpia los logs almacenados"""
        self.log_entries.clear()
    
    def get_logs_as_xml_element(self) -> ET.Element:
        """
        Convierte los logs a elemento XML
        
        Returns:
            ET.Element: Elemento <logs> con todas las entradas
        """
        logs_element = ET.Element("logs")
        
        for entry in self.log_entries:
            log_entry = ET.SubElement(logs_element, "entry")
            log_entry.set("level", entry['level'])
            log_entry.set("timestamp", entry['timestamp'])
            log_entry.set("logger", entry['logger'])
            log_entry.text = entry['message']
        
        return logs_element


class XmlResponseBuilder:
    """Construye respuestas XML del sistema"""
    
    def __init__(self):
        pass
    
    def build_response(self, task_name: str, execution_results: dict, save_result: dict, logs: List[dict]) -> str:
        """
        Construye la respuesta XML completa
        
        Args:
            task_name: Nombre de la tarea ejecutada
            execution_results: Resultados de la ejecución de acciones
            save_result: Resultado del guardado
            logs: Lista de logs capturados
            
        Returns:
            str: XML formateado como string
        """
        # Elemento raíz
        root = ET.Element("ineoDocResponse")
        root.set("task", task_name)
        
        # Resumen de ejecución
        summary = ET.SubElement(root, "executionSummary")
        ET.SubElement(summary, "totalActions").text = str(execution_results.get('total_actions', 0))
        ET.SubElement(summary, "successfulActions").text = str(execution_results.get('successful_actions', 0))
        ET.SubElement(summary, "failedActions").text = str(execution_results.get('failed_actions', 0))
        ET.SubElement(summary, "executionTimeMs").text = str(execution_results.get('execution_time_ms', 0))
        ET.SubElement(summary, "status").text = "success" if save_result.get('success', False) else "error"
        
        # Output
        output = ET.SubElement(root, "output")
        output.set("type", save_result.get('type', 'unknown'))
        
        if save_result.get('type') == 'file':
            ET.SubElement(output, "filePath").text = save_result.get('path', '')
            ET.SubElement(output, "message").text = "Documento guardado exitosamente"
        elif save_result.get('type') == 'base64':
            ET.SubElement(output, "document").text = save_result.get('content', '')
            metadata = ET.SubElement(output, "metadata")
            metadata.set("sizeBytes", str(save_result.get('size_bytes', 0)))
            metadata.set("sizeBase64", str(save_result.get('size_base64', 0)))
        elif save_result.get('type') == 'error':
            ET.SubElement(output, "error").text = save_result.get('error', 'Error desconocido')
        
        # Logs
        logs_element = ET.SubElement(root, "logs")
        for log_entry in logs:
            entry = ET.SubElement(logs_element, "entry")
            entry.set("level", log_entry.get('level', 'INFO'))
            entry.set("timestamp", log_entry.get('timestamp', ''))
            entry.set("logger", log_entry.get('logger', ''))
            entry.text = log_entry.get('message', '')
        
        # Convertir a string con formato
        return self._prettify_xml(root)
    
    def _prettify_xml(self, element: ET.Element) -> str:
        """
        Formatea el XML para que sea legible
        
        Args:
            element: Elemento XML raíz
            
        Returns:
            str: XML formateado
        """
        # Importar minidom para formateo
        from xml.dom import minidom
        
        rough_string = ET.tostring(element, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="    ", encoding=None)
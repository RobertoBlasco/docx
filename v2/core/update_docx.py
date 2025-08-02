"""
Clase principal UpdateDocx - Orquestador de todas las acciones de manipulación de documentos
"""

import os
import sys
import logging

logger = logging.getLogger("IneoDocx")
from utils.memory_log_handler import MemoryLogHandler, XmlResponseBuilder

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.xml_task_parser import XmlTaskParser
from models.executable_actions import (
    TextReplacementAction, 
    TextToImageAction, 
    FieldCheckboxAction, 
    FieldTextAction,
    FieldImageAction
)
from core.docx_document import DocxDocument
from utils.content_loader import load_content

class UpdateDocx:
    """
    Orquestador principal para procesar documentos Word basado en configuración XML
    """
    
    def __init__(self, xml_file_path: str):
        """
        Inicializa el orquestador cargando la configuración XML
        
        Args:
            xml_file_path: Ruta al archivo XML de configuración
        """
        self.xml_file_path = xml_file_path
        self.task_data = None
        self.actions = []
        self.images_dict = {}
        
        # Memory log handler para capturar logs
        self.memory_log_handler = MemoryLogHandler()
        self.xml_response_builder = XmlResponseBuilder()
        
        # Añadir handler al logger
        logger.addHandler(self.memory_log_handler)
        
        # Managers (se inicializarán cuando se cargue el documento)
        self.text_replacement_manager = None
        self.text_to_image_manager = None
        self.field_checkbox_manager = None
        self.field_text_manager = None
        self.field_image_manager = None
        
        # Cargar y parsear XML
        self._load_xml_configuration()
    
    def _load_xml_configuration(self):
        """Carga y parsea la configuración XML"""
        try:
            parser = XmlTaskParser()
            self.task_data = parser.parse_xml_file(self.xml_file_path)
            
            # Crear diccionario de imágenes para acceso rápido
            self.images_dict = {img.id: img.path for img in self.task_data.images}
            
            logger.info("Configuración XML cargada correctamente")
            logger.info(f"\tTask: {self.task_data.task}")
            logger.info(f"\tInput: {self.task_data.data_in}")    
            logger.info(f"\tOutput: {self.task_data.data_out.path}")
            logger.info(f"\tImágenes: {len(self.task_data.images)}")
            logger.info(f"\tAcciones: {len(self.task_data.actions)}")
            
        except Exception as e:
            raise Exception(f"Error cargando configuración XML: {e}")
    
    def _initialize_managers(self, docx_document: DocxDocument):
        """Inicializa los managers con el documento"""
        self.text_replacement_manager = docx_document.text_replacement_manager
        self.text_to_image_manager = docx_document.text_to_image_manager
        self.field_checkbox_manager = docx_document.field_checkbox_manager
        self.field_text_manager = docx_document.field_text_manager
        self.field_image_manager = docx_document.field_image_manager
    
    def _create_executable_actions(self):
        """Convierte las acciones del XML en acciones ejecutables"""
        self.actions = []
        
        for action_data in self.task_data.actions:
            executable_action = None
            
            if action_data.name == 'replaceTextWithText':
                executable_action = TextReplacementAction(
                    action_id=action_data.id,
                    manager=self.text_replacement_manager,
                    replacements=action_data.items
                )
            
            elif action_data.name == 'replaceTextWithImage':
                executable_action = TextToImageAction(
                    action_id=action_data.id,
                    manager=self.text_to_image_manager,
                    replacements=action_data.items,
                    images_dict=self.images_dict
                )
            
            elif action_data.name == 'setFieldCheckbox':
                executable_action = FieldCheckboxAction(
                    action_id=action_data.id,
                    manager=self.field_checkbox_manager,
                    checkboxes=action_data.items
                )
            
            elif action_data.name == 'setFieldText':
                executable_action = FieldTextAction(
                    action_id=action_data.id,
                    manager=self.field_text_manager,
                    text_fields=action_data.items
                )
            
            elif action_data.name == 'setFieldImage':
                executable_action = FieldImageAction(
                    action_id=action_data.id,
                    manager=self.field_image_manager,
                    image_fields=action_data.items,
                    images_dict=self.images_dict
                )
            
            
            if executable_action:
                self.actions.append(executable_action)
                logger.info(f"Acción creada: {executable_action.get_description()}")
            else:
                logger.warning(f"Acción '{action_data.name}' no reconocida o no implementada")
    
    def load_document(self) -> DocxDocument:
        """
        Carga el documento especificado en la configuración XML
        
        Returns:
            DocxDocument: Documento cargado y listo para procesar
        """
        try:
            # Cargar documento usando content_loader
            doc_bytes = load_content(self.task_data.data_in)
            
            docx_document = DocxDocument(doc_bytes)
            
            # Inicializar managers
            self._initialize_managers(docx_document)
            
            # Crear acciones ejecutables
            logger.info("Creando acciones ejecutables...")
            self._create_executable_actions()
            
            logger.info("Documento cargado y listo para procesar")
            return docx_document
            
        except Exception as e:
            raise Exception(f"Error cargando documento: {e}")
    
    def execute_all_actions(self, docx_document: DocxDocument) -> dict:
        """
        Ejecuta todas las acciones en el documento
        
        Args:
            docx_document: Documento a procesar
            
        Returns:
            dict: Resumen de resultados
        """
        results = {
            'total_actions': len(self.actions),
            'successful_actions': 0,
            'failed_actions': 0,
            'details': []
        }
        
        logger.info(f"Ejecutando {len(self.actions)} acciones...")
        
        for i, action in enumerate(self.actions, 1):
            try:
                logger.info(f"Ejecutando acción {i}/{len(self.actions)}: {action.get_description()}")
                success = action.execute(docx_document)
                
                if success:
                    results['successful_actions'] += 1
                    logger.info(f"Acción {i} completada exitosamente")
                else:
                    results['failed_actions'] += 1
                    logger.error(f"Acción {i} falló")
                
                results['details'].append({
                    'action': action.get_description(),
                    'success': success
                })
                
            except Exception as e:
                results['failed_actions'] += 1
                error_msg = f"Error ejecutando acción: {e}"
                logger.error(error_msg)
                
                results['details'].append({
                    'action': action.get_description(),
                    'success': False,
                    'error': str(e)
                })
        
        return results
    
    def save_document(self, docx_document: DocxDocument) -> dict:
        """
        Guarda el documento procesado según el tipo de salida configurado
        
        Args:
            docx_document: Documento a guardar
            
        Returns:
            dict: Información sobre el guardado (ruta, base64, etc.)
        """
        try:
            out_type = self.task_data.data_out.out_type.lower()
            
            if out_type == "file":
                # Guardar como archivo
                output_path = self.task_data.data_out.path.replace('FILE://', '')
                docx_document.save_to_file(output_path)
                logger.info(f"Documento guardado en archivo: {output_path}")
                return {
                    'type': 'file',
                    'path': output_path,
                    'success': True
                }
                
            elif out_type == "base64":
                # Devolver como Base64
                import base64
                doc_bytes = docx_document.get_bytes()
                base64_content = base64.b64encode(doc_bytes).decode('utf-8')
                logger.info(f"Documento convertido a Base64 ({len(base64_content)} caracteres)")
                return {
                    'type': 'base64',
                    'content': base64_content,
                    'size_bytes': len(doc_bytes),
                    'size_base64': len(base64_content),
                    'success': True
                }
            
            else:
                raise ValueError(f"Tipo de salida no soportado: {out_type}")
            
        except Exception as e:
            raise Exception(f"Error guardando documento: {e}")
    
    def generate_xml_response(self, execution_results: dict, save_result: dict) -> str:
        """
        Genera respuesta XML completa con logs
        
        Args:
            execution_results: Resultados de ejecución de acciones
            save_result: Resultado del guardado
            
        Returns:
            str: XML response formateado
        """
        # Obtener logs capturados
        captured_logs = self.memory_log_handler.get_logs()
        
        # Generar XML
        xml_response = self.xml_response_builder.build_response(
            task_name=self.task_data.task,
            execution_results=execution_results,
            save_result=save_result,
            logs=captured_logs
        )
        
        return xml_response
    
    def process_document(self) -> str:
        """
        Proceso completo: cargar documento, ejecutar acciones y guardar
        
        Returns:
            str: Respuesta XML completa del procesamiento
        """
        import time
        start_time = time.time()
        
        try:
            # Cargar documento
            docx_document = self.load_document()
            
            # Ejecutar todas las acciones
            results = self.execute_all_actions(docx_document)
            
            # Guardar documento
            save_result = self.save_document(docx_document)
            
            # Calcular tiempo total de ejecución
            end_time = time.time()
            execution_time_ms = int((end_time - start_time) * 1000)
            
            # Resumen final
            logger.info("Resumen final:")
            logger.info(f"Total acciones: {results['total_actions']}")
            logger.info(f"Acciones exitosas: {results['successful_actions']}")  
            logger.info(f"Acciones fallidas: {results['failed_actions']}")
            logger.info(f"Tiempo de ejecución: {execution_time_ms}ms")
            
            if save_result['type'] == 'file':
                logger.info(f"Documento guardado en: {save_result['path']}")
            else:
                logger.info(f"Documento como Base64: {save_result['size_base64']} caracteres")
            
            # Añadir tiempo de ejecución a resultados
            results['execution_time_ms'] = execution_time_ms
            
            # Generar respuesta XML siempre (independiente del outType)
            xml_response = self.generate_xml_response(results, save_result)
            return xml_response
            
        except Exception as e:
            # Calcular tiempo incluso en error
            end_time = time.time()
            execution_time_ms = int((end_time - start_time) * 1000)
            
            logger.error(f"Error en proceso: {e}")
            
            error_results = {
                'total_actions': len(self.actions) if self.actions else 0,
                'successful_actions': 0,
                'failed_actions': 0,
                'document_saved': False,
                'error': str(e),
                'execution_time_ms': execution_time_ms
            }
            
            # Generar XML de error
            error_save_result = {'type': 'error', 'success': False, 'error': str(e)}
            xml_response = self.generate_xml_response(error_results, error_save_result)
            return xml_response
    
    def get_action_summary(self) -> dict:
        """
        Obtiene resumen de acciones sin ejecutar
        
        Returns:
            dict: Resumen de acciones configuradas
        """
        summary = {}
        
        for action in self.actions:
            action_type = type(action).__name__
            if action_type not in summary:
                summary[action_type] = 0
            summary[action_type] += 1
        
        return summary
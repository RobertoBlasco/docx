# #!/usr/bin/env python3
# """
# action_set_bookmark_image.py - Nuevo archivo independiente
# Establece imágenes en marcadores (bookmarks) del documento
# """

# import logging
# from action_docx import Document
# from docx.oxml.ns import qn
# from docx.oxml import OxmlElement
# from docx.shared import Inches
# import io

# logger = logging.getLogger("IneoDocx")

# class ActionSetBookmarkImage:
#     """
#     Acción para establecer imágenes en marcadores usando python-docx
#     """
    
#     def __init__(self, document_path: str):
#         """
#         Inicializa la acción con el documento a modificar
        
#         Args:
#             document_path: Ruta al documento .docx
#         """
#         self.document_path = document_path
#         self.document = None
        
#     def load_document(self) -> bool:
#         """Carga el documento Word"""
#         try:
#             self.document = Document(self.document_path)
#             logger.info(f"Documento cargado: {self.document_path}")
#             return True
#         except Exception as e:
#             logger.error(f"Error cargando documento: {e}")
#             return False
    
#     def find_bookmark_by_name(self, bookmark_name: str) -> list:
#         """
#         Busca un marcador por su nombre en todo el documento
        
#         Args:
#             bookmark_name: Nombre del marcador a buscar
            
#         Returns:
#             list: Lista de elementos bookmark encontrados
#         """
#         if not self.document:
#             logger.error("Documento no cargado")
#             return []
            
#         found_bookmarks = []
        
#         # Función para buscar marcadores en un elemento
#         def search_in_element(element, location=""):
#             bookmarks = element.findall('.//w:bookmarkStart', {
#                 'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
#             })
            
#             for bookmark in bookmarks:
#                 name = bookmark.get(qn('w:name'))
#                 if name == bookmark_name:
#                     found_bookmarks.append({
#                         'bookmark_element': bookmark,
#                         'location': location,
#                         'name': name
#                     })
#                     logger.info(f"Marcador encontrado: {bookmark_name} en {location}")
        
#         # Buscar en body
#         body_element = self.document._body._element
#         search_in_element(body_element, "body")
        
#         # Buscar en headers y footers
#         for section in self.document.sections:
#             if section.header:
#                 header_element = section.header._element
#                 search_in_element(header_element, "header")
                
#             if section.footer:
#                 footer_element = section.footer._element
#                 search_in_element(footer_element, "footer")
        
#         return found_bookmarks
    
#     def set_image_at_bookmark(self, bookmark_name: str, image_data: bytes, width: int, height: int) -> bool:
#         """
#         Establece una imagen en un marcador (reemplaza si existe, inserta si no existe)
        
#         Args:
#             bookmark_name: Nombre del marcador
#             image_data: Datos binarios de la imagen
#             width: Ancho en píxeles
#             height: Alto en píxeles
            
#         Returns:
#             bool: True si se estableció la imagen correctamente
#         """
#         bookmarks = self.find_bookmark_by_name(bookmark_name)
        
#         if not bookmarks:
#             logger.warning(f"No se encontró marcador con nombre: {bookmark_name}")
#             return False
        
#         success = False
        
#         for bookmark_info in bookmarks:
#             try:
#                 # Obtener el párrafo que contiene el marcador
#                 paragraph = self._get_bookmark_paragraph(bookmark_info)
                
#                 if paragraph is None:
#                     logger.warning(f"No se pudo obtener párrafo para marcador: {bookmark_name}")
#                     continue
                
#                 # Buscar imágenes existentes en el párrafo
#                 existing_images = self._find_images_in_paragraph(paragraph)
                
#                 if existing_images:
#                     # Reemplazar imagen existente
#                     result = self._replace_existing_image(paragraph, existing_images[0], image_data, width, height)
#                     logger.info(f"Imagen reemplazada en marcador: {bookmark_name}")
#                 else:
#                     # Insertar nueva imagen
#                     result = self._insert_new_image(paragraph, bookmark_info, image_data, width, height)
#                     logger.info(f"Nueva imagen insertada en marcador: {bookmark_name}")
                
#                 if result:
#                     success = True
                    
#             except Exception as e:
#                 logger.error(f"Error procesando marcador {bookmark_name}: {e}")
#                 continue
        
#         return success
    
#     def _get_bookmark_paragraph(self, bookmark_info):
#         """
#         Obtiene el párrafo que contiene el marcador
        
#         Args:
#             bookmark_info: Información del marcador
            
#         Returns:
#             Elemento párrafo o None
#         """
#         bookmark_element = bookmark_info['bookmark_element']
        
#         # Buscar el párrafo padre
#         paragraph = bookmark_element
#         while paragraph is not None and not paragraph.tag.endswith('p'):
#             paragraph = paragraph.getparent()
        
#         return paragraph
    
#     def _find_images_in_paragraph(self, paragraph):
#         """
#         Encuentra imágenes existentes en un párrafo
        
#         Args:
#             paragraph: Elemento párrafo
            
#         Returns:
#             list: Lista de elementos de imagen encontrados
#         """
#         if paragraph is None:
#             return []
        
#         # Buscar elementos w:drawing
#         drawings = paragraph.findall('.//w:drawing', {
#             'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
#         })
        
#         images = []
#         for drawing in drawings:
#             # Buscar a:blip dentro del drawing
#             blips = drawing.findall('.//a:blip', {
#                 'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
#             })
            
#             for blip in blips:
#                 embed_id = blip.get(qn('r:embed'))
#                 if embed_id:
#                     images.append({
#                         'drawing': drawing,
#                         'blip': blip,
#                         'embed_id': embed_id
#                     })
        
#         return images
    
#     def _replace_existing_image(self, paragraph, existing_image, image_data, width, height):
#         """
#         Reemplaza una imagen existente
        
#         Args:
#             paragraph: Elemento párrafo
#             existing_image: Información de la imagen existente
#             image_data: Datos de la nueva imagen
#             width: Ancho en píxeles
#             height: Alto en píxeles
            
#         Returns:
#             bool: True si se reemplazó correctamente
#         """
#         try:
#             # Crear nueva relación de imagen usando tempfile
#             import tempfile
            
#             # Crear archivo temporal
#             with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
#                 temp_file.write(image_data)
#                 temp_file_path = temp_file.name
            
#             # Usar python-docx para crear la relación
#             from docx.shared import Inches
#             from docx.parts.image import ImagePart
#             from docx.opc.constants import RELATIONSHIP_TYPE as RT
            
#             # Crear la imagen usando el documento
#             image_part = ImagePart.from_image(temp_file_path, self.document.part)
#             rId = self.document.part.relate_to(image_part, RT.IMAGE)
            
#             # Limpiar archivo temporal
#             import os
#             os.unlink(temp_file_path)
            
#             # Actualizar el a:blip con el nuevo r:embed
#             blip = existing_image['blip']
#             blip.set(qn('r:embed'), rId)
            
#             # Actualizar dimensiones si se especificaron
#             if width and height:
#                 self._update_image_dimensions(existing_image['drawing'], width, height)
            
#             logger.info(f"Imagen reemplazada con nuevo rId: {rId}")
#             return True
            
#         except Exception as e:
#             logger.error(f"Error reemplazando imagen: {e}")
#             return False
    
#     def _insert_new_image(self, paragraph, bookmark_info, image_data, width, height):
#         """
#         Inserta una nueva imagen en el marcador
        
#         Args:
#             paragraph: Elemento párrafo
#             bookmark_info: Información del marcador
#             image_data: Datos de la imagen
#             width: Ancho en píxeles
#             height: Alto en píxeles
            
#         Returns:
#             bool: True si se insertó correctamente
#         """
#         try:
#             # Crear nueva relación de imagen usando tempfile
#             import tempfile
            
#             # Crear archivo temporal
#             with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
#                 temp_file.write(image_data)
#                 temp_file_path = temp_file.name
            
#             # Usar python-docx para crear la relación
#             from docx.shared import Inches
#             from docx.parts.image import ImagePart
#             from docx.opc.constants import RELATIONSHIP_TYPE as RT
            
#             # Crear la imagen usando el documento
#             image_part = ImagePart.from_image(temp_file_path, self.document.part)
#             rId = self.document.part.relate_to(image_part, RT.IMAGE)
            
#             # Limpiar archivo temporal
#             import os
#             os.unlink(temp_file_path)
            
#             # Crear elemento de imagen
#             image_element = self._create_image_element(rId, width, height)
            
#             # Crear nuevo run para la imagen
#             new_run = OxmlElement('w:r')
#             new_run.append(image_element)
            
#             # Insertar después del bookmarkStart
#             bookmark_element = bookmark_info['bookmark_element']
#             parent = bookmark_element.getparent()
            
#             # Encontrar posición del bookmark
#             bookmark_index = list(parent).index(bookmark_element)
            
#             # Insertar después del bookmark
#             parent.insert(bookmark_index + 1, new_run)
            
#             logger.info(f"Nueva imagen insertada con rId: {rId}")
#             return True
            
#         except Exception as e:
#             logger.error(f"Error insertando imagen: {e}")
#             return False
    
#     def _create_image_element(self, r_id, width, height):
#         """
#         Crea la estructura XML completa para una imagen
        
#         Args:
#             r_id: ID de la relación de la imagen
#             width: Ancho en píxeles
#             height: Alto en píxeles
            
#         Returns:
#             Elemento XML de la imagen
#         """
#         # Convertir píxeles a EMUs (English Metric Units)
#         width_emu = width * 9525  # 1 pixel = 9525 EMUs aproximadamente
#         height_emu = height * 9525
        
#         # Crear elemento drawing
#         drawing = OxmlElement('w:drawing')
        
#         # Crear inline
#         inline = OxmlElement('wp:inline')
#         inline.set('distT', '0')
#         inline.set('distB', '0')
#         inline.set('distL', '0')
#         inline.set('distR', '0')
        
#         # Crear extent
#         extent = OxmlElement('wp:extent')
#         extent.set('cx', str(width_emu))
#         extent.set('cy', str(height_emu))
#         inline.append(extent)
        
#         # Crear docPr
#         docpr = OxmlElement('wp:docPr')
#         docpr.set('id', '1')
#         docpr.set('name', 'Image')
#         inline.append(docpr)
        
#         # Crear graphic
#         graphic = OxmlElement('a:graphic')
#         graphic.set(qn('xmlns:a'), 'http://schemas.openxmlformats.org/drawingml/2006/main')
        
#         # Crear graphicData
#         graphic_data = OxmlElement('a:graphicData')
#         graphic_data.set('uri', 'http://schemas.openxmlformats.org/drawingml/2006/picture')
        
#         # Crear pic:pic
#         pic = OxmlElement('pic:pic')
#         pic.set(qn('xmlns:pic'), 'http://schemas.openxmlformats.org/drawingml/2006/picture')
        
#         # Crear nvPicPr
#         nvpicpr = OxmlElement('pic:nvPicPr')
#         cnvpr = OxmlElement('pic:cNvPr')
#         cnvpr.set('id', '1')
#         cnvpr.set('name', 'Image')
#         nvpicpr.append(cnvpr)
        
#         cnvpicpr = OxmlElement('pic:cNvPicPr')
#         nvpicpr.append(cnvpicpr)
        
#         pic.append(nvpicpr)
        
#         # Crear blipFill
#         blip_fill = OxmlElement('pic:blipFill')
#         blip = OxmlElement('a:blip')
#         blip.set(qn('r:embed'), r_id)
#         blip_fill.append(blip)
        
#         stretch = OxmlElement('a:stretch')
#         fill_rect = OxmlElement('a:fillRect')
#         stretch.append(fill_rect)
#         blip_fill.append(stretch)
        
#         pic.append(blip_fill)
        
#         # Crear spPr
#         sppr = OxmlElement('pic:spPr')
#         xfrm = OxmlElement('a:xfrm')
#         off = OxmlElement('a:off')
#         off.set('x', '0')
#         off.set('y', '0')
#         xfrm.append(off)
        
#         ext = OxmlElement('a:ext')
#         ext.set('cx', str(width_emu))
#         ext.set('cy', str(height_emu))
#         xfrm.append(ext)
        
#         sppr.append(xfrm)
        
#         prst_geom = OxmlElement('a:prstGeom')
#         prst_geom.set('prst', 'rect')
#         av_lst = OxmlElement('a:avLst')
#         prst_geom.append(av_lst)
#         sppr.append(prst_geom)
        
#         pic.append(sppr)
        
#         # Ensamblar todo
#         graphic_data.append(pic)
#         graphic.append(graphic_data)
#         inline.append(graphic)
#         drawing.append(inline)
        
#         return drawing
    
#     def _update_image_dimensions(self, drawing, width, height):
#         """
#         Actualiza las dimensiones de una imagen existente
        
#         Args:
#             drawing: Elemento drawing
#             width: Ancho en píxeles
#             height: Alto en píxeles
#         """
#         try:
#             # Convertir píxeles a EMUs
#             width_emu = width * 9525
#             height_emu = height * 9525
            
#             # Actualizar wp:extent
#             extent = drawing.find('.//wp:extent', {
#                 'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
#             })
#             if extent is not None:
#                 extent.set('cx', str(width_emu))
#                 extent.set('cy', str(height_emu))
            
#             # Actualizar a:ext
#             ext = drawing.find('.//a:ext', {
#                 'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
#             })
#             if ext is not None:
#                 ext.set('cx', str(width_emu))
#                 ext.set('cy', str(height_emu))
            
#             logger.info(f"Dimensiones actualizadas: {width}x{height} píxeles")
            
#         except Exception as e:
#             logger.error(f"Error actualizando dimensiones: {e}")
    
#     def save_document(self, output_path: str = None) -> bool:
#         """
#         Guarda el documento modificado
        
#         Args:
#             output_path: Ruta de salida. Si es None, sobrescribe el original
            
#         Returns:
#             bool: True si se guardó correctamente
#         """
#         if not self.document:
#             logger.error("No hay documento para guardar")
#             return False
            
#         try:
#             save_path = output_path or self.document_path
#             self.document.save(save_path)
#             logger.info(f"Documento guardado en: {save_path}")
#             return True
#         except Exception as e:
#             logger.error(f"Error guardando documento: {e}")
#             return False

# # Función standalone para compatibilidad
# def set_image_at_bookmark(document_path: str, bookmark_name: str, image_data: bytes, width: int, height: int) -> bool:
#     """
#     Función standalone para establecer imagen en marcador
    
#     Args:
#         document_path: Ruta al documento
#         bookmark_name: Nombre del marcador
#         image_data: Datos binarios de la imagen
#         width: Ancho en píxeles
#         height: Alto en píxeles
        
#     Returns:
#         bool: True si se estableció correctamente
#     """
#     action = ActionSetBookmarkImage(document_path)
    
#     if not action.load_document():
#         return False
        
#     success = action.set_image_at_bookmark(bookmark_name, image_data, width, height)
    
#     if success:
#         action.save_document()
        
#     return success
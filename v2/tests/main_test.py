import io
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

import docx_document

from models.form_checkbox import FormCheckBoxLegacy

def main() :

    file_in = "/home/rj/2.docx"
    file_image = "/home/rj/firma01.png"

    # file_bytes = None
    # with open(file_in, 'rb') as file:
    #     file_bytes = file.read()

    # docx = docx_document.DocxDocument(file_bytes)
    # checkboxes = docx.get_checkboxes()    
    # for checkbox in checkboxes :
    #     if checkbox.name == "AT" :set_checkbox_value
    #         success = docx.(checkbox, True)
    #         if success :
    #             print ("Fichero modificado")
    #             docx.save_to_file("borrar.docx")
     
    
    # text_occurrences =docx.get_text_occurrences("nombrecontactoemplegal")
    # for text_occurrence in text_occurrences :
    #     text_occurrence.replace_text = "Juan Pérez"
    #     success = docx.replace_text_occurrence(text_occurrence)
    #     if success :
    #          print(f"Reemplazado en {text_occurrence.location}")
    
    
    ## Reemplazar Texto por Imagen
    with open(file_in, "rb") as docx_file :
        docx_file_bytes = docx_file.read()
    
    
    search_text = "31/1995"
    with open(file_image, "rb") as img_file :
        image_data = img_file.read()
    
    docx = docx_document.DocxDocument(docx_file_bytes)
    image_replacements = docx.get_text_for_image_replacement(search_text)
    for image_replacement in image_replacements :
        image_replacement.image_data = image_data
        image_replacement.width = 50
        image_replacement.height = 50
        success = docx.replace_text_with_image(image_replacement)
    
    docx.save_to_file("borrar.docx")
    
    
    # nombrecontactoemplegal

        

if __name__ == "__main__" :
    main()
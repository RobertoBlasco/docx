#!/usr/bin/env python3
"""
Test específico para verificar que los checkboxes se marcan correctamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.docx_document import DocxDocument

def test_checkbox_before_and_after():
    """Verifica que los checkboxes cambian de estado correctamente"""
    
    doc_path_input = "/home/rj/Documentos/prueba.docx"
    doc_path_output = "/home/rj/Documentos/prueba_salida.docx"
    
    print("🔍 ANTES del procesamiento:")
    with open(doc_path_input, 'rb') as f:
        doc_bytes = f.read()
    
    docx_doc_before = DocxDocument(doc_bytes)
    checkboxes_before = docx_doc_before.get_fields_checkbox()
    
    for i, checkbox in enumerate(checkboxes_before, 1):
        if hasattr(checkbox, 'tag'):
            print(f"   {i}. Checkbox '{checkbox.tag}': checked={checkbox.checked} ({checkbox.get_value()})")
        elif hasattr(checkbox, 'name'):
            print(f"   {i}. Checkbox '{checkbox.name}': default={checkbox.default} ({checkbox.get_value()})")
    
    print("\n🔍 DESPUÉS del procesamiento:")
    
    if os.path.exists(doc_path_output):
        with open(doc_path_output, 'rb') as f:
            doc_bytes_after = f.read()
        
        docx_doc_after = DocxDocument(doc_bytes_after)
        checkboxes_after = docx_doc_after.get_fields_checkbox()
        
        for i, checkbox in enumerate(checkboxes_after, 1):
            if hasattr(checkbox, 'tag'):
                print(f"   {i}. Checkbox '{checkbox.tag}': checked={checkbox.checked} ({checkbox.get_value()})")
            elif hasattr(checkbox, 'name'):
                print(f"   {i}. Checkbox '{checkbox.name}': default={checkbox.default} ({checkbox.get_value()})")
        
        print("\n📊 COMPARACIÓN:")
        print("Expected: check_01=False, check_02=True")
        
        check_01_after = None
        check_02_after = None
        
        for checkbox in checkboxes_after:
            if hasattr(checkbox, 'tag'):
                if checkbox.tag == 'check_01':
                    check_01_after = checkbox.get_value()
                elif checkbox.tag == 'check_02':
                    check_02_after = checkbox.get_value()
            elif hasattr(checkbox, 'name'):
                if checkbox.name == 'check_01':
                    check_01_after = checkbox.get_value()
                elif checkbox.name == 'check_02':
                    check_02_after = checkbox.get_value()
        
        print(f"Actual:   check_01={check_01_after}, check_02={check_02_after}")
        
        if check_01_after == False and check_02_after == True:
            print("✅ Los checkboxes están marcados correctamente!")
        else:
            print("❌ Los checkboxes NO están marcados correctamente!")
            
    else:
        print("❌ No se encontró el archivo de salida")

if __name__ == "__main__":
    test_checkbox_before_and_after()
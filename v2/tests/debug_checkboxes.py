#!/usr/bin/env python3
"""
Debug script para analizar checkboxes en el documento
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.docx_document import DocxDocument

def debug_checkboxes():
    """Analiza todos los checkboxes del documento"""
    
    # Ruta al documento de prueba
    doc_path = "/home/rj/Documentos/prueba.docx"
    
    if not os.path.exists(doc_path):
        print(f"❌ Error: No se encontró el documento en {doc_path}")
        return
    
    print(f"🔍 Analizando checkboxes en: {doc_path}")
    
    try:
        # Cargar documento
        with open(doc_path, 'rb') as f:
            doc_bytes = f.read()
        
        docx_doc = DocxDocument(doc_bytes)
        
        # Obtener todos los checkboxes
        checkboxes = docx_doc.get_fields_checkbox()
        
        print(f"\n📋 CHECKBOXES ENCONTRADOS: {len(checkboxes)}")
        
        if not checkboxes:
            print("❌ No se encontraron checkboxes en el documento")
        else:
            for i, checkbox in enumerate(checkboxes, 1):
                print(f"\n{i}. {type(checkbox).__name__}")
                print(f"   - Tipo: {type(checkbox)}")
                
                # Información específica según el tipo
                if hasattr(checkbox, 'name'):  # Legacy
                    print(f"   - Name: '{checkbox.name}'")
                    print(f"   - Default: {checkbox.default}")
                    print(f"   - Valor actual: {checkbox.get_value()}")
                    
                if hasattr(checkbox, 'tag'):  # Modern
                    print(f"   - Tag: '{checkbox.tag}'")
                    print(f"   - Alias: '{checkbox.alias}'")
                    print(f"   - Checked: {checkbox.checked}")
                    print(f"   - Valor actual: {checkbox.get_value()}")
                    
                if hasattr(checkbox, 'xpath'):
                    print(f"   - XPath: '{checkbox.xpath}'")
        
        # Buscar específicamente los que necesitamos
        print(f"\n🔍 BÚSQUEDA ESPECÍFICA:")
        print(f"Buscando 'check_01' y 'check_02'...")
        
        found_check_01 = False
        found_check_02 = False
        
        for checkbox in checkboxes:
            # Buscar por name (legacy)
            if hasattr(checkbox, 'name'):
                if checkbox.name == 'check_01':
                    print(f"✅ Encontrado check_01 (legacy): {checkbox}")
                    found_check_01 = True
                elif checkbox.name == 'check_02':
                    print(f"✅ Encontrado check_02 (legacy): {checkbox}")
                    found_check_02 = True
            
            # Buscar por tag (modern)
            if hasattr(checkbox, 'tag'):
                if checkbox.tag == 'check_01':
                    print(f"✅ Encontrado check_01 (modern): {checkbox}")
                    found_check_01 = True
                elif checkbox.tag == 'check_02':
                    print(f"✅ Encontrado check_02 (modern): {checkbox}")
                    found_check_02 = True
        
        if not found_check_01:
            print(f"❌ No se encontró 'check_01'")
        if not found_check_02:
            print(f"❌ No se encontró 'check_02'")
            
    except Exception as e:
        print(f"❌ Error analizando documento: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_checkboxes()
#!/usr/bin/env python3
"""
Test simple para TextFieldManager - Muestra todos los campos de texto del documento
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.docx_document import DocxDocument

def main():
    """
    Muestra todos los campos de texto encontrados en el documento
    """
    # Ruta al documento de prueba (ajustar según tu estructura)
    document_path = "/home/rj/Documentos/prueba.docx"
    
    if not os.path.exists(document_path):
        print(f"❌ Error: El archivo '{document_path}' no existe")
        print("ℹ️  Ajusta la ruta del documento en el código")
        return
    
    try:
        print("🚀 Iniciando análisis de campos de texto...")
        print(f"📁 Documento: {document_path}")
        
        # Cargar documento
        with open(document_path, 'rb') as file:
            doc_bytes = file.read()
        
        # Crear instancia de DocxDocument
        docx_doc = DocxDocument(doc_bytes)
        
        # Obtener todos los campos de texto usando el manager
        text_fields = docx_doc.get_text_fields()
        
        print(f"\n📝 Campos de texto encontrados: {len(text_fields)}")
        print("=" * 50)
        
        if not text_fields:
            print("ℹ️  No se encontraron campos de texto con tag en el documento")
            return
        
        # Mostrar cada campo encontrado
        for i, field in enumerate(text_fields, 1):
            print(f"\n{i}. CAMPO DE TEXTO:")
            
            if hasattr(field, 'name'):  # Legacy
                print(f"   - Tipo: Legacy")
                print(f"   - Name: {field.name}")
                print(f"   - Valor actual: '{field.get_value()}'")
            else:  # Modern
                # Determinar subtipo por xpath
                if 'w:text]' in field.xpath:
                    subtipo = "Plain (w:text)"
                elif 'w:richText]' in field.xpath:
                    subtipo = "Rich (w:richText)"
                else:
                    subtipo = "Free (sin restricciones)"
                
                print(f"   - Tipo: Modern - {subtipo}")
                print(f"   - Tag: {field.tag}")
                print(f"   - Alias: {field.alias}")
                print(f"   - Valor actual: '{field.get_value()}'")
                if hasattr(field, 'placeholder') and field.placeholder:
                    print(f"   - Placeholder: {field.placeholder}")
            
            print(f"   - XPath: {field.xpath}")
        
        print("\n✅ Análisis completado")
        
    except Exception as e:
        print(f"❌ Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
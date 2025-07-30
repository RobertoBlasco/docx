#!/usr/bin/env python3
"""
Test para el parser XML robusto
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.xml_task_parser import XmlTaskParser

def main():
    """
    Prueba el parser XML con el archivo de configuración
    """
    # Ruta al XML de configuración
    xml_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tasks', 'update_docx_task.xml')
    
    if not os.path.exists(xml_file):
        print(f"❌ Error: No se encontró el archivo XML en {xml_file}")
        return
    
    print("🚀 Iniciando test del parser XML robusto...")
    print(f"📄 Usando archivo XML: {xml_file}")
    
    try:
        # Crear parser
        parser = XmlTaskParser()
        
        # Validar XML
        print(f"\n🔍 Validando XML...")
        if parser.validate_xml_file(xml_file):
            print("✅ XML válido")
        else:
            print("❌ XML inválido")
            return
        
        # Parsear XML
        print(f"\n📖 Parseando XML...")
        docx_task = parser.parse_xml_file(xml_file)
        
        # Mostrar resultados
        print(f"\n📋 INFORMACIÓN DEL TASK:")
        print(f"   - Task: {docx_task.task}")
        print(f"   - Data In: {docx_task.data_in}")
        print(f"   - Data Out: {docx_task.data_out.path} (overwrite: {docx_task.data_out.overwrite})")
        print(f"   - Imágenes: {len(docx_task.images)}")
        print(f"   - Acciones: {len(docx_task.actions)}")
        
        # Mostrar imágenes
        if docx_task.images:
            print(f"\n🖼️  IMÁGENES:")
            for i, img in enumerate(docx_task.images, 1):
                print(f"   {i}. ID: {img.id} → {img.path}")
        
        # Mostrar acciones
        print(f"\n🎯 ACCIONES:")
        for i, action in enumerate(docx_task.actions, 1):
            print(f"\n   {i}. {action.name} (id: {action.id})")
            print(f"      Items: {len(action.items)}")
            
            for j, item in enumerate(action.items, 1):
                if hasattr(item, 'search_text'):
                    if hasattr(item, 'replacement_text'):
                        # TextReplacementItem
                        print(f"         {j}. '{item.search_text}' → '{item.replacement_text}'")
                    else:
                        # ImageReplacementItem
                        print(f"         {j}. '{item.search_text}' → IMG:{item.img_id} ({item.width}x{item.height})")
                elif hasattr(item, 'name') and hasattr(item, 'value') and isinstance(item.value, bool):
                    # CheckboxForm
                    print(f"         {j}. Checkbox '{item.name}' = {item.value}")
                elif hasattr(item, 'tag'):
                    # TextFieldForm
                    print(f"         {j}. TextField '{item.tag}' = '{item.value}'")
                elif hasattr(item, 'name') and hasattr(item, 'img_id'):
                    # BookmarkImage
                    print(f"         {j}. Bookmark '{item.name}' → IMG:{item.img_id} ({item.width}x{item.height})")
        
        print("\n✅ Parsing completado exitosamente")
        
        # Demostrar acceso tipado
        print(f"\n🔬 DEMOSTRACIÓN DE ACCESO TIPADO:")
        for action in docx_task.actions:
            if action.name == 'setTextField':
                print(f"   - Encontrada acción setTextField con {len(action.items)} campos:")
                for item in action.items:
                    print(f"     * Campo '{item.tag}' → '{item.value}'")
                break
        
    except Exception as e:
        print(f"❌ Error durante el parsing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
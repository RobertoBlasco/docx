#!/usr/bin/env python3
"""
Test detallado para verificar paso a paso la modificación de checkboxes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.docx_document import DocxDocument
from models.executable_actions import FieldCheckboxAction
from models.xml_task_parser import FieldCheckbox

def test_checkbox_step_by_step():
    """Test paso a paso del proceso de modificación de checkboxes"""
    
    doc_path = "/home/rj/Documentos/prueba.docx"
    
    print("🔧 TEST DETALLADO DE CHECKBOXES")
    print("=" * 50)
    
    # 1. Cargar documento
    with open(doc_path, 'rb') as f:
        doc_bytes = f.read()
    
    docx_doc = DocxDocument(doc_bytes)
    
    # 2. Obtener checkboxes existentes
    print("\n📋 CHECKBOXES EN EL DOCUMENTO:")
    checkboxes = docx_doc.get_fields_checkbox()
    
    for i, checkbox in enumerate(checkboxes, 1):
        print(f"   {i}. Tipo: {type(checkbox).__name__}")
        if hasattr(checkbox, 'tag'):
            print(f"      Tag: '{checkbox.tag}'")
            print(f"      Checked: {checkbox.checked}")
            print(f"      Valor: {checkbox.get_value()}")
        elif hasattr(checkbox, 'name'):
            print(f"      Name: '{checkbox.name}'")
            print(f"      Default: {checkbox.default}")
            print(f"      Valor: {checkbox.get_value()}")
        print()
    
    # 3. Crear acciones de prueba
    checkbox_actions = [
        FieldCheckbox(name='check_01', value=False),  # Debe quedar sin marcar
        FieldCheckbox(name='check_02', value=True)    # Debe quedar marcado
    ]
    
    print("🎯 ACCIONES A EJECUTAR:")
    for action in checkbox_actions:
        print(f"   - '{action.name}' → {action.value}")
    
    # 4. Crear y ejecutar acción
    checkbox_action = FieldCheckboxAction(
        action_id="test_checkboxes",
        manager=docx_doc.field_checkbox_manager,
        checkboxes=checkbox_actions
    )
    
    print("\n🚀 EJECUTANDO ACCIÓN...")
    result = checkbox_action.execute(docx_doc)
    print(f"Resultado: {'✅ Exitoso' if result else '❌ Falló'}")
    
    # 5. Verificar cambios
    print("\n🔍 VERIFICANDO CAMBIOS:")
    checkboxes_after = docx_doc.get_fields_checkbox()
    
    for i, checkbox in enumerate(checkboxes_after, 1):
        print(f"   {i}. Tipo: {type(checkbox).__name__}")
        if hasattr(checkbox, 'tag'):
            print(f"      Tag: '{checkbox.tag}'")
            print(f"      Checked: {checkbox.checked}")
            print(f"      Valor: {checkbox.get_value()}")
            if checkbox.tag == 'check_01' and checkbox.get_value() == False:
                print("      ✅ check_01 correctamente desmarcado")
            elif checkbox.tag == 'check_02' and checkbox.get_value() == True:
                print("      ✅ check_02 correctamente marcado")
        elif hasattr(checkbox, 'name'):
            print(f"      Name: '{checkbox.name}'")
            print(f"      Default: {checkbox.default}")
            print(f"      Valor: {checkbox.get_value()}")
            if checkbox.name == 'check_01' and checkbox.get_value() == False:
                print("      ✅ check_01 correctamente desmarcado")
            elif checkbox.name == 'check_02' and checkbox.get_value() == True:
                print("      ✅ check_02 correctamente marcado")
        print()
    
    # 6. Guardar y verificar persistencia
    output_path = "/tmp/test_checkboxes.docx"
    docx_doc.save_to_file(output_path)
    print(f"📄 Documento guardado en: {output_path}")
    
    # 7. Recargar y verificar
    print("\n🔄 RECARGANDO DOCUMENTO GUARDADO:")
    with open(output_path, 'rb') as f:
        doc_bytes_reloaded = f.read()
    
    docx_doc_reloaded = DocxDocument(doc_bytes_reloaded)
    checkboxes_reloaded = docx_doc_reloaded.get_fields_checkbox()
    
    print("Estado después de recargar:")
    for checkbox in checkboxes_reloaded:
        if hasattr(checkbox, 'tag'):
            if checkbox.tag in ['check_01', 'check_02']:
                status = "✅" if (checkbox.tag == 'check_01' and not checkbox.get_value()) or (checkbox.tag == 'check_02' and checkbox.get_value()) else "❌"
                print(f"   {status} {checkbox.tag}: {checkbox.get_value()}")
        elif hasattr(checkbox, 'name'):
            if checkbox.name in ['check_01', 'check_02']:
                status = "✅" if (checkbox.name == 'check_01' and not checkbox.get_value()) or (checkbox.name == 'check_02' and checkbox.get_value()) else "❌"
                print(f"   {status} {checkbox.name}: {checkbox.get_value()}")

if __name__ == "__main__":
    test_checkbox_step_by_step()
#!/usr/bin/env python3
"""
Debug script para analizar bookmarks en el documento
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.docx_document import DocxDocument

def debug_bookmarks():
    """Analiza todos los bookmarks del documento"""
    
    # Ruta al documento de prueba
    doc_path = "/home/rj/Documentos/prueba.docx"
    
    if not os.path.exists(doc_path):
        print(f"❌ Error: No se encontró el documento en {doc_path}")
        return
    
    print(f"🔍 Analizando bookmarks en: {doc_path}")
    
    try:
        # Cargar documento
        with open(doc_path, 'rb') as f:
            doc_bytes = f.read()
        
        docx_doc = DocxDocument(doc_bytes)
        
        # Obtener todos los bookmarks
        bookmarks = docx_doc.get_bookmarks()
        
        print(f"\n📑 BOOKMARKS ENCONTRADOS: {len(bookmarks)}")
        
        if not bookmarks:
            print("❌ No se encontraron bookmarks en el documento")
        else:
            for i, bookmark in enumerate(bookmarks, 1):
                print(f"\n{i}. Bookmark:")
                print(f"   - Name: '{bookmark['name']}'")
                print(f"   - ID: '{bookmark['id']}'")
                print(f"   - Parent: {bookmark['parent'].tag if bookmark['parent'] is not None else 'None'}")
        
        # Buscar específicamente el que necesitamos
        print(f"\n🔍 BÚSQUEDA ESPECÍFICA:")
        print(f"Buscando 'main_logo'...")
        
        main_logo_bookmark = docx_doc.find_bookmark_by_name('main_logo')
        if main_logo_bookmark:
            print(f"✅ Encontrado main_logo: {main_logo_bookmark}")
        else:
            print(f"❌ No se encontró 'main_logo'")
            
        # Listar todos los nombres para referencia
        print(f"\n📝 LISTA DE NOMBRES DE BOOKMARKS:")
        bookmark_names = [b['name'] for b in bookmarks]
        for name in bookmark_names:
            print(f"   - '{name}'")
            
    except Exception as e:
        print(f"❌ Error analizando documento: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_bookmarks()
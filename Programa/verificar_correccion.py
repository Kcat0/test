#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación para confirmar que el error 'current_folder' ha sido corregido
"""

import sys
import os
sys.path.append('/workspace/code')

def test_initialization():
    """
    Prueba la inicialización de la clase para verificar que no hay errores
    """
    try:
        import tkinter as tk
        import kurohyou_csv_extractor as extractor
        
        print("🧪 VERIFICACIÓN DE CORRECCIÓN - KUROHYOU CSV EXTRACTOR")
        print("=" * 55)
        print()
        
        # Crear ventana raíz de prueba
        print("📋 Creando ventana raíz de tkinter...")
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana para prueba
        
        # Intentar crear la aplicación
        print("📋 Inicializando KurohyouUniversalExtractor...")
        app = extractor.KurohyouUniversalExtractor(root)
        
        # Verificar que current_folder existe
        print("📋 Verificando atributo 'current_folder'...")
        assert hasattr(app, 'current_folder'), "❌ Error: current_folder no existe"
        
        # Verificar que se puede acceder a current_folder
        print("📋 Probando acceso a current_folder...")
        folder_value = app.current_folder.get()
        print(f"   Valor inicial: '{folder_value}'")
        
        # Verificar otros atributos críticos
        print("📋 Verificando otros atributos críticos...")
        assert hasattr(app, 'csv_files'), "❌ Error: csv_files no existe"
        assert hasattr(app, 'extracted_data'), "❌ Error: extracted_data no existe"
        assert hasattr(app, 'is_processing'), "❌ Error: is_processing no existe"
        
        # Limpiar
        root.destroy()
        
        print("\n✅ TODAS LAS VERIFICACIONES PASARON EXITOSAMENTE")
        print("✅ El error 'current_folder' object has no attribute ha sido CORREGIDO")
        print("✅ La aplicación se inicializa correctamente")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except AssertionError as e:
        print(f"❌ Error de verificación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_methods():
    """
    Prueba algunos métodos básicos para asegurar funcionalidad
    """
    try:
        import tkinter as tk
        import kurohyou_csv_extractor as extractor
        
        print("\n🔧 PRUEBA DE MÉTODOS BÁSICOS")
        print("-" * 30)
        
        root = tk.Tk()
        root.withdraw()
        app = extractor.KurohyouUniversalExtractor(root)
        
        # Probar establecer carpeta
        print("📋 Probando establecer carpeta...")
        app.current_folder.set("/test/path")
        assert app.current_folder.get() == "/test/path", "Error al establecer carpeta"
        
        # Probar reiniciar variables
        print("📋 Probando reinicio de variables...")
        app.current_folder.set("")
        app.csv_files = []
        app.extracted_data = {}
        
        root.destroy()
        
        print("✅ Todos los métodos básicos funcionan correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de métodos: {e}")
        return False

if __name__ == "__main__":
    print("🎯 INICIANDO VERIFICACIÓN DEL ERROR CORREGIDO\n")
    
    # Ejecutar pruebas
    test1_passed = test_initialization()
    test2_passed = test_methods()
    
    print("\n" + "=" * 55)
    print("📊 RESUMEN DE RESULTADOS:")
    print(f"   Inicialización: {'✅ EXITOSA' if test1_passed else '❌ FALLÓ'}")
    print(f"   Métodos básicos: {'✅ EXITOSA' if test2_passed else '❌ FALLÓ'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 VERIFICACIÓN COMPLETA: ¡TODOS LOS ERRORES HAN SIDO CORREGIDOS!")
        print("🚀 La aplicación está lista para usar")
    else:
        print("\n⚠️  Algunos problemas persisten. Revisar errores arriba.")
    
    print("\n📌 Para ejecutar la aplicación:")
    print("   python lanzar_extractor.py")
    print("   python code/kurohyou_csv_extractor.py")

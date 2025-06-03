#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 LANZADOR DEL EXTRACTOR DE TEXTO JAPONÉS - KUROHYOU 1 PSP
==========================================================

Script de lanzamiento simple para iniciar el extractor con interfaz gráfica.
¡Simplemente ejecuta este archivo para comenzar!

Para usar: python lanzar_extractor.py
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """
    Verificar que la versión de Python sea compatible
    """
    if sys.version_info < (3, 6):
        print("❌ ERROR: Se requiere Python 3.6 o superior")
        print(f"   Versión actual: {sys.version}")
        print("   Por favor, actualiza Python e intenta nuevamente.")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - Compatible")
    return True

def check_extractor_files():
    """
    Verificar que los archivos del extractor estén presentes
    """
    current_dir = Path(__file__).parent
    extractor_path = current_dir / "code" / "kurohyou_csv_extractor.py"
    
    if not extractor_path.exists():
        print(f"❌ ERROR: No se encontró el archivo principal del extractor")
        print(f"   Buscado en: {extractor_path}")
        print("   Asegúrate de que todos los archivos estén en el lugar correcto.")
        return False, None
    
    print(f"✅ Extractor encontrado: {extractor_path}")
    return True, extractor_path

def show_intro():
    """
    Mostrar introducción del programa
    """
    print("🎮 EXTRACTOR DE TEXTO JAPONÉS - KUROHYOU 1 PSP")
    print("=" * 55)
    print("📋 Programa con interfaz gráfica para extraer texto japonés")
    print("   de archivos CSV de cinemáticas del juego Kurohyou 1 PSP")
    print()
    print("✨ CARACTERÍSTICAS:")
    print("   • Interfaz gráfica intuitiva")
    print("   • Búsqueda automática de archivos CSV")
    print("   • Visualización de texto japonés")
    print("   • Análisis de timing detallado")
    print("   • Exportación en múltiples formatos")
    print("   • Soporte completo para caracteres japoneses")
    print()
    print("🚀 Iniciando verificaciones...")
    print()

def launch_extractor(extractor_path):
    """
    Lanzar la aplicación principal
    """
    try:
        print("🖥️  Iniciando interfaz gráfica...")
        print("   (Si es la primera vez, puede tardar un momento en cargar)")
        print()
        
        # Intentar lanzar la aplicación
        result = subprocess.run([sys.executable, str(extractor_path)], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print("\n✅ Aplicación cerrada correctamente")
        else:
            print(f"\n⚠️  La aplicación se cerró con código: {result.returncode}")
            if result.stderr:
                print("📋 Error detallado:")
                print(f"   {result.stderr.strip()}")
                
                # Sugerir soluciones para errores comunes
                if "'current_folder'" in result.stderr:
                    print("\n💡 SOLUCIÓN SUGERIDA:")
                    print("   Este error ha sido corregido. Intenta ejecutar nuevamente.")
                elif "tkinter" in result.stderr.lower():
                    print("\n💡 SOLUCIÓN SUGERIDA:")
                    print("   Instala tkinter: sudo apt-get install python3-tk")
                elif "import" in result.stderr.lower():
                    print("\n💡 SOLUCIÓN SUGERIDA:")
                    print("   Verifica que Python esté correctamente instalado.")
            
    except FileNotFoundError:
        print("❌ ERROR: No se pudo ejecutar Python")
        print("   Asegúrate de que Python esté instalado correctamente.")
        return False
    except Exception as e:
        print(f"❌ ERROR inesperado al lanzar la aplicación: {e}")
        return False
    
    return True

def show_help():
    """
    Mostrar información de ayuda
    """
    print("\n📚 AYUDA E INFORMACIÓN ADICIONAL")
    print("-" * 40)
    print("📖 Manual completo:")
    print("   /workspace/docs/README_KurohyouExtractor.md")
    print()
    print("🧪 Para ejecutar las pruebas:")
    print("   python code/test_extractor.py")
    print()
    print("🎬 Para ver una demostración:")
    print("   python code/demo_extractor.py")
    print()
    print("📂 Archivos de salida se guardan en:")
    print("   /workspace/data/")
    print()
    print("❓ Si tienes problemas:")
    print("   1. Verifica que tengas Python 3.6 o superior")
    print("   2. Asegúrate de que los archivos CSV estén en formato UTF-8")
    print("   3. Revisa que las fuentes japonesas estén instaladas")
    print()

def main():
    """
    Función principal del lanzador
    """
    try:
        # Mostrar introducción
        show_intro()
        
        # Verificar Python
        if not check_python_version():
            return False
        
        # Verificar archivos del extractor
        files_ok, extractor_path = check_extractor_files()
        if not files_ok:
            return False
        
        print("✅ Todas las verificaciones pasaron correctamente")
        print()
        
        # Lanzar la aplicación
        success = launch_extractor(extractor_path)
        
        # Mostrar ayuda adicional
        show_help()
        
        return success
        
    except KeyboardInterrupt:
        print("\n⏹️  Lanzamiento cancelado por el usuario")
        return False
    except Exception as e:
        print(f"\n💥 Error fatal en el lanzador: {e}")
        return False

if __name__ == "__main__":
    print("🎯 LANZADOR DEL EXTRACTOR KUROHYOU 1 PSP")
    print("=" * 45)
    print()
    
    success = main()
    
    if success:
        print("\n🎉 ¡Gracias por usar el Extractor Kurohyou!")
    else:
        print("\n❌ Hubo problemas durante el lanzamiento")
        print("   Consulta los mensajes de error arriba para más detalles")
    
    input("\n📌 Presiona Enter para cerrar...")

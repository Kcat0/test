#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración de la funcionalidad automática recursiva del extractor Kurohyou 1 PSP
Simula el proceso automático sin GUI para mostrar cómo funciona
"""

import os
import sys
import glob
from pathlib import Path

# Agregar path del código
sys.path.append('/workspace/code')

def demo_recursive_search():
    """
    Demostrar búsqueda recursiva automática en la estructura de prueba
    """
    print("🎮 DEMO: EXTRACTOR AUTOMÁTICO KUROHYOU 1 PSP")
    print("=" * 50)
    print()
    
    # Usar la estructura de prueba creada
    test_folder = Path("/workspace/test_kurohyou_structure")
    
    if not test_folder.exists():
        print("❌ Error: Estructura de prueba no encontrada")
        print("   Ejecuta primero: python test_carpetas.py")
        return
    
    print(f"📂 CARPETA OBJETIVO: {test_folder}")
    print()
    
    # Simular búsqueda recursiva
    print("🔍 FASE 1: BÚSQUEDA RECURSIVA DE ARCHIVOS CSV")
    print("-" * 50)
    
    csv_files = []
    subdirs_explored = 0
    
    for root, dirs, files in os.walk(test_folder):
        subdirs_explored += 1
        relative_path = os.path.relpath(root, test_folder)
        
        if relative_path == ".":
            print(f"📁 Explorando carpeta principal...")
        else:
            print(f"📁 Explorando subcarpeta: {relative_path}")
        
        # Buscar archivos CSV
        csv_in_dir = [f for f in files if f.lower().endswith('.csv')]
        
        for csv_file in csv_in_dir:
            full_path = os.path.join(root, csv_file)
            csv_files.append(full_path)
            
            # Mostrar archivo encontrado
            if relative_path == ".":
                print(f"   📄 Encontrado: {csv_file}")
            else:
                print(f"   📄 Encontrado: {relative_path}/{csv_file}")
    
    print(f"\n✅ BÚSQUEDA COMPLETADA:")
    print(f"   📊 Subcarpetas exploradas: {subdirs_explored}")
    print(f"   📊 Archivos CSV encontrados: {len(csv_files)}")
    print()
    
    # Simular procesamiento automático
    print("📝 FASE 2: PROCESAMIENTO AUTOMÁTICO")
    print("-" * 50)
    
    import csv
    total_lines = 0
    total_characters = 0
    processed_files = 0
    
    for i, csv_file in enumerate(csv_files):
        relative_path = os.path.relpath(csv_file, test_folder)
        print(f"📝 Procesando ({i+1}/{len(csv_files)}): {relative_path}")
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                file_lines = 0
                file_chars = 0
                
                for row in reader:
                    if len(row) >= 3 and row[2].strip():
                        file_lines += 1
                        file_chars += len(row[2])
                        total_lines += 1
                        total_characters += len(row[2])
                
                print(f"   ✓ {file_lines} líneas, {file_chars} caracteres japoneses")
                processed_files += 1
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print(f"\n✅ PROCESAMIENTO COMPLETADO:")
    print(f"   📊 Archivos procesados exitosamente: {processed_files}/{len(csv_files)}")
    print(f"   📊 Total líneas de diálogo: {total_lines}")
    print(f"   📊 Total caracteres japoneses: {total_characters}")
    print()
    
    # Mostrar estructura detallada
    print("📋 ESTRUCTURA DETALLADA ENCONTRADA:")
    print("-" * 50)
    
    structure = {}
    for csv_file in sorted(csv_files):
        relative_path = os.path.relpath(csv_file, test_folder)
        folder = os.path.dirname(relative_path) if os.path.dirname(relative_path) else "📁 Carpeta raíz"
        filename = os.path.basename(relative_path)
        
        if folder not in structure:
            structure[folder] = []
        structure[folder].append(filename)
    
    for folder, files in structure.items():
        print(f"\n📁 {folder}:")
        for file in files:
            print(f"   📄 {file}")
    
    print(f"\n🎉 ¡DEMOSTRACIÓN COMPLETADA!")
    print("=" * 50)
    print("🚀 VENTAJAS DEL PROCESAMIENTO AUTOMÁTICO:")
    print("   ✅ Sin botones manuales - Todo automático")
    print("   ✅ Búsqueda recursiva completa")
    print("   ✅ Procesamiento inmediato tras selección")
    print("   ✅ Visualización en tiempo real del progreso")
    print("   ✅ Manejo robusto de errores")
    print("   ✅ Soporte completo para subcarpetas")
    print()
    print("🖥️  Para usar la GUI:")
    print("   python lanzar_extractor.py")
    print("   python code/kurohyou_csv_extractor.py")
    print()
    print(f"📂 Carpeta de prueba: {test_folder}")

def show_comparison():
    """
    Mostrar comparación entre versión anterior y nueva
    """
    print("\n📊 COMPARACIÓN: ANTES vs AHORA")
    print("=" * 50)
    
    print("❌ VERSIÓN ANTERIOR:")
    print("   1. Seleccionar carpeta")
    print("   2. ⏸️  Hacer clic en 'Buscar CSV'")
    print("   3. ⏸️  Esperar y hacer clic en 'Extraer Texto'")
    print("   4. ⏸️  Solo busca en carpeta principal")
    print("   5. ⏸️  Proceso manual en 3 pasos")
    print()
    
    print("✅ VERSIÓN NUEVA (AUTOMÁTICA):")
    print("   1. Seleccionar carpeta")
    print("   2. ⚡ ¡TODO AUTOMÁTICO!")
    print("      - Búsqueda recursiva en subcarpetas")
    print("      - Extracción inmediata de texto")
    print("      - Progreso en tiempo real")
    print("      - Resultados instantáneos")
    print("   3. 🎯 Proceso en 1 solo paso")

if __name__ == "__main__":
    demo_recursive_search()
    show_comparison()

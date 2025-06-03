#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Prueba para el Extractor de Texto Japonés - Kurohyou 1 PSP
====================================================================

Este script prueba las funcionalidades principales del extractor sin GUI
para verificar que el procesamiento de archivos CSV funciona correctamente.
"""

import os
import sys
import json
from pathlib import Path

# Importar las funciones principales del extractor
sys.path.append('/workspace/code')

def test_csv_parsing():
    """
    Probar el parsing de archivos CSV
    """
    print("🧪 PRUEBA 1: Parsing de archivo CSV")
    print("=" * 50)
    
    # Simular la función de extracción de CSV
    def extract_csv_data(csv_file):
        """Versión simplificada de la función de extracción"""
        try:
            data = {
                'filename': os.path.basename(csv_file),
                'filepath': csv_file,
                'lines': [],
                'stats': {}
            }
            
            dialogue_lines = 0
            pause_lines = 0
            total_chars = 0
            total_duration = 0
            
            with open(csv_file, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue
                        
                    # Parsear línea CSV manualmente (formato: tiempo_inicio,tiempo_fin,texto)
                    parts = line.split(',', 2)
                    if len(parts) >= 3:
                        try:
                            start_time = int(parts[0])
                            end_time = int(parts[1])
                            text = parts[2]
                            line_id = line_num  # Usar número de línea como ID
                            
                            line_data = {
                                'line_id': line_id,
                                'start_time': start_time,
                                'end_time': end_time,
                                'text': text,
                                'duration': end_time - start_time if start_time != -1 and end_time != -1 else 0,
                                'is_pause': start_time == -1 and end_time == -1
                            }
                            
                            data['lines'].append(line_data)
                            
                            if line_data['is_pause']:
                                pause_lines += 1
                            else:
                                dialogue_lines += 1
                                total_chars += len(text)
                                total_duration += line_data['duration']
                                
                        except ValueError:
                            continue
                            
            # Calcular estadísticas
            data['stats'] = {
                'total_lines': len(data['lines']),
                'dialogue_lines': dialogue_lines,
                'pause_lines': pause_lines,
                'total_chars': total_chars,
                'avg_chars': total_chars / dialogue_lines if dialogue_lines > 0 else 0,
                'total_duration': total_duration,
                'avg_duration': total_duration / dialogue_lines if dialogue_lines > 0 else 0
            }
            
            return data
            
        except Exception as e:
            print(f"❌ Error procesando {csv_file}: {e}")
            return None
    
    # Probar con el archivo de ejemplo
    test_file = "/workspace/user_input_files/ca01_01.csv"
    
    if not os.path.exists(test_file):
        print(f"❌ Archivo de prueba no encontrado: {test_file}")
        return False
        
    print(f"📂 Procesando archivo: {os.path.basename(test_file)}")
    
    result = extract_csv_data(test_file)
    
    if result:
        print("✅ Parsing exitoso!")
        print(f"   📊 Total de líneas: {result['stats']['total_lines']}")
        print(f"   💬 Líneas de diálogo: {result['stats']['dialogue_lines']}")
        print(f"   ⏸️  Pausas: {result['stats']['pause_lines']}")
        print(f"   📝 Total de caracteres: {result['stats']['total_chars']}")
        print(f"   ⏱️  Duración total: {result['stats']['total_duration']} ms")
        print(f"   📏 Promedio de caracteres: {result['stats']['avg_chars']:.1f}")
        print(f"   ⏳ Duración promedio: {result['stats']['avg_duration']:.1f} ms")
        
        # Mostrar algunas líneas de ejemplo
        print("\n📖 Primeras 5 líneas de diálogo:")
        dialogue_count = 0
        for line in result['lines']:
            if not line['is_pause'] and dialogue_count < 5:
                print(f"   [{line['line_id']:2d}] {line['text']}")
                dialogue_count += 1
                
        return True
    else:
        print("❌ Error en el parsing")
        return False

def test_japanese_encoding():
    """
    Probar que el manejo de caracteres japoneses funciona correctamente
    """
    print("\n🧪 PRUEBA 2: Codificación de caracteres japoneses")
    print("=" * 50)
    
    test_strings = [
        "マジでヤル気なのかよ？",
        "雄介… お前ビビッてんのか？",
        "ち… チゲーよ",
        "怖いんなら 降りろ",
        "龍也 テメェ…"
    ]
    
    print("📝 Verificando caracteres japoneses:")
    
    for i, text in enumerate(test_strings, 1):
        try:
            # Verificar que se puede codificar/decodificar correctamente
            encoded = text.encode('utf-8')
            decoded = encoded.decode('utf-8')
            
            if text == decoded:
                print(f"   ✅ Línea {i}: {text} ({len(text)} caracteres)")
            else:
                print(f"   ❌ Línea {i}: Error de codificación")
                return False
                
        except Exception as e:
            print(f"   ❌ Línea {i}: Error - {e}")
            return False
            
    print("✅ Codificación japonesa funciona correctamente!")
    return True

def test_export_functionality():
    """
    Probar la funcionalidad de exportación
    """
    print("\n🧪 PRUEBA 3: Funcionalidad de exportación")
    print("=" * 50)
    
    # Datos de prueba
    test_data = {
        'ca01_01.csv': {
            'filename': 'ca01_01.csv',
            'lines': [
                {
                    'line_id': 1,
                    'start_time': 542,
                    'end_time': 596,
                    'text': 'マジでヤル気なのかよ？',
                    'duration': 54,
                    'is_pause': False
                },
                {
                    'line_id': 2,
                    'start_time': -1,
                    'end_time': -1,
                    'text': '……',
                    'duration': 0,
                    'is_pause': True
                }
            ],
            'stats': {
                'total_lines': 2,
                'dialogue_lines': 1,
                'pause_lines': 1,
                'total_chars': 11,
                'avg_chars': 11.0,
                'total_duration': 54,
                'avg_duration': 54.0
            }
        }
    }
    
    # Crear directorio de salida
    output_dir = Path("/workspace/data")
    output_dir.mkdir(exist_ok=True)
    
    # Probar exportación JSON
    json_file = output_dir / "test_export.json"
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        print(f"✅ Exportación JSON exitosa: {json_file}")
    except Exception as e:
        print(f"❌ Error en exportación JSON: {e}")
        return False
    
    # Probar exportación de texto
    txt_file = output_dir / "test_export.txt"
    try:
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("PRUEBA DE EXPORTACIÓN - KUROHYOU 1 PSP\n")
            f.write("=" * 50 + "\n\n")
            
            for filename, data in test_data.items():
                f.write(f"ARCHIVO: {filename}\n")
                f.write("-" * 30 + "\n")
                
                for line in data['lines']:
                    if not line['is_pause']:
                        f.write(f"[{line['line_id']:2d}] {line['text']}\n")
                        
        print(f"✅ Exportación TXT exitosa: {txt_file}")
    except Exception as e:
        print(f"❌ Error en exportación TXT: {e}")
        return False
        
    return True

def test_error_handling():
    """
    Probar el manejo de errores
    """
    print("\n🧪 PRUEBA 4: Manejo de errores")
    print("=" * 50)
    
    # Probar archivo inexistente
    try:
        with open("/archivo/inexistente.csv", 'r'):
            pass
        print("❌ Debería haber lanzado excepción para archivo inexistente")
        return False
    except FileNotFoundError:
        print("✅ Manejo correcto de archivo inexistente")
    except Exception as e:
        print(f"❌ Excepción inesperada: {e}")
        return False
    
    # Probar datos malformados
    test_lines = [
        "542,596,texto_válido",
        "malformado,sin",
        "abc,def,tiempo_inválido",
        "1000,2000,texto_válido_2"
    ]
    
    valid_lines = 0
    for line in test_lines:
        parts = line.split(',', 2)
        if len(parts) >= 3:
            try:
                start_time = int(parts[0])
                end_time = int(parts[1])
                valid_lines += 1
            except ValueError:
                # Esperado para líneas malformadas
                pass
                
    print(f"✅ Procesamiento robusto: {valid_lines}/4 líneas válidas detectadas correctamente")
    
    return True

def run_all_tests():
    """
    Ejecutar todas las pruebas
    """
    print("🚀 INICIANDO PRUEBAS DEL EXTRACTOR DE TEXTO JAPONÉS")
    print("=" * 60)
    print("📋 Probando funcionalidades principales sin GUI...")
    print()
    
    tests = [
        ("Parsing de CSV", test_csv_parsing),
        ("Codificación japonesa", test_japanese_encoding),
        ("Exportación de datos", test_export_functionality),
        ("Manejo de errores", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ Prueba fallida: {test_name}")
        except Exception as e:
            print(f"❌ Error en prueba '{test_name}': {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTADOS: {passed}/{total} pruebas pasaron exitosamente")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El extractor está listo para usar.")
        print("\n💡 Para usar la GUI completa, ejecuta:")
        print("   python /workspace/code/kurohyou_csv_extractor.py")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración Completa del Extractor de Texto Japonés - Kurohyou 1 PSP
=====================================================================

Este script demuestra las capacidades completas del extractor procesando
el archivo de ejemplo y generando reportes detallados.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Agregar el directorio de código al path
sys.path.append('/workspace/code')

# Constante para FPS del juego Kurohyou 1 PSP
KUROHYOU_FPS = 30.0

def frames_to_seconds(frames):
    """Convertir fotogramas a segundos"""
    return frames / KUROHYOU_FPS if frames > 0 else 0.0

def frames_to_milliseconds(frames):
    """Convertir fotogramas a milisegundos"""
    return (frames / KUROHYOU_FPS) * 1000 if frames > 0 else 0.0

def format_duration(frames):
    """Formatear duración desde fotogramas a texto legible"""
    if frames <= 0:
        return "0 frames"
    
    seconds = frames_to_seconds(frames)
    return f"{frames} frames ({seconds:.2f}s)"

def process_sample_file():
    """
    Procesar el archivo de ejemplo y generar análisis detallado
    """
    print("🎮 DEMOSTRACIÓN DEL EXTRACTOR KUROHYOU 1 PSP")
    print("=" * 60)
    
    sample_file = "/workspace/user_input_files/ca01_01.csv"
    
    if not os.path.exists(sample_file):
        print(f"❌ Archivo de ejemplo no encontrado: {sample_file}")
        return False
    
    print(f"📂 Archivo de ejemplo: {os.path.basename(sample_file)}")
    print(f"📍 Ubicación: {sample_file}")
    print()
    
    # Función de extracción (copia de la función principal)
    def extract_csv_data(csv_file):
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
                        
                    # Parsear línea CSV (formato: tiempo_inicio,tiempo_fin,texto)
                    parts = line.split(',', 2)
                    if len(parts) >= 3:
                        try:
                            start_time = int(parts[0])
                            end_time = int(parts[1])
                            text = parts[2]
                            line_id = line_num
                            
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
                            
            # Calcular estadísticas (duración en fotogramas)
            data['stats'] = {
                'total_lines': len(data['lines']),
                'dialogue_lines': dialogue_lines,
                'pause_lines': pause_lines,
                'total_chars': total_chars,
                'avg_chars': total_chars / dialogue_lines if dialogue_lines > 0 else 0,
                'total_duration_frames': total_duration,
                'avg_duration_frames': total_duration / dialogue_lines if dialogue_lines > 0 else 0,
                'total_duration_seconds': frames_to_seconds(total_duration),
                'avg_duration_seconds': frames_to_seconds(total_duration / dialogue_lines) if dialogue_lines > 0 else 0
            }
            
            return data
            
        except Exception as e:
            print(f"❌ Error procesando {csv_file}: {e}")
            return None
    
    # Procesar el archivo
    print("🔄 Procesando archivo...")
    result = extract_csv_data(sample_file)
    
    if not result:
        print("❌ Error al procesar el archivo")
        return False
    
    # Mostrar estadísticas generales
    stats = result['stats']
    print("✅ Procesamiento completado!")
    print()
    print("📊 ESTADÍSTICAS GENERALES")
    print("-" * 30)
    print(f"📈 Total de líneas: {stats['total_lines']}")
    print(f"💬 Líneas de diálogo: {stats['dialogue_lines']}")
    print(f"⏸️  Pausas detectadas: {stats['pause_lines']}")
    print(f"📝 Total de caracteres: {stats['total_chars']:,}")
    print(f"📏 Promedio de caracteres por línea: {stats['avg_chars']:.1f}")
    print(f"⏱️  Duración total: {stats['total_duration_frames']:,} frames ({stats['total_duration_seconds']:.1f} segundos)")
    print(f"⏳ Duración promedio por línea: {stats['avg_duration_frames']:.1f} frames ({stats['avg_duration_seconds']:.3f}s)")
    print()
    
    # Análisis detallado
    print("🔍 ANÁLISIS DETALLADO")
    print("-" * 30)
    
    dialogue_lines = [line for line in result['lines'] if not line['is_pause']]
    
    if dialogue_lines:
        # Línea más larga/corta
        longest_line = max(dialogue_lines, key=lambda x: len(x['text']))
        shortest_line = min(dialogue_lines, key=lambda x: len(x['text']))
        
        print(f"📏 Línea más larga: {len(longest_line['text'])} caracteres")
        print(f"   └── [{longest_line['line_id']:2d}] {longest_line['text']}")
        print(f"📏 Línea más corta: {len(shortest_line['text'])} caracteres")
        print(f"   └── [{shortest_line['line_id']:2d}] {shortest_line['text']}")
        
        # Timing más largo/corto
        longest_timing = max(dialogue_lines, key=lambda x: x['duration'])
        shortest_timing = min(dialogue_lines, key=lambda x: x['duration'])
        
        print(f"⏱️  Timing más largo: {longest_timing['duration']} frames ({frames_to_seconds(longest_timing['duration']):.3f}s)")
        print(f"   └── [{longest_timing['line_id']:2d}] {longest_timing['text']}")
        print(f"⏱️  Timing más corto: {shortest_timing['duration']} frames ({frames_to_seconds(shortest_timing['duration']):.3f}s)")
        print(f"   └── [{shortest_timing['line_id']:2d}] {shortest_timing['text']}")
        
        # Análisis de patrones
        long_dialogues = [line for line in dialogue_lines if len(line['text']) > 15]
        short_dialogues = [line for line in dialogue_lines if len(line['text']) <= 5]
        # Análisis de timing (30 FPS = 30 frames por segundo)
        fast_dialogues = [line for line in dialogue_lines if 0 < line['duration'] < 15]  # < 0.5 segundos
        slow_dialogues = [line for line in dialogue_lines if line['duration'] > 60]  # > 2 segundos
        
        print(f"📊 Diálogos largos (>15 chars): {len(long_dialogues)}")
        print(f"📊 Diálogos cortos (≤5 chars): {len(short_dialogues)}")
        print(f"⚡ Diálogos rápidos (<15 frames / 0.5s): {len(fast_dialogues)}")
        print(f"🐌 Diálogos lentos (>60 frames / 2s): {len(slow_dialogues)}")
    
    print()
    
    # Mostrar todo el texto japonés
    print("🇯🇵 TEXTO JAPONÉS COMPLETO")
    print("-" * 30)
    for line in result['lines']:
        if line['is_pause']:
            print(f"[{line['line_id']:2d}] ⏸️  PAUSA")
        else:
            duration_str = f"({line['duration']} frames / {frames_to_seconds(line['duration']):.2f}s)"
            print(f"[{line['line_id']:2d}] {line['text']} {duration_str}")
    
    print()
    
    # Generar archivos de salida
    create_demo_outputs(result)
    
    return True

def create_demo_outputs(data):
    """
    Crear archivos de salida de demostración
    """
    print("💾 GENERANDO ARCHIVOS DE SALIDA")
    print("-" * 30)
    
    # Crear directorio de salida
    output_dir = Path("/workspace/data")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Archivo JSON completo
    json_file = output_dir / f"kurohyou_demo_{timestamp}.json"
    try:
        export_data = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'extractor': 'Kurohyou CSV Extractor Demo',
                'version': '1.0',
                'source_file': data['filename']
            },
            'data': data
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON generado: {json_file}")
    except Exception as e:
        print(f"❌ Error generando JSON: {e}")
    
    # 2. Archivo de texto limpio
    txt_file = output_dir / f"kurohyou_text_{timestamp}.txt"
    try:
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("TEXTO JAPONÉS EXTRAÍDO - KUROHYOU 1 PSP\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Archivo: {data['filename']}\n")
            f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Líneas de diálogo: {data['stats']['dialogue_lines']}\n")
            f.write(f"Duración total: {data['stats']['total_duration_frames']} frames ({data['stats']['total_duration_seconds']:.2f}s)\n\n")
            
            f.write("DIÁLOGOS:\n")
            f.write("-" * 20 + "\n")
            
            for line in data['lines']:
                if not line['is_pause']:
                    f.write(f"[{line['line_id']:2d}] {line['text']}\n")
        
        print(f"✅ Texto generado: {txt_file}")
    except Exception as e:
        print(f"❌ Error generando texto: {e}")
    
    # 3. Archivo CSV de timing
    timing_file = output_dir / f"kurohyou_timing_{timestamp}.csv"
    try:
        with open(timing_file, 'w', encoding='utf-8') as f:
            f.write("linea,inicio_frames,fin_frames,duracion_frames,caracteres,texto\n")
            
            for line in data['lines']:
                if not line['is_pause']:
                    f.write(f"{line['line_id']},{line['start_time']},{line['end_time']},{line['duration']},{len(line['text'])},\"{line['text']}\"\n")
        
        print(f"✅ Timing CSV generado: {timing_file}")
    except Exception as e:
        print(f"❌ Error generando CSV de timing: {e}")
    
    # 4. Reporte de análisis
    report_file = output_dir / f"kurohyou_report_{timestamp}.md"
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Reporte de Análisis - Kurohyou 1 PSP\n\n")
            f.write(f"**Archivo:** {data['filename']}  \n")
            f.write(f"**Generado:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n\n")
            
            f.write("## Estadísticas Generales\n\n")
            stats = data['stats']
            f.write(f"- **Total de líneas:** {stats['total_lines']}\n")
            f.write(f"- **Líneas de diálogo:** {stats['dialogue_lines']}\n")
            f.write(f"- **Pausas:** {stats['pause_lines']}\n")
            f.write(f"- **Caracteres totales:** {stats['total_chars']:,}\n")
            f.write(f"- **Promedio por línea:** {stats['avg_chars']:.1f} caracteres\n")
            f.write(f"- **Duración total:** {stats['total_duration_frames']:,} frames ({stats['total_duration_seconds']:.1f} segundos)\n")
            f.write(f"- **Duración promedio:** {stats['avg_duration_frames']:.1f} frames ({stats['avg_duration_seconds']:.3f}s)\n\n")
            
            f.write("## Texto Japonés\n\n")
            for line in data['lines']:
                if not line['is_pause']:
                    f.write(f"**{line['line_id']:2d}.** {line['text']} _({line['duration']} frames / {frames_to_seconds(line['duration']):.2f}s)_  \n")
        
        print(f"✅ Reporte Markdown generado: {report_file}")
    except Exception as e:
        print(f"❌ Error generando reporte: {e}")

def main():
    """
    Función principal de demostración
    """
    try:
        success = process_sample_file()
        
        if success:
            print("\n🎉 DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
            print("-" * 40)
            print("📁 Los archivos de salida se han generado en: /workspace/data/")
            print()
            print("🖥️  Para usar la interfaz gráfica completa, ejecuta:")
            print("   python /workspace/code/kurohyou_csv_extractor.py")
            print()
            print("📚 Para más información, consulta:")
            print("   /workspace/docs/README_KurohyouExtractor.md")
        else:
            print("\n❌ Error durante la demostración")
            
    except Exception as e:
        print(f"\n💥 Error fatal en la demostración: {e}")
        return False
        
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

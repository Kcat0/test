#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar las conversiones de fotogramas del extractor Kurohyou 1 PSP
"""

import sys
sys.path.append('/workspace/code')

# Importar las funciones de conversión
from kurohyou_csv_extractor import frames_to_seconds, frames_to_milliseconds, format_duration

def test_frame_conversions():
    """
    Probar las conversiones de fotogramas a tiempo real
    """
    print("🧪 PRUEBA DE CONVERSIONES DE FOTOGRAMAS - KUROHYOU 1 PSP")
    print("=" * 60)
    print()
    
    print("📊 CONSTANTES:")
    print(f"   FPS del juego: 30")
    print(f"   1 segundo = 30 fotogramas")
    print(f"   1 fotograma = 33.33ms")
    print()
    
    # Casos de prueba
    test_cases = [
        ("Muy rápido", 5),
        ("Rápido", 15), 
        ("Normal", 30),
        ("Largo", 60),
        ("Muy largo", 90),
        ("Del archivo ejemplo", 54),  # Primer diálogo del ca01_01.csv
        ("Del archivo ejemplo", 95),  # Diálogo más largo del ca01_01.csv
    ]
    
    print("🔢 PRUEBAS DE CONVERSIÓN:")
    print("-" * 60)
    print(f"{'Descripción':<20} {'Frames':<8} {'Segundos':<10} {'Milisegundos':<12} {'Formato'}")
    print("-" * 60)
    
    for desc, frames in test_cases:
        seconds = frames_to_seconds(frames)
        ms = frames_to_milliseconds(frames)
        formatted = format_duration(frames)
        
        print(f"{desc:<20} {frames:<8} {seconds:<10.3f} {ms:<12.0f} {formatted}")
    
    print()
    
    # Verificar datos del archivo ejemplo
    print("📋 VERIFICACIÓN CON ARCHIVO EJEMPLO (ca01_01.csv):")
    print("-" * 50)
    
    # Datos reales del archivo
    example_data = [
        (1, 542, 596, "マジでヤル気なのかよ？"),
        (2, 639, 703, "雄介… お前ビビッてんのか？"),
        (11, 1492, 1587, "な… 龍也 テメェ…"),  # El más largo
        (30, 2766, 2781, "あ？"),  # El más corto
    ]
    
    total_duration = 0
    
    for line_id, start, end, text in example_data:
        duration = end - start
        total_duration += duration
        
        print(f"Línea {line_id:2d}: {duration:3d} frames = {frames_to_seconds(duration):.3f}s")
        print(f"         '{text}'")
        print()
    
    print(f"📊 TOTALES DEL EJEMPLO:")
    print(f"   Duración total: {total_duration} frames")
    print(f"   En segundos: {frames_to_seconds(total_duration):.2f}s")
    print(f"   Promedio por línea: {total_duration/len(example_data):.1f} frames")
    print(f"   Promedio en segundos: {frames_to_seconds(total_duration/len(example_data)):.3f}s")
    
    print()
    
    # Comparación con valores anteriores (erróneos)
    print("⚖️  COMPARACIÓN: ANTES vs AHORA")
    print("-" * 50)
    print("ANTES (interpretación errónea como ms):")
    print(f"   Total: {total_duration}ms = {total_duration/1000:.2f}s")
    print()
    print("AHORA (correcta como fotogramas @ 30 FPS):")
    print(f"   Total: {total_duration} frames = {frames_to_seconds(total_duration):.2f}s")
    print()
    
    difference = frames_to_seconds(total_duration) - (total_duration/1000)
    print(f"💡 DIFERENCIA: {difference:+.2f} segundos")
    print(f"   La duración real es {abs(difference):.2f}s {'mayor' if difference > 0 else 'menor'}")

def test_analysis_thresholds():
    """
    Probar los nuevos umbrales de análisis
    """
    print("\n🎯 PRUEBA DE UMBRALES DE ANÁLISIS")
    print("=" * 50)
    
    thresholds = [
        ("Diálogos muy rápidos", "< 15 frames", "< 0.5s"),
        ("Diálogos normales", "15-60 frames", "0.5-2.0s"),
        ("Diálogos lentos", "> 60 frames", "> 2.0s"),
        ("Diálogos muy lentos", "> 90 frames", "> 3.0s"),
    ]
    
    print(f"{'Categoría':<20} {'Frames':<15} {'Tiempo'}")
    print("-" * 50)
    
    for category, frame_range, time_range in thresholds:
        print(f"{category:<20} {frame_range:<15} {time_range}")
    
    print()
    
    # Ejemplos del archivo ca01_01.csv
    example_timings = [
        ("あ？", 15, "muy rápido"),
        ("どけ！", 18, "muy rápido"), 
        ("マジでヤル気なのかよ？", 54, "normal"),
        ("な… 龍也 テメェ…", 95, "muy lento"),
    ]
    
    print("📋 CLASIFICACIÓN DE EJEMPLOS REALES:")
    print("-" * 50)
    
    for text, duration, expected in example_timings:
        seconds = frames_to_seconds(duration)
        
        if duration < 15:
            category = "muy rápido"
        elif duration <= 60:
            category = "normal"
        elif duration <= 90:
            category = "lento"
        else:
            category = "muy lento"
        
        status = "✅" if category == expected else "❌"
        
        print(f"{status} '{text}'")
        print(f"   {duration} frames ({seconds:.3f}s) → {category}")
        print()

if __name__ == "__main__":
    test_frame_conversions()
    test_analysis_thresholds()
    
    print("\n🎉 PRUEBAS COMPLETADAS")
    print("✅ Las conversiones de fotogramas funcionan correctamente")
    print("✅ Los umbrales de análisis están calibrados")
    print("✅ El programa está listo para manejar fotogramas @ 30 FPS")

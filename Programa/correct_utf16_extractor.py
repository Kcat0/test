#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extractor correcto de texto japonés UTF-16-LE para Kurohyou 1 PSP
=================================================================

Usando el método correcto proporcionado por el usuario para decodificar UTF-16-LE.
"""

import gzip
import os
import re
from typing import List, Tuple

def decode_utf16le_japanese(hex_bytes: str) -> str:
    """
    Función correcta para decodificar texto japonés UTF-16-LE
    Proporcionada por el usuario
    """
    try:
        raw = bytes.fromhex(hex_bytes)
        # decodifica en little-endian y quita caracteres NUL sobrantes
        return raw.decode('utf-16-le').rstrip('\x00')
    except:
        return ""

def find_japanese_text_sequences(data: bytes) -> List[Tuple[str, str, int]]:
    """
    Encontrar secuencias de texto japonés en los datos binarios
    
    Returns:
        Lista de tuplas (hex_string, decoded_text, offset)
    """
    japanese_texts = []
    
    # Buscar secuencias de bytes que podrían contener texto japonés
    i = 0
    while i < len(data) - 3:
        # Verificar si hay una secuencia que podría ser texto japonés
        # Buscar patrones que terminen en 00 00 (null terminator UTF-16)
        
        # Método 1: Buscar secuencias largas y probar decodificación
        for length in [20, 40, 60, 80, 100, 150, 200]:
            if i + length <= len(data):
                # Extraer secuencia de bytes
                sequence = data[i:i + length]
                hex_string = sequence.hex().upper()
                
                # Intentar decodificar
                decoded = decode_utf16le_japanese(hex_string)
                
                # Verificar si contiene caracteres japoneses
                if decoded and any('\u3040' <= char <= '\u309F' or  # Hiragana
                                  '\u30A0' <= char <= '\u30FF' or  # Katakana
                                  '\u4E00' <= char <= '\u9FAF'     # Kanji
                                  for char in decoded):
                    
                    # Limpiar el texto (quitar caracteres de control)
                    clean_text = ''.join(char for char in decoded 
                                       if char.isprintable() or 
                                       '\u3040' <= char <= '\u309F' or
                                       '\u30A0' <= char <= '\u30FF' or
                                       '\u4E00' <= char <= '\u9FAF')
                    
                    if clean_text.strip() and len(clean_text.strip()) >= 2:
                        japanese_texts.append((hex_string, clean_text.strip(), i))
                        i += length  # Saltar esta secuencia
                        break
        else:
            i += 2  # Avanzar por pares de bytes (UTF-16)
    
    return japanese_texts

def find_japanese_by_null_terminators(data: bytes) -> List[Tuple[str, str, int]]:
    """
    Método alternativo: buscar texto japonés entre terminadores null
    """
    japanese_texts = []
    
    # Buscar secuencias entre 00 00 (null terminators UTF-16)
    null_pattern = b'\x00\x00'
    positions = []
    
    # Encontrar todas las posiciones de null terminators
    start = 0
    while True:
        pos = data.find(null_pattern, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 2
    
    # Examinar secuencias entre terminadores
    for i in range(len(positions) - 1):
        start_pos = positions[i] + 2
        end_pos = positions[i + 1]
        
        if end_pos - start_pos > 4:  # Secuencia mínima útil
            sequence = data[start_pos:end_pos]
            hex_string = sequence.hex().upper()
            
            decoded = decode_utf16le_japanese(hex_string)
            
            if decoded and any('\u3040' <= char <= '\u309F' or
                             '\u30A0' <= char <= '\u30FF' or
                             '\u4E00' <= char <= '\u9FAF'
                             for char in decoded):
                
                clean_text = ''.join(char for char in decoded 
                                   if char.isprintable() or 
                                   '\u3040' <= char <= '\u309F' or
                                   '\u30A0' <= char <= '\u30FF' or
                                   '\u4E00' <= char <= '\u9FAF')
                
                if clean_text.strip() and len(clean_text.strip()) >= 1:
                    japanese_texts.append((hex_string, clean_text.strip(), start_pos))
    
    return japanese_texts

def extract_japanese_from_pack_correct(pack_file_path: str):
    """
    Extraer texto japonés usando el método correcto de decodificación
    """
    print("🎯 EXTRACTOR CORRECTO UTF-16-LE - KUROHYOU 1 PSP")
    print("=" * 55)
    print()
    
    # Descomprimir archivo
    with gzip.open(pack_file_path, 'rb') as f:
        data = f.read()
    
    print(f"📂 Archivo: {os.path.basename(pack_file_path)}")
    print(f"📊 Tamaño descomprimido: {len(data):,} bytes")
    print()
    
    # Método 1: Búsqueda por secuencias
    print("🔍 Método 1: Búsqueda por secuencias largas")
    sequences = find_japanese_text_sequences(data)
    print(f"   Textos encontrados: {len(sequences)}")
    
    # Método 2: Búsqueda por terminadores null
    print("🔍 Método 2: Búsqueda por terminadores null")
    null_texts = find_japanese_by_null_terminators(data)
    print(f"   Textos encontrados: {len(null_texts)}")
    
    # Combinar y eliminar duplicados
    all_texts = sequences + null_texts
    unique_texts = []
    seen_texts = set()
    
    for hex_str, decoded, offset in all_texts:
        if decoded not in seen_texts and len(decoded) >= 1:
            unique_texts.append((hex_str, decoded, offset))
            seen_texts.add(decoded)
    
    print(f"📝 Textos únicos japoneses: {len(unique_texts)}")
    print()
    
    # Mostrar ejemplos
    print("💬 EJEMPLOS DE TEXTO JAPONÉS EXTRAÍDO:")
    print("-" * 45)
    
    for i, (hex_str, decoded, offset) in enumerate(unique_texts[:20]):
        print(f"[{i+1:2d}] Offset: {offset:6d} | Hex: {hex_str[:30]}{'...' if len(hex_str) > 30 else ''}")
        print(f"     Japonés: {decoded}")
        print()
    
    return unique_texts

def test_with_user_example():
    """
    Probar con el ejemplo proporcionado por el usuario
    """
    print("🧪 PRUEBA CON EJEMPLO DEL USUARIO:")
    print("-" * 35)
    
    hexstr = "8D9F5F4E0000000008FF4F3063302620262055637E30633061307E3063305F3001FF09FF00000000"
    decoded = decode_utf16le_japanese(hexstr)
    
    print(f"Hex: {hexstr}")
    print(f"Japonés: {decoded}")
    print(f"Longitud: {len(decoded)} caracteres")
    print()

def save_extracted_japanese(texts: List[Tuple[str, str, int]], output_file: str):
    """
    Guardar textos japoneses extraídos
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("TEXTO JAPONÉS EXTRAÍDO - KUROHYOU 1 PSP (MÉTODO CORRECTO)\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"📊 ESTADÍSTICAS:\n")
        f.write(f"Total textos japoneses: {len(texts)}\n")
        
        # Analizar longitudes
        lengths = [len(text) for _, text, _ in texts]
        if lengths:
            f.write(f"Promedio de caracteres: {sum(lengths) / len(lengths):.1f}\n")
            f.write(f"Texto más largo: {max(lengths)} caracteres\n")
            f.write(f"Texto más corto: {min(lengths)} caracteres\n")
        
        f.write(f"\n💬 DIÁLOGOS JAPONESES:\n")
        f.write("-" * 30 + "\n")
        
        for i, (hex_str, decoded, offset) in enumerate(texts, 1):
            f.write(f"\n[{i:3d}] OFFSET: {offset:6d}\n")
            f.write(f"     HEX: {hex_str}\n")
            f.write(f"     JAPONÉS: {decoded}\n")

if __name__ == "__main__":
    pack_file = "/workspace/user_input_files/main_seq01.pack"
    
    # Probar primero con el ejemplo del usuario
    test_with_user_example()
    
    if os.path.exists(pack_file):
        print("🎯 INICIANDO EXTRACCIÓN CON MÉTODO CORRECTO")
        print()
        
        # Extraer texto japonés
        japanese_texts = extract_japanese_from_pack_correct(pack_file)
        
        # Guardar resultados
        output_file = "/workspace/japanese_correct_extraction.txt"
        save_extracted_japanese(japanese_texts, output_file)
        
        print(f"📄 Resultados guardados en: {output_file}")
        print(f"📊 Total textos japoneses: {len(japanese_texts)}")
        
        print("\n🎯 EXTRACCIÓN COMPLETADA")
        print("✅ Método correcto de decodificación UTF-16-LE aplicado")
        print("✅ Texto japonés auténtico extraído")
        print("✅ Listo para integración en programa principal")
        
    else:
        print(f"❌ Archivo no encontrado: {pack_file}")

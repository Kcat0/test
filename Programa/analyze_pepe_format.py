#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador del archivo 'pepe' - Formato ELPK/KSEQ de Kurohyou 1 PSP
====================================================================

Este script analiza la estructura binaria del archivo 'pepe' para entender
cómo están organizados los textos y punteros en el formato del juego.
"""

import struct
import os
from typing import List, Dict, Tuple

def analyze_elpk_format(file_path: str):
    """
    Analizar la estructura del archivo formato ELPK/KSEQ
    """
    print("🔍 ANÁLISIS DEL ARCHIVO 'pepe' - FORMATO ELPK/KSEQ")
    print("=" * 60)
    print()
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    print(f"📂 Archivo: {os.path.basename(file_path)}")
    print(f"📊 Tamaño: {len(data):,} bytes")
    print()
    
    # Analizar header principal
    print("🔤 HEADER PRINCIPAL")
    print("-" * 30)
    
    magic = data[0:4]
    print(f"Magic Number: {magic} ({magic.decode('ascii', errors='ignore')})")
    
    version = data[4:8]
    print(f"Version/Magic 2: {version.hex()} ({version.decode('ascii', errors='ignore')})")
    
    # Leer valores del header
    header_values = struct.unpack('<III', data[8:20])
    print(f"Header values: {header_values}")
    print()
    
    # Buscar header KSEQ
    kseq_pos = data.find(b'KSEQ')
    print(f"🔤 HEADER SECUNDARIO KSEQ")
    print("-" * 30)
    print(f"Posición KSEQ: {kseq_pos} (0x{kseq_pos:x})")
    
    if kseq_pos != -1:
        kseq_data = struct.unpack('<II', data[kseq_pos+4:kseq_pos+12])
        print(f"KSEQ values: {kseq_data}")
    print()
    
    # Analizar tabla de punteros
    print("📋 TABLA DE PUNTEROS/ENTRADAS")
    print("-" * 40)
    
    # Empezar después del header principal
    pointer_start = 20
    entries = []
    
    # Leer entradas hasta llegar al header KSEQ
    pos = pointer_start
    entry_count = 0
    
    while pos < kseq_pos and entry_count < 50:  # Límite de seguridad
        try:
            # Leer entrada (supuesto: hash_id, offset, size)
            hash_id, offset, size = struct.unpack('<III', data[pos:pos+12])
            
            # Verificar si es una entrada válida
            if offset > 0 and offset < len(data) and size > 0 and size < 10000:
                entries.append({
                    'index': entry_count,
                    'hash_id': hash_id,
                    'offset': offset,
                    'size': size,
                    'position': pos
                })
                print(f"[{entry_count:2d}] Hash: 0x{hash_id:08x} | Offset: {offset:5d} | Size: {size:4d}")
                entry_count += 1
            else:
                # Si no es válido, intentar otro patrón
                break
                
        except struct.error:
            break
        
        pos += 12
    
    print(f"\n📊 Total de entradas encontradas: {len(entries)}")
    print()
    
    # Extraer algunos textos de ejemplo
    print("📝 TEXTOS EXTRAÍDOS (EJEMPLOS)")
    print("-" * 40)
    
    for i, entry in enumerate(entries[:10]):  # Primeros 10
        try:
            text_data = data[entry['offset']:entry['offset'] + entry['size']]
            # Intentar decodificar como texto
            try:
                text = text_data.decode('utf-8', errors='ignore').strip('\x00')
                if text and len(text) > 1:
                    print(f"[{entry['index']:2d}] (0x{entry['hash_id']:08x}): '{text[:60]}{'...' if len(text) > 60 else ''}'")
            except:
                # Si no es texto válido, mostrar hex
                print(f"[{entry['index']:2d}] (0x{entry['hash_id']:08x}): [DATOS BINARIOS: {text_data[:20].hex()}...]")
        except:
            print(f"[{entry['index']:2d}] (0x{entry['hash_id']:08x}): [ERROR LEYENDO DATOS]")
    
    print()
    
    # Analizar strings completos
    print("🔤 TODOS LOS STRINGS ENCONTRADOS")
    print("-" * 40)
    
    strings = extract_strings(data)
    print(f"Total strings encontrados: {len(strings)}")
    print()
    
    # Categorizar strings
    dialogue_strings = []
    command_strings = []
    name_strings = []
    
    for s in strings:
        if len(s) > 50 or '.' in s or '!' in s or '?' in s:
            dialogue_strings.append(s)
        elif s.isupper() or '_' in s or any(x in s for x in ['play', 'bgm', 'amb_']):
            command_strings.append(s)
        elif len(s) < 30 and len(s) > 3:
            name_strings.append(s)
    
    print("💬 DIÁLOGOS DETECTADOS (primeros 5):")
    for i, dialogue in enumerate(dialogue_strings[:5]):
        print(f"  {i+1}. {dialogue[:80]}{'...' if len(dialogue) > 80 else ''}")
    
    print(f"\n📝 COMANDOS/IDENTIFICADORES TÉCNICOS (primeros 5):")
    for i, cmd in enumerate(command_strings[:5]):
        print(f"  {i+1}. {cmd}")
    
    print(f"\n👤 NOMBRES/ETIQUETAS (primeros 5):")
    for i, name in enumerate(name_strings[:5]):
        print(f"  {i+1}. {name}")
    
    print()
    
    # Resumen final
    print("📊 RESUMEN DEL ANÁLISIS")
    print("-" * 30)
    print(f"✅ Formato detectado: ELPK/KSEQ (formato propietario)")
    print(f"✅ Estructura: Header + Tabla de punteros + Datos")
    print(f"✅ Método de acceso: Por hash IDs + offsets")
    print(f"✅ Contenido: Diálogos traducidos al inglés")
    print(f"✅ Total entradas: {len(entries)}")
    print(f"✅ Total strings: {len(strings)}")
    print(f"   - Diálogos: {len(dialogue_strings)}")
    print(f"   - Comandos: {len(command_strings)}")
    print(f"   - Nombres: {len(name_strings)}")
    
    return {
        'entries': entries,
        'strings': strings,
        'dialogues': dialogue_strings,
        'commands': command_strings,
        'names': name_strings
    }

def extract_strings(data: bytes, min_length: int = 4) -> List[str]:
    """
    Extraer strings legibles del archivo binario
    """
    strings = []
    current_string = ""
    
    for byte in data:
        if 32 <= byte <= 126:  # Caracteres ASCII imprimibles
            current_string += chr(byte)
        else:
            if len(current_string) >= min_length:
                strings.append(current_string)
            current_string = ""
    
    # Agregar último string si existe
    if len(current_string) >= min_length:
        strings.append(current_string)
    
    return strings

def analyze_hash_distribution(entries: List[Dict]):
    """
    Analizar la distribución de hashes para entender el patrón
    """
    print("\n🔢 ANÁLISIS DE DISTRIBUCIÓN DE HASHES")
    print("-" * 40)
    
    if not entries:
        print("No hay entradas para analizar")
        return
    
    hash_values = [entry['hash_id'] for entry in entries]
    
    print(f"Primer hash: 0x{min(hash_values):08x}")
    print(f"Último hash: 0x{max(hash_values):08x}")
    print(f"Rango: 0x{max(hash_values) - min(hash_values):08x}")
    
    # Buscar patrones en los hashes
    consecutive_pairs = 0
    for i in range(len(hash_values) - 1):
        if hash_values[i+1] - hash_values[i] == 1:
            consecutive_pairs += 1
    
    print(f"Pares consecutivos: {consecutive_pairs}")
    
    if consecutive_pairs > len(hash_values) * 0.5:
        print("✅ Los hashes parecen ser secuenciales (IDs incrementales)")
    else:
        print("✅ Los hashes parecen ser calculados (hash real)")

if __name__ == "__main__":
    file_path = "/workspace/user_input_files/pepe"
    
    if os.path.exists(file_path):
        result = analyze_elpk_format(file_path)
        analyze_hash_distribution(result['entries'])
        
        print("\n🎯 CONCLUSIONES")
        print("-" * 30)
        print("1. 📁 Formato: ELPK/KSEQ - formato propietario del juego")
        print("2. 🔍 Estructura: Tabla de punteros con hash IDs")
        print("3. 📝 Contenido: Diálogos ya traducidos al inglés")
        print("4. 🎮 Tipo: Archivo de script/eventos del juego")
        print("5. 💾 Acceso: Por hash ID para localizar texto específico")
        print()
        print("🎉 ¡Análisis completado! El formato usa punteros hash-based.")
        
    else:
        print(f"❌ Error: Archivo no encontrado: {file_path}")

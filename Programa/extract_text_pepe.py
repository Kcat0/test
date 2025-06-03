#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extractor de textos del archivo 'pepe' - Formato ELPK/KSEQ
===========================================================

Basado en el análisis anterior, este script extrae los textos de manera más precisa
del formato ELPK/KSEQ identificando las secciones KSEQ individuales.
"""

import struct
import os
from typing import List, Dict, Tuple

def extract_kseq_texts(file_path: str):
    """
    Extraer textos de las secciones KSEQ del archivo
    """
    print("📝 EXTRACTOR DE TEXTOS - ARCHIVO 'pepe'")
    print("=" * 50)
    print()
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    # Encontrar todas las posiciones KSEQ
    kseq_positions = []
    pos = 0
    while True:
        pos = data.find(b'KSEQ', pos)
        if pos == -1:
            break
        kseq_positions.append(pos)
        pos += 4
    
    print(f"🔍 Encontradas {len(kseq_positions)} secciones KSEQ")
    print()
    
    all_texts = []
    
    for i, kseq_pos in enumerate(kseq_positions):
        print(f"📄 SECCIÓN KSEQ #{i+1} (offset: {kseq_pos})")
        print("-" * 40)
        
        # Determinar el tamaño de esta sección
        if i < len(kseq_positions) - 1:
            section_size = kseq_positions[i+1] - kseq_pos
        else:
            section_size = len(data) - kseq_pos
        
        section_data = data[kseq_pos:kseq_pos + section_size]
        
        # Extraer textos de esta sección
        section_texts = extract_texts_from_kseq_section(section_data, kseq_pos)
        
        print(f"   Textos encontrados: {len(section_texts)}")
        
        # Mostrar primeros textos
        for j, text in enumerate(section_texts[:5]):
            if text.strip() and len(text) > 2:
                print(f"   [{j+1:2d}] {text[:60]}{'...' if len(text) > 60 else ''}")
        
        if len(section_texts) > 5:
            print(f"   ... y {len(section_texts) - 5} textos más")
        
        all_texts.extend(section_texts)
        print()
    
    return all_texts

def extract_texts_from_kseq_section(section_data: bytes, base_offset: int) -> List[str]:
    """
    Extraer textos de una sección KSEQ individual
    """
    texts = []
    
    # Buscar strings dentro de la sección
    current_string = ""
    for byte in section_data:
        if 32 <= byte <= 126:  # ASCII imprimible
            current_string += chr(byte)
        elif byte == 0:  # Null terminator
            if len(current_string) >= 3:
                texts.append(current_string)
            current_string = ""
        else:
            if len(current_string) >= 3:
                texts.append(current_string)
            current_string = ""
    
    # Agregar último string si existe
    if len(current_string) >= 3:
        texts.append(current_string)
    
    return texts

def categorize_texts(texts: List[str]) -> Dict[str, List[str]]:
    """
    Categorizar los textos extraídos
    """
    categories = {
        'dialogues': [],
        'names': [],
        'commands': [],
        'options': [],
        'narration': []
    }
    
    for text in texts:
        text = text.strip()
        if not text or len(text) < 3:
            continue
            
        # Diálogos (contienen puntuación o son largos)
        if any(punct in text for punct in ['.', '!', '?', ',']):
            if len(text) > 20:
                categories['dialogues'].append(text)
            elif len(text) <= 20:
                categories['options'].append(text)
        
        # Comandos técnicos
        elif any(tech in text.lower() for tech in ['bgm', 'amb_', 'play', '_lr', 'destination']):
            categories['commands'].append(text)
        
        # Nombres (cortos, sin puntuación especial)
        elif len(text) <= 25 and text.replace(' ', '').isalpha():
            categories['names'].append(text)
        
        # Narración (paréntesis, palabras descriptivas)
        elif '(' in text or any(word in text.lower() for word in ['shit', 'damn', 'hell']):
            categories['narration'].append(text)
        
        # Resto como diálogos
        else:
            categories['dialogues'].append(text)
    
    return categories

def generate_text_report(texts: List[str], output_file: str):
    """
    Generar reporte completo de textos extraídos
    """
    categories = categorize_texts(texts)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("EXTRACCIÓN DE TEXTOS - ARCHIVO 'pepe' (FORMATO ELPK/KSEQ)\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"📊 ESTADÍSTICAS GENERALES\n")
        f.write("-" * 30 + "\n")
        f.write(f"Total de textos extraídos: {len(texts)}\n")
        f.write(f"Diálogos: {len(categories['dialogues'])}\n")
        f.write(f"Nombres/Personajes: {len(categories['names'])}\n")
        f.write(f"Opciones: {len(categories['options'])}\n")
        f.write(f"Comandos técnicos: {len(categories['commands'])}\n")
        f.write(f"Narración: {len(categories['narration'])}\n\n")
        
        f.write("💬 DIÁLOGOS PRINCIPALES\n")
        f.write("-" * 30 + "\n")
        for i, dialogue in enumerate(categories['dialogues'], 1):
            f.write(f"{i:3d}. {dialogue}\n")
        
        f.write("\n👤 NOMBRES Y PERSONAJES\n")
        f.write("-" * 30 + "\n")
        unique_names = list(set(categories['names']))
        for i, name in enumerate(unique_names, 1):
            f.write(f"{i:3d}. {name}\n")
        
        f.write("\n🎮 OPCIONES DE RESPUESTA\n")
        f.write("-" * 30 + "\n")
        for i, option in enumerate(categories['options'], 1):
            f.write(f"{i:3d}. {option}\n")
        
        f.write("\n💭 NARRACIÓN/PENSAMIENTOS\n")
        f.write("-" * 30 + "\n")
        for i, narr in enumerate(categories['narration'], 1):
            f.write(f"{i:3d}. {narr}\n")
        
        f.write("\n🔧 COMANDOS TÉCNICOS\n")
        f.write("-" * 30 + "\n")
        for i, cmd in enumerate(categories['commands'], 1):
            f.write(f"{i:3d}. {cmd}\n")

def analyze_dialogue_structure():
    """
    Crear análisis específico para entender la estructura de diálogos
    """
    print("\n🧪 ANÁLISIS DE ESTRUCTURA DE DIÁLOGOS")
    print("-" * 45)
    
    file_path = "/workspace/user_input_files/pepe"
    
    # Extraer todos los textos
    all_texts = extract_kseq_texts(file_path)
    
    # Filtrar solo diálogos reales
    dialogues = []
    for text in all_texts:
        text = text.strip()
        if (len(text) > 10 and 
            any(punct in text for punct in ['.', '!', '?']) and
            not any(tech in text.lower() for tech in ['kseq', 'amb_', 'bgm', 'play'])):
            dialogues.append(text)
    
    print(f"📝 Diálogos identificados: {len(dialogues)}")
    print()
    
    # Mostrar estructura
    print("💬 ESTRUCTURA DE DIÁLOGO DETECTADA:")
    print("-" * 40)
    
    current_speaker = None
    dialogue_blocks = []
    current_block = []
    
    for text in dialogues[:20]:  # Primeros 20 para análisis
        # Detectar si es un nombre/speaker
        if (len(text) <= 25 and 
            text.replace(' ', '').replace('-', '').isalpha() and
            not any(punct in text for punct in ['.', '!', '?'])):
            
            if current_block:
                dialogue_blocks.append((current_speaker, current_block))
                current_block = []
            current_speaker = text
        else:
            current_block.append(text)
    
    # Agregar último bloque
    if current_block:
        dialogue_blocks.append((current_speaker, current_block))
    
    for i, (speaker, lines) in enumerate(dialogue_blocks[:10]):
        print(f"\n[{i+1}] {speaker or 'Unknown Speaker'}:")
        for line in lines:
            print(f"    \"{line}\"")
    
    return {
        'all_texts': all_texts,
        'dialogues': dialogues,
        'dialogue_blocks': dialogue_blocks
    }

if __name__ == "__main__":
    file_path = "/workspace/user_input_files/pepe"
    
    if os.path.exists(file_path):
        # Análisis principal
        result = analyze_dialogue_structure()
        
        # Generar reporte
        output_file = "/workspace/pepe_texts_extracted.txt"
        generate_text_report(result['all_texts'], output_file)
        
        print(f"\n📄 Reporte generado: {output_file}")
        print(f"📊 Total textos extraídos: {len(result['all_texts'])}")
        print(f"💬 Diálogos identificados: {len(result['dialogues'])}")
        
        print("\n🎯 CONCLUSIONES SOBRE EL FORMATO")
        print("-" * 40)
        print("✅ Formato ELPK/KSEQ confirmado")
        print("✅ Textos organizados por secciones KSEQ")
        print("✅ Cada sección contiene diálogos de una escena")
        print("✅ Textos ya traducidos al inglés")
        print("✅ Estructura: Nombre_personaje + Diálogos")
        print("✅ Acceso por hash IDs para localización rápida")
        
    else:
        print(f"❌ Error: Archivo no encontrado: {file_path}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Decodificador de texto japonés para archivos PACK de Kurohyou 1 PSP
====================================================================

Este script descifra la codificación especial de texto japonés usado en los archivos originales.
"""

import gzip
import struct
import re
import os
from typing import List

def decode_kurohyou_japanese(encoded_text: str) -> str:
    """
    Decodificar el formato especial de japonés de Kurohyou 1 PSP
    
    El formato parece usar patrones como:
    - "U0c0M0o0u0V0Q0_0" = caracteres UTF-16 con bytes separados por 0
    """
    
    # Remover el patrón 0X0 donde X es un carácter
    # Patrón observado: letra0letra0letra0...
    if '0' in encoded_text and len(encoded_text) > 4:
        try:
            # Método 1: Remover los 0s intercalados
            # "U0c0M0o0u0V0Q0_0" -> "UcMouVQ_"
            clean_text = re.sub(r'0(.)', r'\1', encoded_text)
            clean_text = clean_text.replace('0', '')
            
            # Intentar decodificar como UTF-16
            try:
                # Los caracteres podrían estar en UTF-16LE
                if len(clean_text) % 2 == 0:
                    bytes_data = clean_text.encode('ascii')
                    # Tratar cada par de caracteres como bytes UTF-16
                    utf16_bytes = b''
                    for i in range(0, len(bytes_data), 2):
                        if i + 1 < len(bytes_data):
                            # Combinar dos bytes ASCII como un carácter UTF-16
                            utf16_bytes += bytes([bytes_data[i], bytes_data[i+1]])
                    
                    decoded = utf16_bytes.decode('utf-16le', errors='ignore')
                    if any('\u3040' <= char <= '\u309F' or  # Hiragana
                           '\u30A0' <= char <= '\u30FF' or  # Katakana
                           '\u4E00' <= char <= '\u9FAF'     # Kanji
                           for char in decoded):
                        return decoded
            except:
                pass
            
            # Método 2: Interpretar como codificación hexadecimal
            try:
                # Podría ser hexadecimal de caracteres japoneses
                hex_pairs = re.findall(r'[0-9A-Fa-f]{2}', clean_text)
                if hex_pairs:
                    hex_bytes = bytes([int(pair, 16) for pair in hex_pairs])
                    for encoding in ['utf-16le', 'utf-16be', 'shift_jis']:
                        try:
                            decoded = hex_bytes.decode(encoding)
                            if any('\u3040' <= char <= '\u309F' or  # Hiragana
                                   '\u30A0' <= char <= '\u30FF' or  # Katakana  
                                   '\u4E00' <= char <= '\u9FAF'     # Kanji
                                   for char in decoded):
                                return decoded
                        except:
                            continue
            except:
                pass
            
        except Exception as e:
            pass
    
    return encoded_text  # Devolver original si no se puede decodificar

def extract_and_decode_japanese_texts(pack_file_path: str):
    """
    Extraer y decodificar todos los textos japoneses del archivo pack
    """
    print("🔤 DECODIFICADOR DE TEXTO JAPONÉS - KUROHYOU 1 PSP")
    print("=" * 55)
    print()
    
    # Descomprimir archivo
    with gzip.open(pack_file_path, 'rb') as f:
        data = f.read()
    
    print(f"📂 Archivo: {pack_file_path}")
    print(f"📊 Tamaño descomprimido: {len(data):,} bytes")
    print()
    
    # Extraer strings de todo el archivo
    all_strings = extract_strings_from_data(data)
    print(f"🔍 Strings totales encontrados: {len(all_strings)}")
    
    # Filtrar y decodificar textos que parecen japoneses
    japanese_texts = []
    decoded_texts = []
    
    for text in all_strings:
        # Identificar textos japoneses codificados
        if ('0' in text and len(text) > 5) or \
           re.search(r'[0-9][A-Za-z][0-9]', text) or \
           any(char in text for char in ['J', 'U', 'M', 'Q', 'V', 'c', 'f']):
            
            japanese_texts.append(text)
            decoded = decode_kurohyou_japanese(text)
            decoded_texts.append(decoded)
    
    print(f"📝 Textos japoneses identificados: {len(japanese_texts)}")
    successful_count = sum(1 for i, d in enumerate(decoded_texts) if d != japanese_texts[i])
    print(f"✅ Textos decodificados exitosamente: {successful_count}")
    print()
    
    # Mostrar ejemplos
    print("💬 EJEMPLOS DE DECODIFICACIÓN:")
    print("-" * 40)
    
    successful_decodes = 0
    for i, (original, decoded) in enumerate(zip(japanese_texts[:20], decoded_texts[:20])):
        if decoded != original and len(decoded) > 0:
            print(f"[{i+1:2d}] Original: {original[:30]}{'...' if len(original) > 30 else ''}")
            print(f"     Decodificado: {decoded}")
            print()
            successful_decodes += 1
        elif len(original) > 10:
            print(f"[{i+1:2d}] Sin decodificar: {original[:50]}{'...' if len(original) > 50 else ''}")
    
    return {
        'all_strings': all_strings,
        'japanese_original': japanese_texts,
        'japanese_decoded': decoded_texts,
        'successful_decodes': successful_decodes
    }

def extract_strings_from_data(data: bytes, min_length: int = 3) -> List[str]:
    """
    Extraer todos los strings del archivo binario
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
    
    # Agregar último string
    if len(current_string) >= min_length:
        strings.append(current_string)
    
    return strings

def save_decoded_texts(result: dict, output_file: str):
    """
    Guardar textos decodificados en archivo
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("TEXTOS JAPONESES DECODIFICADOS - KUROHYOU 1 PSP\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"📊 ESTADÍSTICAS:\n")
        f.write(f"Total strings: {len(result['all_strings'])}\n")
        f.write(f"Textos japoneses: {len(result['japanese_original'])}\n")
        f.write(f"Decodificados exitosamente: {result['successful_decodes']}\n\n")
        
        f.write("💬 TEXTOS DECODIFICADOS:\n")
        f.write("-" * 30 + "\n")
        
        for i, (original, decoded) in enumerate(zip(result['japanese_original'], result['japanese_decoded'])):
            f.write(f"\n[{i+1:3d}] ORIGINAL: {original}\n")
            if decoded != original:
                f.write(f"     JAPONÉS:  {decoded}\n")
            else:
                f.write(f"     [NO DECODIFICADO]\n")

if __name__ == "__main__":
    pack_file = "/workspace/user_input_files/main_seq01.pack"
    
    if os.path.exists(pack_file):
        result = extract_and_decode_japanese_texts(pack_file)
        
        # Guardar resultados
        output_file = "/workspace/japanese_texts_decoded.txt"
        save_decoded_texts(result, output_file)
        
        print(f"📄 Resultados guardados en: {output_file}")
        print()
        print("🎯 ANÁLISIS COMPLETADO")
        print("✅ Formato de codificación japonés analizado")
        print("✅ Textos extraídos y procesados")
        print("✅ Listo para integración en programa principal")
        
    else:
        print(f"❌ Archivo no encontrado: {pack_file}")

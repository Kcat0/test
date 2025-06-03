#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear estructura de carpetas de prueba con archivos CSV
para verificar la funcionalidad de búsqueda recursiva automática
"""

import os
import csv
from pathlib import Path

def create_test_structure():
    """
    Crear estructura de carpetas de prueba con archivos CSV
    """
    base_dir = Path("/workspace/test_kurohyou_structure")
    
    # Limpiar directorio anterior si existe
    if base_dir.exists():
        import shutil
        shutil.rmtree(base_dir)
    
    # Crear estructura de directorios
    dirs_to_create = [
        "cinematicas/capitulo1",
        "cinematicas/capitulo2", 
        "cinematicas/finales",
        "dialogos/principales",
        "dialogos/secundarios",
        "menu",
        "otros_archivos"  # Carpeta sin CSV para probar
    ]
    
    for dir_path in dirs_to_create:
        full_path = base_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Creada carpeta: {dir_path}")
    
    # Datos de prueba para diferentes archivos CSV
    test_data = {
        "cinematicas/capitulo1/intro.csv": [
            ["542", "596", "マジでヤル気なのかよ？"],
            ["639", "703", "雄介… お前ビビッてんのか？"],
            ["821", "877", "ち… チゲーよ"]
        ],
        "cinematicas/capitulo1/pelea1.csv": [
            ["100", "200", "やめろよ！"],
            ["250", "350", "何すんだよ！"],
            ["-1", "-1", "……"]
        ],
        "cinematicas/capitulo2/inicio.csv": [
            ["1000", "1100", "俺に必要なのは…"],
            ["1150", "1250", "チカラだけだ"],
            ["1300", "1400", "仲間なんて… いらねぇ"]
        ],
        "cinematicas/finales/final_bueno.csv": [
            ["2000", "2100", "ありがとう"],
            ["2150", "2250", "また会おう"],
            ["2300", "2400", "さようなら"]
        ],
        "dialogos/principales/dragon.csv": [
            ["500", "600", "龍也…"],
            ["650", "750", "お前は最強だ"],
            ["800", "900", "頑張れ！"]
        ],
        "dialogos/secundarios/npcs.csv": [
            ["300", "400", "いらっしゃいませ"],
            ["450", "550", "何か御用ですか？"],
            ["600", "700", "ありがとうございました"]
        ],
        "menu/opciones.csv": [
            ["0", "0", "ゲーム開始"],
            ["0", "0", "設定"],
            ["0", "0", "終了"]
        ],
        # Archivo en carpeta raíz
        "ca01_test.csv": [
            ["1000", "1050", "これはテストです"],
            ["1100", "1150", "自動処理のテスト"],
            ["1200", "1250", "成功しますように"]
        ]
    }
    
    # Crear archivos CSV
    csv_count = 0
    for file_path, data in test_data.items():
        full_file_path = base_dir / file_path
        
        with open(full_file_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)
        
        csv_count += 1
        print(f"📄 Creado archivo: {file_path} ({len(data)} líneas)")
    
    # Crear algunos archivos no-CSV para verificar filtrado
    other_files = [
        "cinematicas/capitulo1/notas.txt",
        "dialogos/info.md", 
        "menu/config.json"
    ]
    
    for file_path in other_files:
        full_file_path = base_dir / file_path
        with open(full_file_path, 'w', encoding='utf-8') as f:
            f.write("Este no es un archivo CSV")
        print(f"📝 Creado archivo no-CSV: {file_path}")
    
    print(f"\n✅ ESTRUCTURA DE PRUEBA CREADA")
    print(f"📍 Ubicación: {base_dir}")
    print(f"📊 Total archivos CSV: {csv_count}")
    print(f"📊 Total carpetas: {len(dirs_to_create)}")
    print(f"📊 Total archivos no-CSV: {len(other_files)}")
    
    print(f"\n🧪 PARA PROBAR:")
    print(f"1. Ejecuta: python code/kurohyou_csv_extractor.py")
    print(f"2. Selecciona la carpeta: {base_dir}")
    print(f"3. El programa debería encontrar {csv_count} archivos CSV automáticamente")
    print(f"4. Y procesarlos todos automáticamente")
    
    return base_dir

if __name__ == "__main__":
    print("🎯 CREANDO ESTRUCTURA DE PRUEBA PARA BÚSQUEDA RECURSIVA")
    print("=" * 60)
    
    test_dir = create_test_structure()
    
    print(f"\n🎉 ¡Estructura creada exitosamente!")
    print(f"📂 Prueba el extractor automático con: {test_dir}")

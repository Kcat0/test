#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extractor Universal de Texto Japonés para Kurohyou 1 PSP
=========================================================

Este programa proporciona una interfaz gráfica completa para extraer y visualizar
texto japonés de múltiples formatos del juego Kurohyou 1 PSP:

MÓDULOS SOPORTADOS:
- CSV (Cinemáticas): Archivos de subtítulos con timing de fotogramas
- PACK (Diálogos): Archivos comprimidos GZIP con texto japonés original

Funcionalidades:
- Selección de carpeta con archivos múltiples
- Búsqueda automática recursiva de archivos CSV y PACK
- Extracción de texto japonés con decodificación específica
- Categorización automática por tipo de contenido
- Visualización unificada del contenido extraído
- Exportación de resultados por módulos
- Manejo robusto de errores
- Soporte completo para caracteres japoneses

Autor: Executor Agent
Fecha: 2025-06-03
Versión: 2.0 - Soporte Multi-formato
"""

import os
import csv
import glob
import json
import gzip
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
import re
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Constante para FPS del juego Kurohyou 1 PSP
KUROHYOU_FPS = 30.0

def frames_to_seconds(frames: int) -> float:
    """Convertir fotogramas a segundos"""
    return frames / KUROHYOU_FPS if frames > 0 else 0.0

def frames_to_milliseconds(frames: int) -> float:
    """Convertir fotogramas a milisegundos"""
    return (frames / KUROHYOU_FPS) * 1000 if frames > 0 else 0.0

def format_duration(frames: int) -> str:
    """Formatear duración desde fotogramas a texto legible"""
    if frames <= 0:
        return "0 frames"
    
    seconds = frames_to_seconds(frames)
    if seconds < 1:
        ms = frames_to_milliseconds(frames)
        return f"{frames} frames ({ms:.0f}ms)"
    else:
        return f"{frames} frames ({seconds:.2f}s)"

def decompress_pack_file(pack_file_path: str) -> bytes:
    """Descomprimir archivo .pack usando GZIP"""
    try:
        with gzip.open(pack_file_path, 'rb') as f:
            return f.read()
    except Exception as e:
        print(f"Error descomprimiendo {pack_file_path}: {e}")
        return None

def decode_utf16le_japanese(hex_bytes: str) -> str:
    """
    Función correcta para decodificar texto japonés UTF-16-LE
    Método proporcionado por el usuario
    """
    try:
        raw = bytes.fromhex(hex_bytes)
        # decodifica en little-endian y quita caracteres NUL sobrantes
        return raw.decode('utf-16-le').rstrip('\x00')
    except:
        return ""

def find_japanese_text_in_data(data: bytes) -> List[Tuple[str, str, int]]:
    """
    Encontrar secuencias de texto japonés UTF-16-LE en datos binarios
    
    Returns:
        Lista de tuplas (hex_string, decoded_text, offset)
    """
    japanese_texts = []
    
    # Buscar secuencias de bytes que contengan texto japonés
    i = 0
    while i < len(data) - 3:
        # Probar diferentes longitudes de secuencia
        for length in [20, 40, 60, 80, 100, 150, 200]:
            if i + length <= len(data):
                sequence = data[i:i + length]
                hex_string = sequence.hex().upper()
                
                # Usar la función correcta del usuario
                decoded = decode_utf16le_japanese(hex_string)
                
                # Verificar si contiene caracteres japoneses válidos
                if decoded and any('\u3040' <= char <= '\u309F' or  # Hiragana
                                  '\u30A0' <= char <= '\u30FF' or  # Katakana
                                  '\u4E00' <= char <= '\u9FAF'     # Kanji
                                  for char in decoded):
                    
                    # Limpiar texto (quitar caracteres de control)
                    clean_text = ''.join(char for char in decoded 
                                       if char.isprintable() or 
                                       '\u3040' <= char <= '\u309F' or
                                       '\u30A0' <= char <= '\u30FF' or
                                       '\u4E00' <= char <= '\u9FAF')
                    
                    if clean_text.strip() and len(clean_text.strip()) >= 1:
                        japanese_texts.append((hex_string, clean_text.strip(), i))
                        i += length  # Saltar esta secuencia procesada
                        break
        else:
            i += 2  # Avanzar por pares de bytes (UTF-16)
    
    return japanese_texts

def extract_strings_from_data(data: bytes, min_length: int = 3) -> List[str]:
    """Extraer strings del archivo binario"""
    strings = []
    current_string = ""
    
    for byte in data:
        if 32 <= byte <= 126:  # ASCII imprimible
            current_string += chr(byte)
        else:
            if len(current_string) >= min_length:
                strings.append(current_string)
            current_string = ""
    
    if len(current_string) >= min_length:
        strings.append(current_string)
    
    return strings


class KurohyouUniversalExtractor:
    """
    Extractor principal para archivos CSV de Kurohyou 1 PSP
    """
    
    def __init__(self, root):
        """
        Inicializar la aplicación
        
        Args:
            root: Ventana principal de tkinter
        """
        self.root = root
        
        # Variables de estado - INICIALIZAR PRIMERO
        self.current_folder = tk.StringVar()
        self.csv_files = []  # Archivos CSV (cinemáticas)
        self.pack_files = []  # Archivos PACK (diálogos)
        self.extracted_data = {}  # Datos extraídos de ambos tipos
        self.is_processing = False
        
        # Configurar ventana y widgets
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """
        Configurar la ventana principal
        """
        self.root.title("Extractor de Texto Japonés - Kurohyou 1 PSP")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configurar el ícono y estilo
        self.root.configure(bg='#f0f0f0')
        
        # Configurar el grid principal
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def create_widgets(self):
        """
        Crear todos los widgets de la interfaz
        """
        self.create_header_frame()
        self.create_main_frame()
        self.create_status_frame()
        
    def create_header_frame(self):
        """
        Crear el frame del encabezado con controles principales
        """
        header_frame = ttk.Frame(self.root)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Título principal
        title_label = ttk.Label(
            header_frame, 
            text="🎮 Extractor Universal de Texto Japonés - Kurohyou 1 PSP",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Selector de carpeta con instrucciones
        ttk.Label(header_frame, text="📁 Selecciona carpeta (CSV + PACK se procesarán automáticamente):").grid(
            row=1, column=0, sticky="w", padx=(0, 5)
        )
        
        self.folder_entry = ttk.Entry(
            header_frame, 
            textvariable=self.current_folder,
            state="readonly",
            width=50
        )
        self.folder_entry.grid(row=1, column=1, sticky="ew", padx=5)
        
        self.browse_button = ttk.Button(
            header_frame,
            text="🎯 Seleccionar y Procesar",
            command=self.browse_folder
        )
        self.browse_button.grid(row=1, column=2, padx=(5, 0))
        
        # Botones de acción
        button_frame = ttk.Frame(header_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Indicador de procesamiento automático multi-formato
        auto_label = ttk.Label(
            button_frame,
            text="⚡ Procesamiento multi-formato: CSV (cinemáticas) + PACK (diálogos)",
            font=("Arial", 9, "italic"),
            foreground="green"
        )
        auto_label.pack(side="left", padx=(0, 15))
        
        self.export_button = ttk.Button(
            button_frame,
            text="💾 Exportar",
            command=self.export_data,
            state="disabled"
        )
        self.export_button.pack(side="left", padx=5)
        
        self.clear_button = ttk.Button(
            button_frame,
            text="🗑️ Limpiar",
            command=self.clear_all
        )
        self.clear_button.pack(side="left", padx=(5, 0))
        
    def create_main_frame(self):
        """
        Crear el frame principal con paneles izquierdo y derecho
        """
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        
        # Panel izquierdo - Lista de archivos
        self.create_files_panel(main_frame)
        
        # Panel derecho - Visualización del contenido
        self.create_content_panel(main_frame)
        
    def create_files_panel(self, parent):
        """
        Crear el panel izquierdo con la lista de archivos
        """
        files_frame = ttk.LabelFrame(parent, text="📋 Archivos CSV Encontrados")
        files_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        files_frame.grid_rowconfigure(1, weight=1)
        files_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para información de archivos
        info_frame = ttk.Frame(files_frame)
        info_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        info_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(info_frame, text="Total encontrados:").grid(row=0, column=0, sticky="w")
        self.files_count_label = ttk.Label(info_frame, text="0", font=("Arial", 10, "bold"))
        self.files_count_label.grid(row=0, column=1, sticky="w", padx=(5, 0))
        
        # Lista de archivos con scrollbar
        list_frame = ttk.Frame(files_frame)
        list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        self.files_listbox = tk.Listbox(
            list_frame,
            selectmode=tk.SINGLE,
            font=("Consolas", 9)
        )
        self.files_listbox.grid(row=0, column=0, sticky="nsew")
        self.files_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        files_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.files_listbox.yview)
        files_scrollbar.grid(row=0, column=1, sticky="ns")
        self.files_listbox.configure(yscrollcommand=files_scrollbar.set)
        
    def create_content_panel(self, parent):
        """
        Crear el panel derecho con visualización del contenido
        """
        content_frame = ttk.LabelFrame(parent, text="📄 Contenido del Archivo")
        content_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para información del archivo
        file_info_frame = ttk.Frame(content_frame)
        file_info_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        file_info_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(file_info_frame, text="Archivo seleccionado:").grid(row=0, column=0, sticky="w")
        self.selected_file_label = ttk.Label(
            file_info_frame, 
            text="Ninguno",
            font=("Arial", 9, "bold"),
            foreground="blue"
        )
        self.selected_file_label.grid(row=0, column=1, sticky="w", padx=(5, 0))
        
        ttk.Label(file_info_frame, text="Líneas de diálogo:").grid(row=1, column=0, sticky="w")
        self.lines_count_label = ttk.Label(file_info_frame, text="0")
        self.lines_count_label.grid(row=1, column=1, sticky="w", padx=(5, 0))
        
        # Notebook para diferentes vistas
        self.content_notebook = ttk.Notebook(content_frame)
        self.content_notebook.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Pestaña de texto japonés
        self.create_japanese_tab()
        
        # Pestaña de timing detallado
        self.create_timing_tab()
        
        # Pestaña de estadísticas
        self.create_stats_tab()
        
    def create_japanese_tab(self):
        """
        Crear la pestaña de texto japonés
        """
        japanese_frame = ttk.Frame(self.content_notebook)
        self.content_notebook.add(japanese_frame, text="🇯🇵 Texto Japonés")
        
        japanese_frame.grid_rowconfigure(0, weight=1)
        japanese_frame.grid_columnconfigure(0, weight=1)
        
        # Área de texto para mostrar el japonés
        self.japanese_text = scrolledtext.ScrolledText(
            japanese_frame,
            font=("Yu Gothic UI", 12),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.japanese_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
    def create_timing_tab(self):
        """
        Crear la pestaña de timing detallado
        """
        timing_frame = ttk.Frame(self.content_notebook)
        self.content_notebook.add(timing_frame, text="⏱️ Timing Detallado")
        
        timing_frame.grid_rowconfigure(0, weight=1)
        timing_frame.grid_columnconfigure(0, weight=1)
        
        # Treeview para mostrar datos detallados
        self.timing_tree = ttk.Treeview(
            timing_frame,
            columns=("inicio", "fin", "duracion", "texto"),
            show="tree headings"
        )
        
        # Configurar columnas
        self.timing_tree.heading("#0", text="Línea")
        self.timing_tree.heading("inicio", text="Inicio (frames)")
        self.timing_tree.heading("fin", text="Fin (frames)")
        self.timing_tree.heading("duracion", text="Duración (frames)")
        self.timing_tree.heading("texto", text="Texto")
        
        self.timing_tree.column("#0", width=60, minwidth=50)
        self.timing_tree.column("inicio", width=80, minwidth=70)
        self.timing_tree.column("fin", width=80, minwidth=70)
        self.timing_tree.column("duracion", width=90, minwidth=80)
        self.timing_tree.column("texto", width=400, minwidth=200)
        
        self.timing_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Scrollbar para el treeview
        timing_scrollbar = ttk.Scrollbar(timing_frame, orient="vertical", command=self.timing_tree.yview)
        timing_scrollbar.grid(row=0, column=1, sticky="ns")
        self.timing_tree.configure(yscrollcommand=timing_scrollbar.set)
        
        timing_frame.grid_columnconfigure(0, weight=1)
        
    def create_stats_tab(self):
        """
        Crear la pestaña de estadísticas
        """
        stats_frame = ttk.Frame(self.content_notebook)
        self.content_notebook.add(stats_frame, text="📊 Estadísticas")
        
        stats_frame.grid_rowconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para estadísticas generales
        general_stats_frame = ttk.LabelFrame(stats_frame, text="📈 Estadísticas Generales")
        general_stats_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        general_stats_frame.grid_columnconfigure(1, weight=1)
        
        # Labels para estadísticas
        self.stats_labels = {}
        stats_items = [
            ("total_lines", "Total de líneas:"),
            ("dialogue_lines", "Líneas de diálogo:"),
            ("pause_lines", "Pausas (-1,-1):"),
            ("total_duration", "Duración total:"),
            ("avg_duration", "Duración promedio:"),
            ("total_chars", "Total de caracteres:"),
            ("avg_chars", "Caracteres promedio:")
        ]
        
        for i, (key, label) in enumerate(stats_items):
            ttk.Label(general_stats_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            self.stats_labels[key] = ttk.Label(general_stats_frame, text="0", font=("Arial", 9, "bold"))
            self.stats_labels[key].grid(row=i, column=1, sticky="w", padx=5, pady=2)
        
        # Área de texto para estadísticas detalladas
        detailed_stats_frame = ttk.LabelFrame(stats_frame, text="📋 Análisis Detallado")
        detailed_stats_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        detailed_stats_frame.grid_rowconfigure(0, weight=1)
        detailed_stats_frame.grid_columnconfigure(0, weight=1)
        
        self.detailed_stats_text = scrolledtext.ScrolledText(
            detailed_stats_frame,
            font=("Consolas", 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.detailed_stats_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
    def create_status_frame(self):
        """
        Crear el frame de estado en la parte inferior
        """
        status_frame = ttk.Frame(self.root)
        status_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        status_frame.grid_columnconfigure(1, weight=1)
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            status_frame,
            variable=self.progress_var,
            mode='determinate'
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Label de estado
        self.status_label = ttk.Label(
            status_frame,
            text="📌 Listo para comenzar",
            font=("Arial", 9)
        )
        self.status_label.grid(row=0, column=1, sticky="w")
        
    def browse_folder(self):
        """
        Abrir diálogo para seleccionar carpeta y procesar automáticamente
        """
        folder_path = filedialog.askdirectory(
            title="Seleccionar carpeta con archivos CSV de Kurohyou"
        )
        
        if folder_path:
            self.current_folder.set(folder_path)
            self.update_status("📁 Carpeta seleccionada - Iniciando procesamiento automático...")
            
            # Limpiar datos anteriores
            self.csv_files = []
            self.extracted_data = {}
            self.files_listbox.delete(0, tk.END)
            
            # Iniciar procesamiento automático en hilo separado
            threading.Thread(target=self._auto_process_folder, daemon=True).start()
            
    def _auto_process_folder(self):
        """
        Procesar automáticamente la carpeta seleccionada:
        1. Buscar archivos CSV y PACK recursivamente
        2. Extraer texto automáticamente de ambos tipos
        """
        try:
            # Deshabilitar botones durante el procesamiento
            self.root.after(0, lambda: self._set_buttons_state("disabled"))
            
            # Fase 1: Búsqueda recursiva de archivos múltiples
            self.root.after(0, lambda: self.update_status("🔍 Fase 1/3: Buscando archivos CSV y PACK recursivamente..."))
            self.root.after(0, lambda: self.progress_var.set(5))
            
            folder_path = self.current_folder.get()
            self.csv_files = []
            self.pack_files = []
            
            # Búsqueda recursiva de ambos tipos
            subdirs_explored = 0
            for root, dirs, files in os.walk(folder_path):
                subdirs_explored += 1
                # Actualizar progreso durante búsqueda
                relative_path = os.path.relpath(root, folder_path)
                if relative_path == ".":
                    status_msg = "🔍 Explorando carpeta principal..."
                else:
                    status_msg = f"🔍 Explorando: {relative_path}"
                
                self.root.after(0, lambda msg=status_msg: self.update_status(msg))
                self.root.after(0, lambda: self.root.update_idletasks())
                
                # Buscar archivos CSV y PACK en la carpeta actual
                for file in files:
                    full_path = os.path.join(root, file)
                    if file.lower().endswith('.csv'):
                        self.csv_files.append(full_path)
                    elif file.lower().endswith('.pack'):
                        self.pack_files.append(full_path)
            
            # Actualizar progreso tras búsqueda
            self.root.after(0, lambda: self.progress_var.set(15))
            
            # Actualizar lista de archivos encontrados
            self.root.after(0, self._update_files_list)
            
            total_files = len(self.csv_files) + len(self.pack_files)
            if total_files == 0:
                self.root.after(0, lambda: self.update_status(f"⚠️ No se encontraron archivos CSV ni PACK en {subdirs_explored} carpetas exploradas"))
                self.root.after(0, lambda: self._set_buttons_state("normal"))
                return
            
            # Fase 2: Extracción de archivos CSV (cinemáticas)
            if self.csv_files:
                csv_count = len(self.csv_files)
                status_msg = f"🎬 Fase 2/3: Extrayendo cinemáticas de {csv_count} archivos CSV..."
                self.root.after(0, lambda msg=status_msg: self.update_status(msg))
                
                self.extracted_data = {}
                
                for i, csv_file in enumerate(self.csv_files):
                    # Progreso para CSV (15% a 50%)
                    progress = 15 + (i / len(self.csv_files)) * 35
                    self.root.after(0, lambda p=progress: self.progress_var.set(p))
                    
                    relative_path = os.path.relpath(csv_file, folder_path)
                    status_msg = f"🎬 CSV ({i+1}/{csv_count}): {relative_path}"
                    self.root.after(0, lambda msg=status_msg: self.update_status(msg))
                    
                    # Extraer datos CSV con categoría
                    file_data = self._extract_csv_data(csv_file)
                    if file_data:
                        file_data['category'] = 'cinemáticas'
                        file_data['file_type'] = 'CSV'
                        self.extracted_data[csv_file] = file_data
            
            # Fase 3: Extracción de archivos PACK (diálogos)
            if self.pack_files:
                pack_count = len(self.pack_files)
                status_msg = f"💬 Fase 3/3: Extrayendo diálogos de {pack_count} archivos PACK..."
                self.root.after(0, lambda msg=status_msg: self.update_status(msg))
                
                for i, pack_file in enumerate(self.pack_files):
                    # Progreso para PACK (50% a 95%)
                    progress = 50 + (i / len(self.pack_files)) * 45
                    self.root.after(0, lambda p=progress: self.progress_var.set(p))
                    
                    relative_path = os.path.relpath(pack_file, folder_path)
                    status_msg = f"💬 PACK ({i+1}/{pack_count}): {relative_path}"
                    self.root.after(0, lambda msg=status_msg: self.update_status(msg))
                    
                    # Extraer datos PACK con categoría
                    file_data = self._extract_pack_data(pack_file)
                    if file_data:
                        file_data['category'] = 'diálogos'
                        file_data['file_type'] = 'PACK'
                        self.extracted_data[pack_file] = file_data
            
            # Completar procesamiento
            self.root.after(0, lambda: self.progress_var.set(100))
            
            if self.extracted_data:
                # Habilitar exportación
                self.root.after(0, lambda: self.export_button.config(state="normal"))
                
                # Contar por categorías
                csv_count = len([d for d in self.extracted_data.values() if d.get('file_type') == 'CSV'])
                pack_count = len([d for d in self.extracted_data.values() if d.get('file_type') == 'PACK'])
                
                # Mensaje final de éxito multi-formato
                status_msg = "✅ ¡Procesamiento multi-formato completado! "
                if csv_count > 0:
                    status_msg += f"{csv_count} cinemáticas (CSV)"
                if pack_count > 0:
                    if csv_count > 0:
                        status_msg += f" + {pack_count} diálogos (PACK)"
                    else:
                        status_msg += f"{pack_count} diálogos (PACK)"
                
                if subdirs_explored > 1:
                    status_msg += f" en {subdirs_explored} carpetas"
                
                self.root.after(0, lambda msg=status_msg: self.update_status(msg))
                
                # Auto-seleccionar el primer archivo para mostrar vista previa
                all_files = self.csv_files + self.pack_files
                if all_files:
                    self.root.after(0, lambda: self.files_listbox.selection_set(0))
                    self.root.after(0, lambda: self._display_file_content(all_files[0]))
            else:
                self.root.after(0, lambda: self.update_status("⚠️ No se pudo extraer datos de ningún archivo"))
            
        except Exception as e:
            error_msg = f"❌ Error durante procesamiento automático: {str(e)}"
            self.root.after(0, lambda msg=error_msg: self.update_status(msg))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error durante el procesamiento automático:\n{str(e)}"))
        
        finally:
            # Rehabilitar botones
            self.root.after(0, lambda: self._set_buttons_state("normal"))
            
    def _update_files_list(self):
        """
        Actualizar la lista de archivos en la interfaz (CSV y PACK)
        """
        # Limpiar lista anterior
        self.files_listbox.delete(0, tk.END)
        
        folder_path = self.current_folder.get()
        all_files = []
        
        # Agregar archivos CSV con icono de cinemáticas
        for csv_file in sorted(self.csv_files):
            relative_path = os.path.relpath(csv_file, folder_path)
            if os.path.dirname(relative_path):
                display_text = f"🎬 {relative_path} [CSV-Cinemáticas]"
            else:
                display_text = f"🎬 {os.path.basename(csv_file)} [CSV-Cinemáticas]"
            
            self.files_listbox.insert(tk.END, display_text)
            all_files.append(csv_file)
        
        # Agregar archivos PACK con icono de diálogos
        for pack_file in sorted(self.pack_files):
            relative_path = os.path.relpath(pack_file, folder_path)
            if os.path.dirname(relative_path):
                display_text = f"💬 {relative_path} [PACK-Diálogos]"
            else:
                display_text = f"💬 {os.path.basename(pack_file)} [PACK-Diálogos]"
            
            self.files_listbox.insert(tk.END, display_text)
            all_files.append(pack_file)
        
        # Actualizar contador total
        total_files = len(self.csv_files) + len(self.pack_files)
        self.files_count_label.config(text=str(total_files))
        
        # Guardar lista combinada para referencia
        self.all_files = all_files
            
    def _set_buttons_state(self, state):
        """
        Cambiar el estado de botones durante procesamiento
        """
        # Solo manejar botones que aún existen
        try:
            if hasattr(self, 'export_button'):
                # Deshabilitar exportación durante procesamiento
                if state == "disabled":
                    self.export_button.config(state="disabled")
                # No habilitar automáticamente - se habilita solo si hay datos
        except:
            pass
            
    def scan_csv_files(self):
        """
        Buscar archivos CSV recursivamente en la carpeta seleccionada y todas sus subcarpetas
        """
        if not self.current_folder.get():
            messagebox.showwarning("Advertencia", "Por favor, selecciona una carpeta primero")
            return
            
        self.update_status("🔍 Buscando archivos CSV recursivamente...")
        self.progress_var.set(0)
        
        try:
            # Buscar archivos CSV recursivamente
            folder_path = self.current_folder.get()
            self.csv_files = []
            
            # Usar os.walk para búsqueda recursiva más controlada
            subdirs_explored = 0
            total_files_found = 0
            
            for root, dirs, files in os.walk(folder_path):
                subdirs_explored += 1
                # Actualizar progreso visual
                self.update_status(f"🔍 Explorando: {os.path.relpath(root, folder_path)}...")
                self.root.update_idletasks()
                
                # Buscar archivos CSV en la carpeta actual
                for file in files:
                    if file.lower().endswith('.csv'):
                        full_path = os.path.join(root, file)
                        self.csv_files.append(full_path)
                        total_files_found += 1
            
            # Limpiar la lista anterior
            self.files_listbox.delete(0, tk.END)
            
            if self.csv_files:
                # Agregar archivos a la lista con ruta relativa
                for csv_file in sorted(self.csv_files):
                    # Mostrar ruta relativa desde la carpeta base
                    relative_path = os.path.relpath(csv_file, folder_path)
                    
                    # Si está en una subcarpeta, mostrar la ruta completa
                    if os.path.dirname(relative_path):
                        display_text = f"📁 {relative_path}"
                    else:
                        # Si está en la carpeta raíz, solo mostrar el nombre
                        display_text = f"📄 {os.path.basename(csv_file)}"
                    
                    self.files_listbox.insert(tk.END, display_text)
                
                # Actualizar contador
                self.files_count_label.config(text=str(len(self.csv_files)))
                
                # Los botones se gestionan automáticamente
                
                # Mensaje de estado detallado
                status_msg = f"✅ Encontrados {len(self.csv_files)} archivos CSV"
                if subdirs_explored > 1:
                    status_msg += f" en {subdirs_explored} carpetas exploradas"
                self.update_status(status_msg)
                
            else:
                self.files_count_label.config(text="0")
                
                # Mensaje informativo sobre búsqueda recursiva
                if subdirs_explored > 1:
                    self.update_status(f"⚠️ No se encontraron archivos CSV en {subdirs_explored} carpetas exploradas")
                else:
                    self.update_status("⚠️ No se encontraron archivos CSV en la carpeta")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar archivos CSV:\n{str(e)}")
            self.update_status("❌ Error al buscar archivos")
            
    def extract_text(self):
        """
        Extraer texto de todos los archivos CSV encontrados
        """
        if not self.csv_files:
            messagebox.showwarning("Advertencia", "No hay archivos CSV para procesar")
            return
            
        if self.is_processing:
            return
            
        # Ejecutar extracción en hilo separado
        threading.Thread(target=self._extract_text_thread, daemon=True).start()
        
    def _extract_text_thread(self):
        """
        Hilo para extraer texto de archivos CSV
        """
        self.is_processing = True
        # Botón gestionado automáticamente
        
        try:
            total_files = len(self.csv_files)
            self.extracted_data = {}
            
            for i, csv_file in enumerate(self.csv_files):
                # Actualizar progreso
                progress = (i / total_files) * 100
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                
                filename = os.path.basename(csv_file)
                self.root.after(0, lambda f=filename: self.update_status(f"📝 Procesando: {f}"))
                
                # Extraer datos del archivo
                file_data = self._extract_csv_data(csv_file)
                if file_data:
                    # Usar ruta completa como clave para evitar conflictos de nombres
                    self.extracted_data[csv_file] = file_data
                    
            # Completar progreso
            self.root.after(0, lambda: self.progress_var.set(100))
            
            if self.extracted_data:
                self.root.after(0, lambda: self.export_button.config(state="normal"))
                self.root.after(0, lambda: self.update_status(f"✅ Extracción completada: {len(self.extracted_data)} archivos procesados"))
            else:
                self.root.after(0, lambda: self.update_status("⚠️ No se pudo extraer datos de ningún archivo"))
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error durante la extracción:\n{str(e)}"))
            self.root.after(0, lambda: self.update_status("❌ Error durante la extracción"))
        finally:
            self.is_processing = False
            # Botón gestionado automáticamente
            
    def _extract_csv_data(self, csv_file: str) -> Optional[Dict]:
        """
        Extraer datos de un archivo CSV específico
        
        Args:
            csv_file: Ruta al archivo CSV
            
        Returns:
            Diccionario con los datos extraídos o None si hay error
        """
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
                            # Línea con formato inválido, continuar
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
            print(f"Error procesando {csv_file}: {e}")
            return None
            
    def _extract_pack_data(self, pack_file: str) -> Optional[Dict]:
        """
        Extraer datos de un archivo PACK específico (GZIP comprimido con texto japonés UTF-16-LE)
        
        Args:
            pack_file: Ruta al archivo PACK
            
        Returns:
            Diccionario con los datos extraídos o None si hay error
        """
        try:
            # Paso 1: Descomprimir archivo GZIP
            with gzip.open(pack_file, 'rb') as f:
                decompressed_data = f.read()
            
            data = {
                'filename': os.path.basename(pack_file),
                'filepath': pack_file,
                'decompressed_size': len(decompressed_data),
                'lines': [],
                'stats': {}
            }
            
            # Paso 2: Extraer texto japonés UTF-16-LE de los datos descomprimidos
            japanese_texts = find_japanese_text_in_data(decompressed_data)
            
            dialogue_lines = 0
            total_chars = 0
            
            # Procesar textos japoneses encontrados
            for i, (hex_string, decoded_text, offset) in enumerate(japanese_texts, 1):
                # Crear entrada de línea similar al formato CSV pero para PACK
                line_data = {
                    'line_id': i,
                    'offset': offset,
                    'hex_data': hex_string,
                    'text': decoded_text,
                    'char_count': len(decoded_text),
                    'is_dialogue': True  # Los textos japoneses son diálogos
                }
                
                data['lines'].append(line_data)
                dialogue_lines += 1
                total_chars += len(decoded_text)
            
            # Calcular estadísticas para archivos PACK
            data['stats'] = {
                'total_lines': len(data['lines']),
                'dialogue_lines': dialogue_lines,
                'pause_lines': 0,  # Los PACK no tienen pausas como los CSV
                'total_chars': total_chars,
                'avg_chars': total_chars / dialogue_lines if dialogue_lines > 0 else 0,
                'decompressed_size': len(decompressed_data),
                'japanese_texts_found': len(japanese_texts)
            }
            
            return data
            
        except Exception as e:
            print(f"Error procesando archivo PACK {pack_file}: {e}")
            return None
            
    def _extract_pack_data(self, pack_file: str) -> Optional[Dict]:
        """
        Extraer datos de un archivo PACK específico (texto japonés UTF-16-LE)
        
        Args:
            pack_file: Ruta al archivo PACK
            
        Returns:
            Diccionario con los datos extraídos o None si hay error
        """
        try:
            # Descomprimir archivo PACK (GZIP)
            decompressed_data = decompress_pack_file(pack_file)
            if decompressed_data is None:
                return None
            
            data = {
                'filename': os.path.basename(pack_file),
                'filepath': pack_file,
                'lines': [],
                'stats': {},
                'decompressed_size': len(decompressed_data)
            }
            
            # Encontrar texto japonés usando el método correcto del usuario
            japanese_texts = find_japanese_text_in_data(decompressed_data)
            
            dialogue_lines = 0
            total_chars = 0
            
            # Procesar textos japoneses encontrados
            for i, (hex_string, decoded_text, offset) in enumerate(japanese_texts):
                if decoded_text.strip() and len(decoded_text.strip()) >= 1:
                    line_data = {
                        'line_id': i + 1,
                        'text': decoded_text.strip(),
                        'hex_data': hex_string,
                        'offset': offset,
                        'length': len(decoded_text.strip()),
                        'is_dialogue': True
                    }
                    
                    data['lines'].append(line_data)
                    dialogue_lines += 1
                    total_chars += len(decoded_text.strip())
            
            # Calcular estadísticas para archivos PACK
            data['stats'] = {
                'total_lines': len(data['lines']),
                'dialogue_lines': dialogue_lines,
                'pause_lines': 0,  # No hay pausas en archivos PACK
                'total_chars': total_chars,
                'avg_chars': total_chars / dialogue_lines if dialogue_lines > 0 else 0,
                'decompressed_size': len(decompressed_data),
                'compression_ratio': os.path.getsize(pack_file) / len(decompressed_data) * 100 if len(decompressed_data) > 0 else 0
            }
            
            return data
            
        except Exception as e:
            print(f"Error procesando archivo PACK {pack_file}: {e}")
            return None
            
    def on_file_select(self, event):
        """
        Manejar selección de archivo en la lista (CSV y PACK)
        """
        selection = self.files_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        
        # Obtener el archivo correspondiente por índice de la lista combinada
        if hasattr(self, 'all_files') and index < len(self.all_files):
            full_path = self.all_files[index]
            
            # Usar la ruta completa como clave para extracted_data
            if full_path in self.extracted_data:
                self._display_file_content(full_path)
            else:
                # Si no está extraído, mostrar información básica
                display_text = self.files_listbox.get(index)
                # Limpiar iconos para mostrar solo la ruta
                clean_path = display_text.replace("🎬 ", "").replace("💬 ", "").replace(" [CSV-Cinemáticas]", "").replace(" [PACK-Diálogos]", "")
                self.selected_file_label.config(text=clean_path)
            
    def _display_file_content(self, filename: str):
        """
        Mostrar el contenido de un archivo en los paneles
        """
        if filename not in self.extracted_data:
            return
            
        data = self.extracted_data[filename]
        
        # Actualizar información del archivo
        self.selected_file_label.config(text=filename)
        self.lines_count_label.config(text=str(data['stats']['dialogue_lines']))
        
        # Mostrar texto japonés
        self._display_japanese_text(data)
        
        # Mostrar timing detallado
        self._display_timing_data(data)
        
        # Mostrar estadísticas
        self._display_statistics(data)
        
    def _display_japanese_text(self, data: Dict):
        """
        Mostrar texto japonés en el área correspondiente
        """
        self.japanese_text.config(state=tk.NORMAL)
        self.japanese_text.delete(1.0, tk.END)
        
        for line_data in data['lines']:
            if not line_data['is_pause']:
                text_line = f"[{line_data['line_id']:2d}] {line_data['text']}\n"
                self.japanese_text.insert(tk.END, text_line)
                
        self.japanese_text.config(state=tk.DISABLED)
        
    def _display_timing_data(self, data: Dict):
        """
        Mostrar datos de timing en el treeview
        """
        # Limpiar datos anteriores
        for item in self.timing_tree.get_children():
            self.timing_tree.delete(item)
            
        # Agregar datos
        for line_data in data['lines']:
            if line_data['is_pause']:
                values = ("PAUSA", "PAUSA", "0", "...")
            else:
                values = (
                    f"{line_data['start_time']:,}",
                    f"{line_data['end_time']:,}",
                    f"{line_data['duration']:,}",
                    line_data['text'][:50] + "..." if len(line_data['text']) > 50 else line_data['text']
                )
                
            self.timing_tree.insert("", "end", text=str(line_data['line_id']), values=values)
            
    def _display_statistics(self, data: Dict):
        """
        Mostrar estadísticas del archivo
        """
        stats = data['stats']
        
        # Actualizar labels de estadísticas generales
        self.stats_labels['total_lines'].config(text=str(stats['total_lines']))
        self.stats_labels['dialogue_lines'].config(text=str(stats['dialogue_lines']))
        self.stats_labels['pause_lines'].config(text=str(stats['pause_lines']))
        # Mostrar duración en fotogramas y tiempo convertido
        total_duration_text = f"{stats['total_duration_frames']:,} frames ({stats['total_duration_seconds']:.2f}s)"
        avg_duration_text = f"{stats['avg_duration_frames']:.1f} frames ({stats['avg_duration_seconds']:.3f}s)"
        
        self.stats_labels['total_duration'].config(text=total_duration_text)
        self.stats_labels['avg_duration'].config(text=avg_duration_text)
        self.stats_labels['total_chars'].config(text=str(stats['total_chars']))
        self.stats_labels['avg_chars'].config(text=f"{stats['avg_chars']:.1f}")
        
        # Generar análisis detallado
        analysis = self._generate_detailed_analysis(data)
        
        self.detailed_stats_text.config(state=tk.NORMAL)
        self.detailed_stats_text.delete(1.0, tk.END)
        self.detailed_stats_text.insert(tk.END, analysis)
        self.detailed_stats_text.config(state=tk.DISABLED)
        
    def _generate_detailed_analysis(self, data: Dict) -> str:
        """
        Generar análisis detallado del archivo
        """
        stats = data['stats']
        lines = data['lines']
        
        # Calcular estadísticas de duración para análisis
        dialogue_durations = [line['duration'] for line in lines if not line['is_pause']]
        max_duration = max(dialogue_durations) if dialogue_durations else 0
        min_duration = min(dialogue_durations) if dialogue_durations else 0
        
        analysis = f"""ANÁLISIS DETALLADO - {data['filename']}
{'='*50}

📊 RESUMEN GENERAL:
- Total de entradas: {stats['total_lines']}
- Líneas de diálogo: {stats['dialogue_lines']}
- Pausas detectadas: {stats['pause_lines']}
- Duración total: {stats['total_duration_frames']:,} frames ({stats['total_duration_seconds']:.2f} segundos)

📝 ANÁLISIS DE TEXTO:
- Total de caracteres: {stats['total_chars']:,}
- Promedio por línea: {stats['avg_chars']:.1f} caracteres
- Línea más larga: {max(len(line['text']) for line in lines if not line['is_pause']) if stats['dialogue_lines'] > 0 else 0} caracteres
- Línea más corta: {min(len(line['text']) for line in lines if not line['is_pause']) if stats['dialogue_lines'] > 0 else 0} caracteres

⏱️ ANÁLISIS DE TIMING (30 FPS):
- Duración promedio: {stats['avg_duration_frames']:.1f} frames ({stats['avg_duration_seconds']:.3f}s)
- Duración más larga: {max_duration} frames ({frames_to_seconds(max_duration):.3f}s)
- Duración más corta: {min_duration} frames ({frames_to_seconds(min_duration):.3f}s)

🔍 PATRONES DETECTADOS:
"""
        
        # Detectar patrones
        if stats['pause_lines'] > 0:
            analysis += f"- Pausas narrativas: {stats['pause_lines']} pausas detectadas\n"
            
        dialogue_lines = [line for line in lines if not line['is_pause']]
        if dialogue_lines:
            # Analizar longitud de diálogos
            long_dialogues = [line for line in dialogue_lines if len(line['text']) > 20]
            short_dialogues = [line for line in dialogue_lines if len(line['text']) <= 10]
            
            if long_dialogues:
                analysis += f"- Diálogos largos: {len(long_dialogues)} líneas (>{20} caracteres)\n"
            if short_dialogues:
                analysis += f"- Diálogos cortos: {len(short_dialogues)} líneas (≤{10} caracteres)\n"
                
            # Analizar timing (30 FPS = 30 frames por segundo)
            fast_dialogues = [line for line in dialogue_lines if 0 < line['duration'] < 30]  # < 1 segundo
            slow_dialogues = [line for line in dialogue_lines if line['duration'] > 90]  # > 3 segundos
            
            if fast_dialogues:
                analysis += f"- Diálogos rápidos: {len(fast_dialogues)} líneas (<30 frames / 1s)\n"
            if slow_dialogues:
                analysis += f"- Diálogos largos: {len(slow_dialogues)} líneas (>90 frames / 3s)\n"
        
        analysis += f"\n📅 Procesado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return analysis
        
    def export_data(self):
        """
        Exportar datos extraídos
        """
        if not self.extracted_data:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
            
        # Preguntar formato de exportación
        export_format = messagebox.askyesnocancel(
            "Formato de Exportación",
            "Selecciona el formato de exportación:\n\n"
            "• SÍ: Texto plano (.txt)\n"
            "• NO: JSON estructurado (.json)\n"
            "• CANCELAR: Cancelar exportación"
        )
        
        if export_format is None:  # Cancelado
            return
            
        # Seleccionar archivo de destino
        if export_format:  # Texto plano
            file_path = filedialog.asksaveasfilename(
                title="Guardar como archivo de texto",
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            if file_path:
                self._export_as_text(file_path)
        else:  # JSON
            file_path = filedialog.asksaveasfilename(
                title="Guardar como archivo JSON",
                defaultextension=".json",
                filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
            )
            if file_path:
                self._export_as_json(file_path)
                
    def _export_as_text(self, file_path: str):
        """
        Exportar como archivo de texto plano
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("EXTRACCIÓN DE TEXTO JAPONÉS - KUROHYOU 1 PSP\n")
                f.write("="*60 + "\n\n")
                f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total de archivos: {len(self.extracted_data)}\n\n")
                
                for filename, data in self.extracted_data.items():
                    f.write(f"\n{'='*60}\n")
                    f.write(f"ARCHIVO: {filename}\n")
                    f.write(f"{'='*60}\n")
                    
                    stats = data['stats']
                    f.write(f"Líneas de diálogo: {stats['dialogue_lines']}\n")
                    f.write(f"Duración total: {stats['total_duration_frames']:,} frames ({stats['total_duration_seconds']:.2f}s)\n")
                    f.write(f"Total de caracteres: {stats['total_chars']:,}\n\n")
                    
                    f.write("TEXTO JAPONÉS:\n")
                    f.write("-" * 40 + "\n")
                    
                    for line_data in data['lines']:
                        if not line_data['is_pause']:
                            f.write(f"[{line_data['line_id']:2d}] {line_data['text']}\n")
                            
                    f.write("\n" + "-" * 40 + "\n")
                    
            messagebox.showinfo("Éxito", f"Archivo de texto exportado exitosamente:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar archivo de texto:\n{str(e)}")
            
    def _export_as_json(self, file_path: str):
        """
        Exportar como archivo JSON estructurado
        """
        try:
            export_data = {
                'metadata': {
                    'generated': datetime.now().isoformat(),
                    'total_files': len(self.extracted_data),
                    'extractor': 'Kurohyou CSV Extractor',
                    'version': '1.0'
                },
                'files': self.extracted_data
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
                
            messagebox.showinfo("Éxito", f"Archivo JSON exportado exitosamente:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar archivo JSON:\n{str(e)}")
            
    def clear_all(self):
        """
        Limpiar todos los datos y reiniciar la aplicación
        """
        # Confirmar acción
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres limpiar todos los datos?"):
            # Limpiar variables
            self.current_folder.set("")
            self.csv_files = []
            self.extracted_data = {}
            
            # Limpiar interfaz
            self.files_listbox.delete(0, tk.END)
            self.files_count_label.config(text="0")
            self.selected_file_label.config(text="Ninguno")
            self.lines_count_label.config(text="0")
            
            # Limpiar áreas de texto
            self.japanese_text.config(state=tk.NORMAL)
            self.japanese_text.delete(1.0, tk.END)
            self.japanese_text.config(state=tk.DISABLED)
            
            self.detailed_stats_text.config(state=tk.NORMAL)
            self.detailed_stats_text.delete(1.0, tk.END)
            self.detailed_stats_text.config(state=tk.DISABLED)
            
            # Limpiar treeview
            for item in self.timing_tree.get_children():
                self.timing_tree.delete(item)
                
            # Limpiar estadísticas
            for label in self.stats_labels.values():
                label.config(text="0")
                
            # Deshabilitar botón de exportar
            self.export_button.config(state="disabled")
            
            # Reiniciar progreso
            self.progress_var.set(0)
            self.update_status("📌 Listo para comenzar")
            
    def update_status(self, message: str):
        """
        Actualizar mensaje de estado
        """
        self.status_label.config(text=message)
        self.root.update_idletasks()


def main():
    """
    Función principal para ejecutar la aplicación
    """
    try:
        # Crear ventana principal
        root = tk.Tk()
        
        # Crear aplicación
        app = KurohyouUniversalExtractor(root)
        
        # Configurar cierre de aplicación
        def on_closing():
            if app.is_processing:
                if messagebox.askokcancel("Cerrar", "Hay un proceso en ejecución. ¿Estás seguro de que quieres cerrar?"):
                    root.destroy()
            else:
                root.destroy()
                
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Ejecutar aplicación
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error Fatal", f"Error al iniciar la aplicación:\n{str(e)}")


if __name__ == "__main__":
    main()

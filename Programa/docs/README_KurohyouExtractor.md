# 🎮 Extractor de Texto Japonés - Kurohyou 1 PSP

## 📋 Descripción

Este programa proporciona una interfaz gráfica completa y user-friendly para extraer y visualizar texto japonés de archivos CSV de cinemáticas del juego **Kurohyou 1 PSP**. Está diseñado para ser utilizado por usuarios no técnicos y proporciona análisis detallado del contenido extraído.

## ✨ Características Principales

### 🖥️ Interfaz Gráfica Intuitiva
- **Diseño moderno** con tkinter
- **Navegación por pestañas** para diferentes vistas
- **Indicadores visuales** de progreso y estado
- **Soporte completo** para caracteres japoneses

### 📂 Gestión de Archivos
- **Selector de carpeta** con navegador visual
- **Búsqueda automática** de archivos CSV
- **Lista interactiva** de archivos encontrados
- **Validación automática** de formato

### 📝 Extracción de Texto
- **Procesamiento concurrente** para múltiples archivos
- **Detección automática** de pausas (-1,-1)
- **Análisis de timing** (inicio, fin, duración)
- **Manejo robusto de errores** de formato

### 📊 Análisis y Visualización
- **Vista de texto japonés** con fuentes optimizadas
- **Tabla de timing detallado** con todas las métricas
- **Estadísticas completas** del contenido
- **Análisis de patrones** automático

### 💾 Exportación de Datos
- **Formato de texto plano** (.txt) para lectura fácil
- **Formato JSON estructurado** (.json) para procesamiento
- **Metadatos completos** incluidos en exportación
- **Preservación de caracteres japoneses**

## 🚀 Instalación y Uso

### Requisitos del Sistema

- **Python 3.6 o superior**
- **Sistema operativo**: Windows, macOS, o Linux
- **Fuentes japonesas** (recomendado para visualización óptima)

### Instalación de Fuentes (Opcional pero Recomendado)

#### Windows
Las fuentes japonesas generalmente están incluidas por defecto.

#### macOS
```bash
# Instalar fuentes adicionales si es necesario
brew install font-noto-sans-cjk
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install fonts-noto-cjk fonts-noto-sans-cjk
```

### Ejecución del Programa

1. **Descargar el archivo** `kurohyou_csv_extractor.py`
2. **Abrir terminal/consola** en la carpeta del archivo
3. **Ejecutar el programa**:
   ```bash
   python kurohyou_csv_extractor.py
   ```

## 📖 Guía de Uso

### 1. Selección de Carpeta
1. Hacer clic en **"Seleccionar Carpeta"**
2. Navegar hasta la carpeta que contiene los archivos CSV
3. Confirmar la selección

### 2. Búsqueda de Archivos CSV
1. Hacer clic en **"🔍 Buscar CSV"**
2. El programa buscará automáticamente todos los archivos `.csv`
3. Los archivos encontrados aparecerán en la lista izquierda

### 3. Extracción de Texto
1. Hacer clic en **"📝 Extraer Texto"**
2. El programa procesará todos los archivos encontrados
3. La barra de progreso mostrará el avance
4. Una vez completado, podrás seleccionar archivos para visualizar

### 4. Visualización del Contenido
- **Hacer clic en cualquier archivo** de la lista izquierda
- **Navegar entre pestañas** para ver diferentes aspectos:
  - **🇯🇵 Texto Japonés**: Vista limpia del diálogo
  - **⏱️ Timing Detallado**: Tabla con tiempos y duraciones
  - **📊 Estadísticas**: Análisis completo del archivo

### 5. Exportación de Datos
1. Hacer clic en **"💾 Exportar"**
2. Seleccionar formato:
   - **Texto plano** (.txt): Para lectura humana
   - **JSON estructurado** (.json): Para procesamiento automático
3. Elegir ubicación y nombre del archivo
4. Confirmar la exportación

### 6. Limpieza de Datos
- Hacer clic en **"🗑️ Limpiar"** para reiniciar la sesión
- Confirmará antes de borrar todos los datos

## 📊 Formato de Archivos CSV

### Estructura Esperada
```
tiempo_inicio,tiempo_fin,texto_japonés
542,596,マジでヤル気なのかよ？
639,703,雄介… お前ビビッてんのか？
...
-1,-1,……
```

### Descripción de Campos
- **tiempo_inicio**: Tiempo de inicio en milisegundos
- **tiempo_fin**: Tiempo de finalización en milisegundos
- **texto_japonés**: Contenido del diálogo en japonés

### Casos Especiales
- **Pausas**: Representadas como `-1,-1` en los campos de tiempo
- **Texto vacío**: Líneas con `……` u otros indicadores de pausa

## 🔍 Análisis Proporcionado

### Estadísticas Generales
- **Total de líneas** procesadas
- **Líneas de diálogo** vs **pausas**
- **Duración total** de la secuencia
- **Promedio de duración** por línea
- **Análisis de caracteres** (total y promedio)

### Análisis de Patrones
- **Diálogos largos/cortos** basados en longitud de texto
- **Timing rápido/lento** basado en duración
- **Pausas narrativas** detectadas automáticamente
- **Patrones de conversación** identificados

### Información Técnica
- **Fecha y hora** de procesamiento
- **Metadatos** de archivos
- **Estadísticas detalladas** por archivo
- **Validación de formato** automática

## 🛡️ Manejo de Errores

### Errores Comunes y Soluciones

#### "No se pueden mostrar caracteres japoneses"
- **Solución**: Instalar fuentes japonesas en el sistema
- **Linux**: `sudo apt-get install fonts-noto-cjk`

#### "Error al leer archivo CSV"
- **Causa**: Archivo con formato incorrecto o codificación no UTF-8
- **Solución**: Verificar que el archivo sea CSV válido con texto en UTF-8

#### "No se encontraron archivos CSV"
- **Causa**: Carpeta seleccionada no contiene archivos .csv
- **Solución**: Verificar que la carpeta contiene los archivos correctos

#### "Error durante la exportación"
- **Causa**: Permisos insuficientes o ruta inválida
- **Solución**: Seleccionar una ubicación con permisos de escritura

### Características de Robustez
- **Validación automática** de formato de archivos
- **Manejo graceful** de errores de codificación
- **Recuperación automática** de líneas malformadas
- **Logging detallado** de errores para debugging

## 🔧 Detalles Técnicos

### Arquitectura del Programa
- **Interfaz**: tkinter con diseño modular
- **Procesamiento**: Threading para operaciones no bloqueantes
- **Análisis**: Parsing personalizado para formato CSV específico
- **Exportación**: Múltiples formatos con preservación de Unicode

### Optimizaciones
- **Carga lazy** de contenido de archivos
- **Rendering eficiente** de texto japonés
- **Memoria optimizada** para archivos grandes
- **Procesamiento concurrente** de múltiples archivos

### Estructura de Datos
```python
{
    'filename': str,
    'filepath': str,
    'lines': [
        {
            'line_id': int,
            'start_time': int,
            'end_time': int,
            'text': str,
            'duration': int,
            'is_pause': bool
        }
    ],
    'stats': {
        'total_lines': int,
        'dialogue_lines': int,
        'pause_lines': int,
        'total_chars': int,
        'avg_chars': float,
        'total_duration': int,
        'avg_duration': float
    }
}
```

## 🎯 Casos de Uso

### Traducción de Juegos
- **Extracción de diálogos** para proyectos de traducción
- **Análisis de timing** para sincronización
- **Generación de scripts** de traducción

### Análisis de Contenido
- **Estadísticas de diálogo** para análisis narrativo
- **Patrones de conversación** para estudios de juegos
- **Métricas de timing** para análisis técnico

### Procesamiento de Datos
- **Conversión de formato** desde CSV a otros formatos
- **Preparación de datos** para herramientas de traducción
- **Backup y archivo** de contenido extraído

## 🚀 Expansiones Futuras

### Funcionalidades Planificadas
- **Integración con APIs de traducción**
- **Editor de texto integrado**
- **Comparación entre versiones**
- **Exportación a formatos de subtítulos**
- **Búsqueda y filtrado avanzado**

### Extensibilidad
- **Plugin system** para formatos adicionales
- **Temas personalizables** de interfaz
- **Configuración de fuentes** personalizada
- **Integración con herramientas externas**

## 📞 Soporte y Contribuciones

### Reportar Problemas
Si encuentras algún problema:
1. **Documenta el error** con capturas de pantalla
2. **Incluye archivos de ejemplo** que causan el problema
3. **Especifica tu sistema operativo** y versión de Python

### Mejoras Sugeridas
Las siguientes mejoras son bienvenidas:
- **Soporte para otros formatos** de archivo
- **Mejoras en la interfaz** de usuario
- **Optimizaciones de rendimiento**
- **Nuevas funcionalidades de análisis**

## 📄 Licencia y Créditos

### Licencia
Este programa se distribuye bajo licencia MIT - úsalo libremente para proyectos personales y comerciales.

### Créditos
- **Desarrollado por**: Executor Agent
- **Inspirado en**: Comunidad de traducción de Kurohyou
- **Basado en**: Análisis de archivos del juego Kurohyou 1 PSP

---

**¡Disfruta extrayendo y analizando texto japonés de Kurohyou 1 PSP! 🎮🇯🇵**

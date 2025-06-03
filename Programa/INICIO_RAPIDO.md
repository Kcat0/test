# 🚀 GUÍA DE INICIO RÁPIDO - Extractor Kurohyou 1 PSP

## ⚡ Inicio Inmediato

### Opción 1: Lanzador Automático (Recomendado)
```bash
python lanzar_extractor.py
```

### Opción 2: Ejecución Directa
```bash
python code/kurohyou_csv_extractor.py
```

## 📋 Pasos Básicos de Uso

### 1. Preparar tus Archivos CSV
- Coloca tus archivos CSV de Kurohyou en una carpeta
- Formato esperado: `tiempo_inicio,tiempo_fin,texto_japonés`
- Ejemplo: `542,596,マジでヤル気なのかよ？`

### 2. Ejecutar el Programa
1. **Abrir** el programa usando una de las opciones de arriba
2. **Seleccionar** la carpeta con tus archivos CSV
3. **Buscar** archivos CSV automáticamente
4. **Extraer** el texto japonés
5. **Visualizar** los resultados
6. **Exportar** en el formato que prefieras

### 3. Explorar los Resultados
- **🇯🇵 Texto Japonés**: Vista limpia del diálogo
- **⏱️ Timing Detallado**: Tabla con tiempos y duraciones
- **📊 Estadísticas**: Análisis completo del contenido

## 🎯 Archivos Incluidos

### Programa Principal
- `code/kurohyou_csv_extractor.py` - Aplicación completa con GUI
- `lanzar_extractor.py` - Lanzador automático

### Herramientas de Prueba
- `code/test_extractor.py` - Verificar que todo funciona
- `code/demo_extractor.py` - Demostración con archivo de ejemplo

### Documentación
- `docs/README_KurohyouExtractor.md` - Manual completo
- `INICIO_RAPIDO.md` - Esta guía
- `code/requirements.txt` - Información de dependencias

### Archivos de Ejemplo
- `user_input_files/ca01_01.csv` - Archivo CSV de ejemplo
- `data/` - Carpeta donde se guardan los resultados

## 🧪 Probar el Programa

### Ejecutar Pruebas
```bash
python code/test_extractor.py
```

### Ver Demostración
```bash
python code/demo_extractor.py
```

## 📤 Formatos de Exportación

### Texto Plano (.txt)
- Fácil de leer para humanos
- Incluye solo el texto japonés
- Ideal para revisión manual

### JSON Estructurado (.json)
- Datos completos con metadatos
- Incluye timing y estadísticas
- Ideal para procesamiento automático

### CSV de Timing (.csv)
- Tabla con tiempos detallados
- Compatible con Excel/Sheets
- Ideal para análisis de datos

### Reporte Markdown (.md)
- Documentación formateada
- Incluye análisis y estadísticas
- Ideal para documentación

## ⚠️ Requisitos del Sistema

### Software
- **Python 3.6** o superior
- **Sistema operativo**: Windows, macOS, o Linux

### Fuentes (Opcional pero Recomendado)
- **Windows**: Generalmente incluidas
- **macOS**: `brew install font-noto-sans-cjk`
- **Linux**: `sudo apt-get install fonts-noto-cjk`

## 🐛 Solución de Problemas

### "No se muestran caracteres japoneses correctamente"
- **Solución**: Instalar fuentes japonesas (ver arriba)

### "Error al leer archivo CSV"
- **Causa**: Formato incorrecto o codificación no UTF-8
- **Solución**: Verificar formato del archivo

### "No se encontraron archivos CSV"
- **Causa**: Carpeta incorrecta o archivos sin extensión .csv
- **Solución**: Verificar ubicación y extensión de archivos

### El programa no inicia
- **Solución**: Ejecutar `python lanzar_extractor.py` para diagnóstico automático

## 🎮 Acerca del Formato CSV de Kurohyou

Los archivos CSV de cinemáticas de Kurohyou 1 PSP tienen este formato:
```
542,596,マジでヤル気なのかよ？
639,703,雄介… お前ビビッてんのか？
-1,-1,……
```

Donde:
- **Primer número**: Tiempo de inicio en milisegundos
- **Segundo número**: Tiempo de fin en milisegundos  
- **Texto**: Diálogo en japonés
- **-1,-1**: Indica una pausa en la narrativa

## 📊 Características del Análisis

### Estadísticas Automáticas
- Conteo de líneas de diálogo vs pausas
- Duración total y promedio
- Análisis de caracteres japoneses
- Detección de patrones de timing

### Análisis Avanzado
- Identificación de diálogos largos/cortos
- Detección de timing rápido/lento
- Análisis de pausas narrativas
- Métricas de conversación

## 🔧 Personalización

El programa es altamente extensible:
- Código modular y bien documentado
- Soporte para nuevos formatos de exportación
- Interfaz personalizable
- Fácil integración con otras herramientas

## 📞 Soporte

### Para Problemas Técnicos
1. Ejecutar `python code/test_extractor.py` para diagnóstico
2. Revisar esta guía de solución de problemas
3. Consultar el manual completo en `docs/`

### Para Mejoras y Sugerencias
- El código está diseñado para ser fácilmente extensible
- Todas las funciones están bien documentadas
- Se pueden agregar nuevos formatos y características

---

## 🎉 ¡Listo para Comenzar!

1. **Ejecuta**: `python lanzar_extractor.py`
2. **Selecciona** tu carpeta con archivos CSV
3. **Extrae** el texto japonés
4. **Disfruta** de los resultados

**¡Que disfrutes extrayendo texto de Kurohyou 1 PSP! 🎮🇯🇵**

# 🔧 APA Multi-Page Table Fixer

> **Solve the APA table numbering problem that Word can't handle automatically**

When writing theses, scientific papers, or academic documents, you've probably faced this issue: **table titles that repeat across multiple pages need consecutive numbering** (e.g., "Table 1. Title (1/3)", "Table 1. Title (2/3)") according to APA standards.

**Microsoft Word doesn't have a built-in function to automate this.** The only "solution" Word offers is manually splitting tables, which is tedious, error-prone, and breaks your document flow.

**This tool fixes it automatically in seconds.** 🚀

---

## 🎯 The Problem

In APA style, when a table spans multiple pages, each page must show the table title with a consecutive number indicator:

- Page 1: `Table 1. Descriptive Title (1/3)`
- Page 2: `Table 1. Descriptive Title (2/3)`
- Page 3: `Table 1. Descriptive Title (3/3)`

**Word's limitations:**
- ❌ No automatic function for multi-page table numbering
- ❌ Requires manual table splitting (breaks formatting)
- ❌ Time-consuming and error-prone
- ❌ Must be done page by page

**This project:**
- ✅ Automatically detects repeated table titles
- ✅ Adds proper APA numbering in seconds
- ✅ Preserves original formatting
- ✅ Works directly on PDF files (final format)

---

## ✨ Features

- **🔍 Automatic Detection**: Finds all tables that repeat across pages
- **📊 Format Analysis**: Detects font, size, bold, and italic formatting
- **🎨 Format Preservation**: Option to keep original format or customize
- **⚡ Fast Processing**: Processes entire documents in seconds
- **🎯 APA Compliant**: Follows APA 7th edition standards
- **🔧 Scalable**: Built to handle more APA rules that Word can't automate

---

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run

```bash
python src/main.py
```

### Usage

1. **Select your PDF** (thesis, paper, or document)
2. **Review detected tables** and required modifications
3. **Choose format** (keep original or customize)
4. **Apply changes** and save your corrected PDF

**That's it!** Your document is now APA compliant. ✨

---

## 📋 Requirements

- Python 3.8+
- PDF document with table titles

---

## 🏗️ Project Status

This is an **active project** focused on solving APA formatting problems that **cannot be automated in Word**.

**Current Rule:**
- ✅ Multi-page table title numbering

**Coming Soon:**
- More APA rules that require manual work in Word
- Additional formatting corrections
- Batch processing for multiple documents

---

## 🛠️ Technical Details

- **GUI**: Modern interface with Fluent Design + Glassmorphism
- **PDF Processing**: pdfplumber + PyMuPDF
- **Architecture**: Modular and scalable for future APA rules

See [ARCHITECTURE.md](ARCHITECTURE.md) for more details.

---

## 📖 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - Free to use for academic and commercial purposes.

---

## 🙏 Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- PDF processing: [pdfplumber](https://github.com/jsvine/pdfplumber) & [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
- Design inspired by Microsoft Fluent Design System

---

# 🔧 Corrector de Tablas Multi-Página APA

> **Soluciona el problema de numeración de tablas que Word no puede manejar automáticamente**

Al escribir tesis, artículos científicos o documentos académicos, probablemente has enfrentado este problema: **los títulos de tablas que se repiten en múltiples páginas necesitan numeración consecutiva** (ej. "Tabla 1. Título (1/3)", "Tabla 1. Título (2/3)") según las normas APA.

**Microsoft Word no tiene una función integrada para automatizar esto.** La única "solución" que Word ofrece es dividir tablas manualmente, lo cual es tedioso, propenso a errores y rompe el flujo de tu documento.

**Esta herramienta lo corrige automáticamente en segundos.** 🚀

---

## 🎯 El Problema

En estilo APA, cuando una tabla abarca múltiples páginas, cada página debe mostrar el título de la tabla con un indicador numérico consecutivo:

- Página 1: `Tabla 1. Título Descriptivo (1/3)`
- Página 2: `Tabla 1. Título Descriptivo (2/3)`
- Página 3: `Tabla 1. Título Descriptivo (3/3)`

**Limitaciones de Word:**
- ❌ No tiene función automática para numeración de tablas multi-página
- ❌ Requiere división manual de tablas (rompe el formato)
- ❌ Consume mucho tiempo y es propenso a errores
- ❌ Debe hacerse página por página

**Este proyecto:**
- ✅ Detecta automáticamente títulos de tablas repetidos
- ✅ Agrega numeración APA correcta en segundos
- ✅ Preserva el formato original
- ✅ Funciona directamente en archivos PDF (formato final)

---

## ✨ Características

- **🔍 Detección Automática**: Encuentra todas las tablas que se repiten entre páginas
- **📊 Análisis de Formato**: Detecta fuente, tamaño, negrita y cursiva
- **🎨 Preservación de Formato**: Opción de mantener formato original o personalizar
- **⚡ Procesamiento Rápido**: Procesa documentos completos en segundos
- **🎯 Compatible con APA**: Sigue estándares APA 7ma edición
- **🔧 Escalable**: Construido para manejar más reglas APA que Word no puede automatizar

---

## 🚀 Inicio Rápido

### Instalación

```bash
pip install -r requirements.txt
```

### Ejecutar

```bash
python src/main.py
```

### Uso

1. **Selecciona tu PDF** (tesis, artículo o documento)
2. **Revisa las tablas detectadas** y modificaciones requeridas
3. **Elige el formato** (mantener original o personalizar)
4. **Aplica los cambios** y guarda tu PDF corregido

**¡Eso es todo!** Tu documento ahora cumple con las normas APA. ✨

---

## 📋 Requisitos

- Python 3.8+
- Documento PDF con títulos de tablas

---

## 🏗️ Estado del Proyecto

Este es un **proyecto activo** enfocado en resolver problemas de formato APA que **no se pueden automatizar en Word**.

**Regla Actual:**
- ✅ Numeración de títulos de tablas multi-página

**Próximamente:**
- Más reglas APA que requieren trabajo manual en Word
- Correcciones de formato adicionales
- Procesamiento por lotes para múltiples documentos

---

## 🛠️ Detalles Técnicos

- **GUI**: Interfaz moderna con Fluent Design + Glassmorphism
- **Procesamiento PDF**: pdfplumber + PyMuPDF
- **Arquitectura**: Modular y escalable para futuras reglas APA

Ver [ARCHITECTURE.md](ARCHITECTURE.md) para más detalles.

---

## 📖 Contribuir

¡Las contribuciones son bienvenidas! Ver [CONTRIBUTING.md](CONTRIBUTING.md) para las guías.

---

## 📄 Licencia

Licencia MIT - Libre de usar para fines académicos y comerciales.

---

## 🙏 Agradecimientos

- Construido con [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Procesamiento PDF: [pdfplumber](https://github.com/jsvine/pdfplumber) & [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
- Diseño inspirado en Microsoft Fluent Design System

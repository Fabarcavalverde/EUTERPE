---
title: "EUTERPE: Análisis Morfosintáctico de Letras del Billboard Top 100"
author: "Proyecto de Procesamiento de Lenguaje Natural"
date: "`r Sys.Date()`"
output: github_document
---

# 1. Introducción

EUTERPE es un proyecto de Procesamiento de Lenguaje Natural (PLN) enfocado en el análisis morfosintáctico de letras musicales pertenecientes al Billboard Top 100 de los ultimos 52 años.

El estudio utiliza técnicas de Part-of-Speech Tagging (POS Tagging) para identificar patrones gramaticales, estructuras lingüísticas dominantes y posibles tendencias temporales en canciones populares.

Este proyecto integra herramientas del ecosistema Python, principalmente NLTK y spaCy, para realizar el etiquetado morfosintáctico y posterior análisis cuantitativo.

---

# 2. Objetivos

## 2.1 Objetivo General

Aplicar técnicas de POS Tagging para analizar la estructura morfosintáctica de letras musicales y detectar patrones lingüísticos relevantes.

## 2.2 Objetivos Específicos

- Implementar POS Tagging utilizando NLTK y spaCy.
- Analizar la distribución de categorías gramaticales.
- Evaluar tendencias temporales en la complejidad gramatical.
- Generar visualizaciones interpretables.

---

# 3. Metodología

El proyecto sigue el siguiente pipeline:

1. Recolección de datos (corpus de letras).
2. Limpieza y normalización del texto.
3. Tokenización.
4. Etiquetado POS.
5. Cálculo de métricas lingüísticas.
6. Visualización y análisis comparativo.

---

# 4. Estructura del Proyecto

EUTERPE/  
├── dashboard/ # Aplicación de visualización  
├── data/ # Datos crudos y procesados  
├── src/ # Scripts de procesamiento  
├── tests.ipynb # Notebook exploratorio  
├── requirements.txt # Dependencias del proyecto  
├── USO_DE_IA.md # Documentación uso de IA  
├── README.Rmd # Documentación principal  




---

# 5. Instalación

## 5.1 Clonar el repositorio

```bash
git clone https://github.com/Fabarcavalverde/EUTERPE.git
cd EUTERPE

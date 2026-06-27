# Sistema de Análisis Matemático Modular — MAT1186

**Asignatura:** Introducción al Cálculo  
**Evaluación:** EID N°1 
**Carrera:** Ingeniería Civil en Informática  
**Departamento:** Departamento de Ingeniería Civil en Informática  
**Universidad:** Universidad Católica de Temuco

---

## Descripción

Aplicación web interactiva desarrollada con **Streamlit** que genera problemas personalizados de matemáticas a partir del RUT del estudiante. El sistema modela secciones cónicas, analiza funciones por tramos y evalúa continuidad, todo sin dependencias externas como numpy, sympy o pandas.

## Funcionalidades

- **Validación de RUT:** Algoritmo Módulo 11 con soporte para DV = K y DV = 0.
- **Cónicas:** Generación de coeficientes, clasificación (circunferencia, elipse, hipérbola, parábola), completación de cuadrados, forma canónica, elementos geométricos y gráficos.
- **Límites y Continuidad:** Tres casos de discontinuidad (removible, salto, infinita), tablas de aproximación numérica y gráficos con marcadores visuales.
- **Panel de Auditoría:** Interfaz para la defensa oral con campos de entrada manual.

## Estructura del Proyecto

```
calculo_EID/
├── app.py                  # Interfaz principal y flujo de control
├── README.md
├── .gitignore
└── modulos/
    ├── __init__.py
    ├── conicas.py           # Coeficientes, reglas, clasificación, completación de cuadrados
    ├── graficador.py        # Generación manual de puntos para gráficos
    ├── limites.py           # Funciones por tramos, tablas, justificación
    ├── validador_rut.py     # Validación Módulo 11
    └── utilidades.py        # Funciones compartidas (raíz cuadrada Newton-Raphson)
```

## Requisitos

- Python 3.10 o superior
- streamlit

## Instalación y Ejecución

```bash
pip install streamlit
python -m streamlit run app.py
```

## Restricciones Técnicas

- **Sin numpy, math, sympy, scipy ni pandas.** Todos los cálculos (incluyendo raíz cuadrada por Newton-Raphson) están implementados manualmente en Python puro.

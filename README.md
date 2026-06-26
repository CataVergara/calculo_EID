# SISTEMA DE EVALUACIÓN MATEMÁTICA MODULAR (MAT1186)
## Panel Analítico - Departamento de Ingeniería Civil en Informática

Este proyecto es una aplicación web interactiva desarrollada con **Streamlit** para la Evaluación Integrada de Desempeño N°1. El sistema permite modelar y analizar secciones cónicas, evaluar límites por tramos, verificar continuidad y validar credenciales mediante la extracción de dígitos del RUT.

**Restricción:** Sin numpy, math, sympy, scipy ni pandas. Cálculos implementados manualmente (Newton-Raphson para raíz cuadrada).

---

## Estructura del Proyecto

```text
 CALCULO_EID/
│
├── app.py                  # Código principal de la interfaz y flujo de control
├── README.md               # Esta guía de uso e instalación
└── modulos/                # Carpeta contenedora de los submódulos lógicos
    ├── __init__.py         # Inicializador de paquete (vacío)
    ├── conicas.py          # Coeficientes, discriminante, clasificación, completación de cuadrados, elementos geométricos
    ├── graficador.py       # Generación manual de puntos para gráficas de cónicas
    ├── limites.py          # Evaluación de funciones por tramos, tablas de aproximación, justificación algebraica
    └── validador_rut.py    # Algoritmo de validación Módulo 11 y extracción de dígitos
```

---

## Requisitos

- Python 3.10 o superior
- Librería `streamlit`

## Cómo ejecutar

```bash
python -m pip install streamlit
python -m streamlit run app.py
```

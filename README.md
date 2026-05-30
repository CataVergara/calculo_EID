# SISTEMA DE EVALUACIÓN MATEMÁTICA MODULAR (MAT1186)
## Panel Analítico - Departamento de Ingeniería Civil en Informática

Este proyecto es una aplicación web interactiva desarrollada con **Streamlit** para la Evaluación Integrada de Desempeño N°1. El sistema permite modelar y analizar secciones cónicas, evaluar límites por tramos, verificar continuidad y validar credenciales mediante la extracción de dígitos del RUT.

---

## 📁 Estructura del Proyecto

Para que el sistema funcione correctamente, los archivos deben estar organizados en tu directorio de la siguiente manera:

```text
📁 CALCULO_EID/
│
├── 📄 app.py                  # Código principal de la interfaz y flujo de control
├── 📄 README.md               # Esta guía de uso e instalación
└── 📁 modulos/                # Carpeta contenedora de los submódulos lógicos
    ├── 📄 __init__.py         # Inicializador de paquete (vacío)
    ├── 📄 conicas.py          # Lógica de procesamiento y desglose de cónicas
    ├── 📄 graficador.py       # Funciones de graficación y visualización auxiliar
    ├── 📄 limites.py          # Lógica de cálculo y aproximación de límites por tramo
    └── 📄 validador_rut.py    # Algoritmo de validación Módulo 11 y extracción de dígitos
```

---

## 🛠 Requisitos

- Python 3.10 o superior
- Librería `streamlit`

Si deseas gestionar dependencias en un entorno virtual, crea el entorno y actívalo primero.

---

## Cómo ejecutar la aplicación

1. Abre una terminal en la carpeta del proyecto `CALCULO_EID`.
2. Instala la librería necesaria:

```bash
python -m pip install streamlit
```

3. Inicia la aplicación con Streamlit:

```bash
streamlit run app.py
```

4. Abre el navegador en la URL que Streamlit muestre, típicamente:

```text
http://localhost:8501
```

---

## Notas adicionales

- `app.py` importa los módulos desde la carpeta `modulos/`.
- El flujo principal se estructura en pestañas para:
  - Secciones cónicas
  - Límites y continuidad
  - Validación de competencias
- El RUT ingresado se valida con `modulos/validador_rut.py` y luego se usa para construir los datos del modelo.

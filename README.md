# MAT1186 - Sistema de Evaluación Matemática Modular

Proyecto universitario para la asignatura de Cálculo (MAT1186).
Evaluación Integrada de Desempeño N°1.

## Estructura

- `app.py` — Punto de entrada Streamlit (3 tabs: Cónicas, Límites, Validación)
- `modulos/conicas.py` — Coeficientes, discriminante, clasificación, completación de cuadrados, elementos geométricos
- `modulos/graficador.py` — Generación manual de puntos para gráficas de cónicas (Newton-Raphson para raíz cuadrada)
- `modulos/limites.py` — Evaluación de funciones por tramos, tablas de aproximación, justificación algebraica
- `modulos/validador_rut.py` — Validación de RUT chileno (Módulo 11)

## Ejecución

```bash
streamlit run app.py
```

## Restricciones

Sin numpy, math, sympy, scipy ni pandas. Cálculos implementados manualmente.

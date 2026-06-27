# -*- coding: utf-8 -*-


def identificar_caso_discontinuidad(d8: int) -> tuple[str, str]:
    residuo = d8 % 3
    if residuo == 0:
        return "Removible (Caso 1)", "d8 es múltiplo de 3."
    elif residuo == 1:
        return "De Salto (Caso 2)", "d8 deja residuo 1 al dividirse por 3."
    else:
        return "Infinita (Caso 3)", "d8 deja residuo 2 al dividirse por 3."


def evaluar_tramos_manualmente(x: float, caso: str, d: list[int], a: float) -> float | None:
    d1 = d[-8] if len(d) == 8 else 0
    d2 = d[-7]
    d4 = d[-5]
    d5 = d[-4]

    if x < a:
        if "Removible" in caso:
            if abs(x - a) < 1e-6:
                return None
            return x + d1
        elif "De Salto" in caso:
            return x + d2
        else:
            if abs(x - a) < 1e-6:
                return -999.0
            return (d5 + 1) / (x - a)
    else:
        if "Removible" in caso:
            return x + d1
        elif "De Salto" in caso:
            return x + d4
        else:
            if abs(x - a) < 1e-6:
                return None
            return (d5 + 1) / (x - a)


def obtener_tabla_aproximacion(caso: str, d: list[int], a: float) -> tuple[list[dict], list[dict]]:
    h_izq = [1.0, 0.1, 0.01, 0.001]
    h_der = [0.001, 0.01, 0.1, 1.0]

    datos_izq: list[dict] = []
    for h in h_izq:
        x_val = a - h
        y_val = evaluar_tramos_manualmente(x_val, caso, d, a)
        datos_izq.append({"x": round(x_val, 3), "f(x)": round(y_val, 4) if y_val is not None else "No Def"})

    datos_der: list[dict] = []
    for h in h_der:
        x_val = a + h
        y_val = evaluar_tramos_manualmente(x_val, caso, d, a)
        datos_der.append({"x": round(x_val, 3), "f(x)": round(y_val, 4) if y_val is not None else "No Def"})

    return datos_izq, datos_der


def obtener_puntos_grafica(caso: str, d: list[int], a: float, rango: float = 2.0, pasos: int = 40) -> list[dict]:
    puntos: list[dict] = []
    for i in range(pasos + 1):
        x_val = a - rango + (i / pasos) * (2.0 * rango)
        if abs(x_val - a) < 1e-6:
            continue
        y_val = evaluar_tramos_manualmente(x_val, caso, d, a)
        if y_val is not None and abs(y_val) < 1e6:
            puntos.append({"x": round(x_val, 4), "y": round(y_val, 4)})
    return puntos


def obtener_texto_justificacion(caso: str, d: list[int], a: float) -> str:
    d1 = d[-8] if len(d) == 8 else 0
    d2 = d[-7]
    d4 = d[-5]
    d5 = d[-4]

    if "Removible" in caso:
        return (
            f"Indeterminación 0/0 en x={a}. "
            f"Simplificando: f(x) = x + {d1}, x ≠ {a}. "
            f"Límite bilateral = {a + d1}. "
            f"Como f({a}) no está definida, la discontinuidad es removible."
        )
    elif "De Salto" in caso:
        lim_izq = a + d2
        lim_der = a + d4
        if lim_izq == lim_der:
            return f"Ambos límites laterales coinciden ({lim_izq}). La función es continua en x={a}."
        return (
            f"Límite izquierdo = {lim_izq}, límite derecho = {lim_der}. "
            f"Como {lim_izq} ≠ {lim_der}, el límite bilateral no existe. "
            f"Hay un salto de magnitud {abs(lim_der - lim_izq)}."
        )
    else:
        return (
            f"Cuando x→{a} por izquierda, f(x) → -∞. "
            f"Cuando x→{a} por derecha, f(x) → +∞. "
            f"Por tanto, x={a} es una asíntota vertical y la discontinuidad es infinita."
        )

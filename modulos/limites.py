# -*- coding: utf-8 -*-

def identificar_caso_discontinuidad(d8):
    residuo = d8 % 3
    if residuo == 0:
        return ("Removible", f"d8 ({d8}) es multiplo de 3.")
    elif residuo == 1:
        return ("De Salto", f"d8 ({d8}) deja residuo 1 al dividirse por 3.")
    else:
        return ("Infinita", f"d8 ({d8}) deja residuo 2 al dividirse por 3.")


def evaluar_funcion(x, caso, d, a):
    d1 = d[-8] if len(d) == 8 else 0
    d2 = d[-7]
    d4 = d[-5]
    d5 = d[-4]

    if "Removible" in caso:
        if abs(x - a) < 1e-12:
            return None
        return ((x - a) * (x + d1)) / (x - a)

    elif "De Salto" in caso:
        if x < a:
            return x + d2
        else:
            return x + d4

    else:
        if abs(x - a) < 1e-12:
            return None
        return (d5 + 1) / (x - a)


def generar_tabla_aproximacion(caso, d, a):
    h_izq = [1.0, 0.1, 0.01, 0.001]
    h_der = [0.001, 0.01, 0.1, 1.0]

    datos_izq = []
    for h in h_izq:
        xv = a - h
        yv = evaluar_funcion(xv, caso, d, a)
        datos_izq.append({
            "x": round(xv, 3),
            "f(x)": round(yv, 4) if yv is not None else "No def."
        })

    datos_der = []
    for h in h_der:
        xv = a + h
        yv = evaluar_funcion(xv, caso, d, a)
        datos_der.append({
            "x": round(xv, 3),
            "f(x)": round(yv, 4) if yv is not None else "No def."
        })

    return datos_izq, datos_der


def generar_puntos_grafica(caso, d, a, rango=2.0, pasos=40):
    puntos = []
    for i in range(pasos + 1):
        xv = a - rango + (i / pasos) * (2.0 * rango)
        if abs(xv - a) < 1e-12:
            continue
        yv = evaluar_funcion(xv, caso, d, a)
        if yv is not None and abs(yv) < 150:
            puntos.append(round(yv, 4))
    return puntos


def generar_texto_justificacion(caso, d, a):
    d1 = d[-8] if len(d) == 8 else 0
    d2 = d[-7]
    d4 = d[-5]
    d5 = d[-4]

    if "Removible" in caso:
        return (
            f"1. En x = {a}, el denominador se anula: f({a}) = 0/0 (indeterminacion).\n\n"
            f"2. Simplificando algebraicamente: f(x) = x + {d1}, x ≠ {a}.\n\n"
            f"3. El limite cuando x→{a} existe y vale {a + d1}, "
            f"pero f({a}) no esta definida (agujero).\n\n"
            f"4. Por tanto, la discontinuidad es **removible**."
        )
    elif "De Salto" in caso:
        li = a + d2
        ld = a + d4
        return (
            f"Limite izquierdo: lim_(x→{a}⁻) (x + {d2}) = {li}.\n\n"
            f"Limite derecho: lim_(x→{a}⁺) (x + {d4}) = {ld}.\n\n"
            f"Al ser {li} ≠ {ld}, el limite bilateral NO existe.\n\n"
            f"Existe un **salto finito** de magnitud {abs(li - ld)} en x = {a}."
        )
    else:
        return (
            f"1. Cuando x->{a} por izquierda, el denominador (x - {a}) -> 0⁻, "
            f"por lo que f(x) -> -∞.\n\n"
            f"2. Cuando x->{a} por derecha, el denominador (x - {a}) -> 0⁺, "
            f"por lo que f(x) -> +∞.\n\n"
            f"3. Los limites laterales son infinitos y de distinto signo.\n\n"
            f"4. Existe una **asintota vertical** en x = {a}. "
            f"La discontinuidad es **infinita/esencial**."
        )

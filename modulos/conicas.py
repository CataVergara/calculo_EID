# -*- coding: utf-8 -*-

def generar_coeficientes(digitos, v_aux):
    d1, d2, d3, d4, d5, d6, d7, d8 = digitos
    A = (d1 + d2) / v_aux
    B = (d3 + d4) / v_aux
    C = -(d5 + d6)
    D = -(d7 + d8)
    E = d1 + d3 + d5 + d7
    F = 0.0
    return A, B, C, D, E, F


def aplicar_reglas_ajuste(A, B, C, digitos):
    ajustes = []
    d = digitos
    d8 = d[-1]; d7 = d[-2]; d6 = d[-3]; d5 = d[-4]
    d2 = d[-7]; d1 = d[-8] if len(d) == 8 else 0

    if (d5 + d6) % 3 == 0:
        if d7 % 2 == 0:
            B = 0.0
            C = 0.0
            ajustes.append(
                "Ajuste condicional: d5+d6 multiplo de 3 y d7 par. "
                "Se define C=0, B=0 (Parabola de eje horizontal)."
            )
        else:
            A = 0.0
            B = 0.0
            ajustes.append(
                "Ajuste condicional: d5+d6 multiplo de 3 y d7 impar. "
                "Se define A=0, B=0 (Parabola de eje vertical)."
            )
    elif d8 % 2 != 0:
        C = -C
        ajustes.append(
            "Ajuste condicional: d8 impar. Se reemplaza C por -C "
            "para generar una Hiperbola."
        )
    elif len(d) == 8 and d1 == d2:
        C = A
        B = 0.0
        ajustes.append(
            "Ajuste condicional: d1 = d2. Se impone C = A y B = 0 "
            "para generar una Circunferencia."
        )

    return float(A), float(B), float(C), ajustes


def calcular_discriminante(A, B, C):
    return B**2 - 4.0 * A * C


def clasificar_conica(A, B, C):
    disc = B**2 - 4.0 * A * C
    tol = 1e-12
    if abs(disc) < tol:
        return "Parabola"
    elif disc < 0:
        if abs(A - C) < tol and abs(B) < tol and abs(A) > tol:
            return "Circunferencia"
        return "Elipse"
    else:
        return "Hiperbola"


def _raiz_cuadrada(x):
    if x < 0:
        return None
    if x == 0:
        return 0.0
    r = x / 2.0
    for _ in range(30):
        nr = (r + x / r) / 2.0
        if abs(nr - r) < 1e-14:
            return nr
        r = nr
    return r


def completar_cuadrados(A, B, C, D, E, F, tipo):
    tol = 1e-12
    disc = B**2 - 4.0 * A * C
    tiene_rotacion = abs(B) > tol

    # Si hay rotacion y no se puede ignorar, se documenta
    if tiene_rotacion and tipo != "Hiperbola":
        pass  # se continua con la aproximacion

    if tipo == "Parabola":
        return _completar_parabola(A, B, C, D, E, F, tol)
    elif tipo == "Circunferencia":
        return _completar_circunferencia(A, B, C, D, E, F, tol)
    elif tipo == "Elipse":
        return _completar_elipse(A, B, C, D, E, F, tol)
    else:
        return _completar_hiperbola(A, B, C, D, E, F, tol)


def _completar_parabola(A, B, C, D, E, F, tol):
    # Caso: A ~ 0, C ~ 0 no deberia ocurrir (seria degenerada)
    if abs(C) > tol and abs(A) < tol:
        # Cy² + Dx + Ey + F = 0 → (y - k)² = 4p(x - h)
        Cv = C
        k = -E / (2.0 * Cv)
        if abs(D) < tol:
            return {
                "tipo": "Parabola", "eje": "horizontal",
                "error": "Coeficiente D es cero. Forma degenerada."
            }
        p_val = -D / (4.0 * Cv)
        h = -(F - E**2 / (4.0 * Cv)) / D
        return {
            "tipo": "Parabola",
            "eje": "horizontal",
            "h": h, "k": k,
            "p": p_val,
            "vertex": (round(h, 4), round(k, 4)),
            "focus": (round(h + p_val, 4), round(k, 4)),
            "directrix_tipo": "vertical",
            "directrix_val": round(h - p_val, 4),
            "canonica": f"(y - ({round(k,4)}))^2 = 4({round(p_val,4)})(x - ({round(h,4)}))"
        }
    elif abs(A) > tol and abs(C) < tol:
        # Ax² + Dx + Ey + F = 0 → (x - h)² = 4p(y - k)
        Av = A
        h = -D / (2.0 * Av)
        if abs(E) < tol:
            return {
                "tipo": "Parabola", "eje": "vertical",
                "error": "Coeficiente E es cero. Forma degenerada."
            }
        p_val = -E / (4.0 * Av)
        k = -(F - D**2 / (4.0 * Av)) / E
        return {
            "tipo": "Parabola",
            "eje": "vertical",
            "h": h, "k": k,
            "p": p_val,
            "vertex": (round(h, 4), round(k, 4)),
            "focus": (round(h, 4), round(k + p_val, 4)),
            "directrix_tipo": "horizontal",
            "directrix_val": round(k - p_val, 4),
            "canonica": f"(x - ({round(h,4)}))^2 = 4({round(p_val,4)})(y - ({round(k,4)}))"
        }
    return {"tipo": "Parabola", "error": "Forma degenerada (A y C son ambos cero)"}


def _completar_circunferencia(A, B, C, D, E, F, tol):
    Av = A
    h = -D / (2.0 * Av)
    k = -E / (2.0 * Av)
    R = -F + D**2 / (4.0 * Av) + E**2 / (4.0 * Av)
    r_cuad = R / Av
    r_val = _raiz_cuadrada(r_cuad) if r_cuad >= 0 else None
    if r_val is None or r_val < tol:
        return {
            "tipo": "Circunferencia",
            "h": round(h, 4), "k": round(k, 4),
            "radio": 0,
            "centro": (round(h, 4), round(k, 4)),
            "error": "Radio no positivo. Circunferencia degenerada."
        }
    return {
        "tipo": "Circunferencia",
        "h": round(h, 4), "k": round(k, 4),
        "radio": round(r_val, 4),
        "centro": (round(h, 4), round(k, 4)),
        "focos": [(round(h, 4), round(k, 4))],
        "vertices": [
            (round(h + r_val, 4), round(k, 4)),
            (round(h - r_val, 4), round(k, 4)),
            (round(h, 4), round(k + r_val, 4)),
            (round(h, 4), round(k - r_val, 4))
        ],
        "canonica": (
            f"(x - ({round(h,4)}))^2 + (y - ({round(k,4)}))^2 = {round(r_val,4)}^2"
        )
    }


def _completar_elipse(A, B, C, D, E, F, tol):
    h = -D / (2.0 * A)
    k = -E / (2.0 * C)
    R = -F + D**2 / (4.0 * A) + E**2 / (4.0 * C)
    a2 = R / A
    b2 = R / C
    if a2 <= 0 or b2 <= 0:
        return {
            "tipo": "Elipse",
            "h": round(h, 4), "k": round(k, 4),
            "error": "Semiejes no positivos. Elipse degenerada."
        }
    a_val = _raiz_cuadrada(a2)
    b_val = _raiz_cuadrada(b2)
    if a_val is None or b_val is None:
        return {"tipo": "Elipse", "error": "Semiejes imaginarios."}
    a_mayor = max(a_val, b_val)
    b_menor = min(a_val, b_val)
    c2 = abs(a_mayor**2 - b_menor**2)
    c_val = _raiz_cuadrada(c2) if c2 > 0 else 0.0
    if a_val >= b_val:
        focos = [(round(h + c_val, 4), round(k, 4)),
                 (round(h - c_val, 4), round(k, 4))]
        vertices = [(round(h + a_val, 4), round(k, 4)),
                    (round(h - a_val, 4), round(k, 4))]
        eje_mayor = "horizontal"
    else:
        focos = [(round(h, 4), round(k + c_val, 4)),
                 (round(h, 4), round(k - c_val, 4))]
        vertices = [(round(h, 4), round(k + b_val, 4)),
                    (round(h, 4), round(k - b_val, 4))]
        eje_mayor = "vertical"
    return {
        "tipo": "Elipse",
        "h": round(h, 4), "k": round(k, 4),
        "a": round(a_val, 4), "b": round(b_val, 4),
        "c": round(c_val, 4),
        "a_mayor": round(a_mayor, 4),
        "b_menor": round(b_menor, 4),
        "centro": (round(h, 4), round(k, 4)),
        "focos": focos,
        "vertices": vertices,
        "eje_mayor": eje_mayor,
        "long_eje_mayor": round(2 * a_mayor, 4),
        "long_eje_menor": round(2 * b_menor, 4),
        "distancia_focal": round(2 * c_val, 4),
        "canonica": (
            f"(x - ({round(h,4)}))^2 / ({round(a_val,4)})^2 "
            f"+ (y - ({round(k,4)}))^2 / ({round(b_val,4)})^2 = 1"
        )
    }


def _completar_hiperbola(A, B, C, D, E, F, tol):
    h = -D / (2.0 * A)
    k = -E / (2.0 * C)
    R = -F + D**2 / (4.0 * A) + E**2 / (4.0 * C)
    tiene_rotacion = abs(B) > tol
    if A > 0:
        a2 = R / A
        b2 = -R / C
        if a2 <= 0 or b2 <= 0:
            return {"tipo": "Hiperbola", "error": "Parametros no positivos."}
        a_val = _raiz_cuadrada(a2)
        b_val = _raiz_cuadrada(b2)
        if a_val is None or b_val is None:
            return {"tipo": "Hiperbola", "error": "Parametros imaginarios."}
        c_val = _raiz_cuadrada(a_val**2 + b_val**2)
        focos = [(round(h + c_val, 4), round(k, 4)),
                 (round(h - c_val, 4), round(k, 4))]
        vertices = [(round(h + a_val, 4), round(k, 4)),
                    (round(h - a_val, 4), round(k, 4))]
        pendiente = b_val / a_val
        asintotas = [
            (round(pendiente, 4), round(k - pendiente * h, 4)),
            (round(-pendiente, 4), round(k + pendiente * h, 4))
        ]
        orientacion = "horizontal"
    else:
        a2 = -R / A
        b2 = R / C
        if a2 <= 0 or b2 <= 0:
            return {"tipo": "Hiperbola", "error": "Parametros no positivos."}
        a_val = _raiz_cuadrada(a2)
        b_val = _raiz_cuadrada(b2)
        if a_val is None or b_val is None:
            return {"tipo": "Hiperbola", "error": "Parametros imaginarios."}
        c_val = _raiz_cuadrada(a_val**2 + b_val**2)
        focos = [(round(h, 4), round(k + c_val, 4)),
                 (round(h, 4), round(k - c_val, 4))]
        vertices = [(round(h, 4), round(k + a_val, 4)),
                    (round(h, 4), round(k - a_val, 4))]
        pendiente = a_val / b_val
        asintotas = [
            (round(pendiente, 4), round(k - pendiente * h, 4)),
            (round(-pendiente, 4), round(k + pendiente * h, 4))
        ]
        orientacion = "vertical"
    return {
        "tipo": "Hiperbola",
        "h": round(h, 4), "k": round(k, 4),
        "a": round(a_val, 4), "b": round(b_val, 4),
        "c": round(c_val, 4),
        "centro": (round(h, 4), round(k, 4)),
        "focos": focos,
        "vertices": vertices,
        "asintotas": asintotas,
        "orientacion": orientacion,
        "distancia_focal": round(2 * c_val, 4),
        "tiene_rotacion": tiene_rotacion,
        "canonica": (
            f"(x - ({round(h,4)}))^2 / ({round(a_val,4)})^2 "
            f"- (y - ({round(k,4)}))^2 / ({round(b_val,4)})^2 = 1"
            if orientacion == "horizontal" else
            f"(y - ({round(k,4)}))^2 / ({round(a_val,4)})^2 "
            f"- (x - ({round(h,4)}))^2 / ({round(b_val,4)})^2 = 1"
        )
    }


def generar_desglose_algebraico(A, B, C, D, E, F, tipo, params):
    elementos = []
    if not params or "error" in params:
        return "**Error en la transformacion:** " + params.get("error", "Parametros no disponibles.")

    if tipo == "Parabola":
        elementos.append(_desglose_parabola(A, B, C, D, E, F, params))
    elif tipo == "Circunferencia":
        elementos.append(_desglose_circunferencia(A, B, C, D, E, F, params))
    elif tipo == "Elipse":
        elementos.append(_desglose_elipse(A, B, C, D, E, F, params))
    elif tipo == "Hiperbola":
        elementos.append(_desglose_hiperbola(A, B, C, D, E, F, params))

    return "\n\n---\n\n".join(elementos)


def _fmt(v):
    return f"{v:.4f}" if abs(v) < 1e6 else f"{v:.4e}"


def _desglose_parabola(A, B, C, D, E, F, p):
    eje = p.get("eje", "vertical")
    h = p["h"]; k = p["k"]; pv = p["p"]
    lines = []
    if eje == "vertical":
        # Ax² + Dx + Ey + F = 0
        lines.append("### Desarrollo: Forma General a Canonica (Parabola Vertical)")
        lines.append("")
        lines.append(f"**Ecuacion General:**")
        lines.append(f"$$ ({_fmt(A)})x^2 + ({_fmt(D)})x + ({_fmt(E)})y + ({_fmt(F)}) = 0 $$")
        lines.append("")
        lines.append("**Paso 1:** Aislar terminos en x y completar cuadrado:")
        lines.append(f"$$ {_fmt(A)}(x^2 + {_fmt(D/A)}x) = -{_fmt(E)}y - {_fmt(F)} $$")
        lines.append(f"$$ {_fmt(A)}(x + {_fmt(h)})^2 - {_fmt(A*h**2)} = -{_fmt(E)}y - {_fmt(F)} $$")
        lines.append(f"$$ {_fmt(A)}(x + {_fmt(h)})^2 = -{_fmt(E)}(y - {_fmt(k)}) $$")
        lines.append("")
        lines.append(f"**Paso 2:** Dividir por el coeficiente:")
        lines.append(f"$$ (x - ({_fmt(-h)}))^2 = {_fmt(-E/A)}(y - ({_fmt(k)})) $$")
        lines.append("$$ \\Rightarrow 4p = " + _fmt(-E/A) + " $$")
        lines.append(f"$$ p = {_fmt(pv)} $$")
        lines.append("")
        lines.append(f"**Forma Canonica:**")
        lines.append(f"$$ {p['canonica']} $$")
    else:
        lines.append("### Desarrollo: Forma General a Canonica (Parabola Horizontal)")
        lines.append("")
        lines.append(f"**Ecuacion General:**")
        lines.append(f"$$ ({_fmt(C)})y^2 + ({_fmt(D)})x + ({_fmt(E)})y + ({_fmt(F)}) = 0 $$")
        lines.append("")
        lines.append(f"**Forma Canonica:**")
        lines.append(f"$$ {p['canonica']} $$")
    return "\n".join(lines)


def _desglose_circunferencia(A, B, C, D, E, F, p):
    h = p["h"]; k_val = p["k"]; r = p["radio"]
    lines = []
    lines.append("### Desarrollo: Forma General a Canonica (Circunferencia)")
    lines.append("")
    lines.append(f"**Ecuacion General:**")
    lines.append(f"$$ ({_fmt(A)})x^2 + ({_fmt(C)})y^2 + ({_fmt(D)})x + ({_fmt(E)})y + ({_fmt(F)}) = 0 $$")
    lines.append("")
    lines.append(f"**Paso 1:** Completar cuadrados en x e y:")
    lines.append(f"$$ {_fmt(A)}(x^2 + {_fmt(D/A)}x) + {_fmt(C)}(y^2 + {_fmt(E/C)}y) = {_fmt(-F)} $$")
    lines.append(f"$$ {_fmt(A)}(x - ({_fmt(-h)}))^2 + {_fmt(C)}(y - ({_fmt(-k_val)}))^2 = {_fmt(A*h**2 + C*k_val**2 - F)} $$")
    lines.append("")
    lines.append(f"**Forma Canonica:**")
    lines.append(f"$$ {p['canonica']} $$")
    lines.append("")
    lines.append(f"**Radio:**")
    lines.append(f"$$ r = {_fmt(r)} $$")
    return "\n".join(lines)


def _desglose_elipse(A, B, C, D, E, F, p):
    h = p["h"]; k_val = p["k"]; a = p["a"]; b = p["b"]
    lines = []
    lines.append("### Desarrollo: Forma General a Canonica (Elipse)")
    lines.append("")
    lines.append(f"**Ecuacion General:**")
    lines.append(f"$$ ({_fmt(A)})x^2 + ({_fmt(C)})y^2 + ({_fmt(D)})x + ({_fmt(E)})y + ({_fmt(F)}) = 0 $$")
    lines.append("")
    lines.append("**Paso 1:** Agrupar y completar cuadrados:")
    lines.append(f"$$ {_fmt(A)}(x^2 + {_fmt(D/A)}x) + {_fmt(C)}(y^2 + {_fmt(E/C)}y) = {_fmt(-F)} $$")
    lines.append(f"$$ {_fmt(A)}(x - ({_fmt(-h)}))^2 + {_fmt(C)}(y - ({_fmt(-k_val)}))^2 = {_fmt(A*h**2 + C*k_val**2 - F)} $$")
    lines.append("")
    lines.append("**Forma Canonica:**")
    lines.append(f"$$ {p['canonica']} $$")
    lines.append("")
    lines.append(f"**Parametros:**")
    lines.append(f"- Semieje mayor (a): {_fmt(a)}")
    lines.append(f"- Semieje menor (b): {_fmt(b)}")
    lines.append(f"- Distancia focal (c): {_fmt(p['c'])}")
    return "\n".join(lines)


def _desglose_hiperbola(A, B, C, D, E, F, p):
    h = p["h"]; k_val = p["k"]; a = p["a"]; b = p["b"]
    lines = []
    lines.append("### Desarrollo: Forma General a Canonica (Hiperbola)")
    lines.append("")
    lines.append(f"**Ecuacion General:**")
    lines.append(f"$$ ({_fmt(A)})x^2 + ({_fmt(B)})xy + ({_fmt(C)})y^2 + ({_fmt(D)})x + ({_fmt(E)})y + ({_fmt(F)}) = 0 $$")
    lines.append("")
    lines.append("**Paso 1:** Agrupar y completar cuadrados:")
    lines.append(f"$$ {_fmt(A)}(x^2 + {_fmt(D/A)}x) + {_fmt(C)}(y^2 + {_fmt(E/C)}y) = {_fmt(-F)} $$")
    lines.append("")
    lines.append("**Forma Canonica:**")
    lines.append(f"$$ {p['canonica']} $$")
    lines.append("")
    lines.append(f"**Parametros:**")
    lines.append(f"- Semieje transverso (a): {_fmt(a)}")
    lines.append(f"- Semieje conjugado (b): {_fmt(b)}")
    lines.append(f"- Distancia focal (c): {_fmt(p['c'])}")
    lines.append(f"- Orientacion: {p.get('orientacion', 'N/A')}")
    if p.get("tiene_rotacion"):
        lines.append("")
        lines.append("> **Nota:** Esta hiperbola presenta termino xy (rotacion de ejes).")
    return "\n".join(lines)


def generar_texto_elementos(p):
    if not p or "error" in p:
        return "**Elementos geometricos no disponibles.**"
    lines = []
    lines.append(f"**Tipo:** {p['tipo']}")
    if p["tipo"] == "Circunferencia":
        lines.append(f"- **Centro:** {p.get('centro', 'N/A')}")
        lines.append(f"- **Radio (r):** {p.get('radio', 'N/A')}")
        lines.append(f"- **Vertices (aprox):** {p.get('vertices', 'N/A')}")
    elif p["tipo"] == "Elipse":
        lines.append(f"- **Centro:** {p.get('centro', 'N/A')}")
        lines.append(f"- **Semieje mayor (a):** {p.get('a_mayor', 'N/A')}")
        lines.append(f"- **Semieje menor (b):** {p.get('b_menor', 'N/A')}")
        lines.append(f"- **Distancia focal (c):** {p.get('c', 'N/A')}")
        lines.append(f"- **Focos:** {p.get('focos', 'N/A')}")
        lines.append(f"- **Vertices:** {p.get('vertices', 'N/A')}")
        lines.append(f"- **Eje mayor:** {p.get('eje_mayor', 'N/A')}")
        lines.append(f"- **Longitud eje mayor:** {p.get('long_eje_mayor', 'N/A')}")
        lines.append(f"- **Longitud eje menor:** {p.get('long_eje_menor', 'N/A')}")
    elif p["tipo"] == "Hiperbola":
        lines.append(f"- **Centro:** {p.get('centro', 'N/A')}")
        lines.append(f"- **Semieje transverso (a):** {p.get('a', 'N/A')}")
        lines.append(f"- **Semieje conjugado (b):** {p.get('b', 'N/A')}")
        lines.append(f"- **Distancia focal (c):** {p.get('c', 'N/A')}")
        lines.append(f"- **Focos:** {p.get('focos', 'N/A')}")
        lines.append(f"- **Vertices:** {p.get('vertices', 'N/A')}")
        lines.append(f"- **Asintotas:** {p.get('asintotas', 'N/A')}")
        lines.append(f"- **Orientacion:** {p.get('orientacion', 'N/A')}")
    elif p["tipo"] == "Parabola":
        lines.append(f"- **Vertice:** {p.get('vertex', 'N/A')}")
        lines.append(f"- **Foco:** {p.get('focus', 'N/A')}")
        lines.append(f"- **Directriz:** {p.get('directrix_tipo', 'N/A')} = {p.get('directrix_val', 'N/A')}")
        lines.append(f"- **Parametro p:** {p.get('p', 'N/A')}")
        lines.append(f"- **Eje:** {p.get('eje', 'N/A')}")
    return "\n".join(lines)

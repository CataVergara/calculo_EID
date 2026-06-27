# -*- coding: utf-8 -*-

def generar_coeficientes(digitos, v_aux):
    """
    Genera coeficientes según pauta (Fase 1):
    Ecuación general: Ax² + By² + Cx + Dy + E = 0
    """
    d1, d2, d3, d4, d5, d6, d7, d8 = digitos
    A = (d1 + d2) / v_aux
    B = (d3 + d4) / v_aux
    C = -(d5 + d6)
    D = -(d7 + d8)
    E = d1 + d3 + d5 + d7
    F = 0.0
    return float(A), float(B), float(C), float(D), float(E), float(F)


def aplicar_reglas_ajuste(A, B, C, D, E, digitos):
    ajustes = []
    d8 = digitos[-1]
    d7 = digitos[-2]
    d6 = digitos[-3]
    d5 = digitos[-4]
    d2 = digitos[-7]
    d1 = digitos[-8] if len(digitos) == 8 else 0

    # REGLA 1: Si d8 es impar → B = -B (hipérbola) - PRIMERO
    if d8 % 2 != 0:
        B = -B
        ajustes.append("Ajuste condicional: d8 es impar. Se reemplaza B por -B para generar una Hiperbola.")
    
    # REGLA 2: Si d1 == d2 → B = A (circunferencia) - SEGUNDO
    if len(digitos) == 8 and d1 == d2:
        B = A
        ajustes.append("Ajuste condicional: d1 = d2. Se impone B = A para generar una Circunferencia.")
    
    # REGLA 3: Si d5 + d6 es múltiplo de 3 → parábola - TERCERO (ÚLTIMO)
    if (d5 + d6) % 3 == 0:
        if d7 % 2 == 0:
            B = 0.0
            ajustes.append("Ajuste condicional: d5+d6 es multiplo de 3 y d7 es par. Se define B = 0 (Parabola de eje vertical).")
        else:
            A = 0.0
            ajustes.append("Ajuste condicional: d5+d6 es multiplo de 3 y d7 es impar. Se define A = 0 (Parabola de eje horizontal).")

    return float(A), float(B), float(C), float(D), float(E), ajustes


def aplicar_reglas_individualmente(A, B, C, D, E, digitos):
    """
    Aplica cada regla de ajuste INDEPENDIENTEMENTE sobre los coeficientes base.
    Retorna una lista de (A, B, C, D, E, descripcion) para cada regla que se cumple.
    """
    resultados = []
    d8 = digitos[-1]
    d7 = digitos[-2]
    d6 = digitos[-3]
    d5 = digitos[-4]
    d2 = digitos[-7]
    d1 = digitos[-8] if len(digitos) == 8 else 0

    if d8 % 2 != 0:
        resultados.append((
            float(A), float(-B), float(C), float(D), float(E),
            "d8 es impar. Se reemplaza B por -B para generar una Hipérbola."
        ))

    if len(digitos) == 8 and d1 == d2:
        resultados.append((
            float(A), float(A), float(C), float(D), float(E),
            "d1 = d2. Se impone B = A para generar una Circunferencia."
        ))

    if (d5 + d6) % 3 == 0:
        if d7 % 2 == 0:
            resultados.append((
                float(A), 0.0, float(C), float(D), float(E),
                "d5+d6 es múltiplo de 3 y d7 es par. Se define B = 0 (Parábola de eje vertical)."
            ))
        else:
            resultados.append((
                0.0, float(B), float(C), float(D), float(E),
                "d5+d6 es múltiplo de 3 y d7 es impar. Se define A = 0 (Parábola de eje horizontal)."
            ))

    return resultados


def clasificar_conica(A, B):
    if abs(A) < 1e-9 or abs(B) < 1e-9:
        return "Parabola"
    if A * B < 0:
        return "Hiperbola"
    if abs(A - B) < 1e-9:
        return "Circunferencia"
    return "Elipse"


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


def completar_cuadrados(A, B, C, D, E, tipo):
    p = {"tipo": tipo, "A": A, "B": B, "C": C, "D": D, "E": E}

    if tipo == "Parabola":
        if abs(B) < 1e-9:
            h = -C / (2.0 * A)
            k_num = E - (C**2 / (4.0 * A))
            p["h"] = round(h, 4)
            p["k"] = round(-k_num / D, 4) if abs(D) > 1e-9 else 0.0
            p["p"] = round(-D / (4.0 * A), 4) if abs(A) > 1e-9 else 1.0
            p["centro"] = (p["h"], p["k"])
            p["focos"] = [(p["h"], round(p["k"] + p["p"], 4))]
            p["vertices"] = [(p["h"], p["k"])]
            p["directriz"] = f"y = {round(p['k'] - p['p'], 4)}"
            p["eje"] = "vertical"
        else:
            k = -D / (2.0 * B)
            h_num = E - (D**2 / (4.0 * B))
            p["k"] = round(k, 4)
            p["h"] = round(-h_num / C, 4) if abs(C) > 1e-9 else 0.0
            p["p"] = round(-C / (4.0 * B), 4) if abs(B) > 1e-9 else 1.0
            p["centro"] = (p["h"], p["k"])
            p["focos"] = [(round(p["h"] + p["p"], 4), p["k"])]
            p["vertices"] = [(p["h"], p["k"])]
            p["directriz"] = f"x = {round(p['h'] - p['p'], 4)}"
            p["eje"] = "horizontal"

    elif tipo == "Circunferencia":
        h = -C / (2.0 * A)
        k = -D / (2.0 * B)
        r_cuad = (C**2 / (4.0 * A**2)) + (D**2 / (4.0 * B**2)) - (E / A)
        r_val = _raiz_cuadrada(r_cuad) if r_cuad >= 0 else 0.0
        p["h"] = round(h, 4)
        p["k"] = round(k, 4)
        p["radio"] = round(r_val, 4)
        p["r_cuad"] = round(r_cuad, 6)
        p["imaginaria"] = r_cuad < 0
        p["punto"] = abs(r_cuad) < 1e-9
        p["centro"] = (p["h"], p["k"])
        p["focos"] = [(p["h"], p["k"])]
        p["vertices"] = [(p["h"], p["k"])]

    elif tipo in ["Elipse", "Hiperbola"]:
        h = -C / (2.0 * A)
        k = -D / (2.0 * B)
        p["h"] = round(h, 4)
        p["k"] = round(k, 4)
        p["centro"] = (p["h"], p["k"])

        M = A * (h**2) + B * (k**2) - E
        a2 = M / A if A != 0 else 1.0
        b2 = M / B if B != 0 else 1.0

        if tipo == "Elipse":
            p["M"] = round(M, 6)
            p["imaginaria"] = M <= 0
            p["a_mayor"] = round(abs(a2)**0.5, 4)
            p["b_menor"] = round(abs(b2)**0.5, 4)
            p["a"] = p["a_mayor"]
            p["b"] = p["b_menor"]
            c2 = abs(a2 - b2)
            p["c"] = round(c2**0.5, 4)
            p["vertices"] = [(round(h - p["a_mayor"], 4), k), (round(h + p["a_mayor"], 4), k)]
            p["focos"] = [(round(h - p["c"], 4), k), (round(h + p["c"], 4), k)]
            p["eje_mayor"] = "horizontal" if a2 >= b2 else "vertical"
            p["long_eje_mayor"] = round(2.0 * p["a_mayor"], 4)
            p["long_eje_menor"] = round(2.0 * p["b_menor"], 4)
        else:
            p["a"] = round(abs(a2)**0.5, 4)
            p["b"] = round(abs(b2)**0.5, 4)
            c2 = abs(a2) + abs(b2)
            p["c"] = round(c2**0.5, 4)
            p["vertices"] = [(round(h - p["a"], 4), k), (round(h + p["a"], 4), k)]
            p["focos"] = [(round(h - p["c"], 4), k), (round(h + p["c"], 4), k)]
            p["orientacion"] = "horizontal" if a2 > 0 else "vertical"
            m_p = p["b"] / p["a"] if p["a"] != 0 else 0.0
            # asintotas como tuplas (pendiente, intercepto_y) para graficador
            p["asintotas"] = [
                (m_p,  -m_p * h + k),
                (-m_p,  m_p * h + k)
            ]
            # version texto legible para mostrar al usuario
            p["asintotas_texto"] = f"y = ±{round(m_p, 4)}(x - {p['h']}) + {p['k']}"
            p["distancia_focal"] = round(2.0 * p["c"], 4)

    return p


def generar_desglose_algebraico(A, B, C, D, E, tipo, p):
    """Genera explicacion detallada del paso a paso algebraico."""
    r = lambda v: round(float(v), 4)
    ecuacion_gen = f"({r(A)})x^2 + ({r(B)})y^2 + ({r(C)})x + ({r(D)})y + ({r(E)}) = 0"

    def titulo(txt):
        return f"### {txt}\n\n"

    def nota(txt):
        return f"> {txt}\n\n"

    def resultado(expr):
        return "**Resultado canónico:**\n\n" + f"$$ {expr} $$\n\n"

    desglose = "## Guia visual de transformacion algebraica\n\n"
    desglose += nota("Ruta: forma general -> forma canonica -> forma general.")
    desglose += "---\n\n"
    desglose += titulo("1) Ecuacion general (forma inicial)")
    desglose += f"$$ {ecuacion_gen} $$\n\n"
    desglose += nota("Objetivo: transformar la ecuacion general a forma canonica por completacion de cuadrados.")

    if tipo == "Parabola":
        desglose += "---\n\n"
        desglose += titulo("2) Identificacion de la conica")
        if abs(B) < 1e-9:
            h = -C / (2.0 * A)
            t = (C / (2.0 * A))**2
            k_num = E - (C**2 / (4.0 * A))
            m = -D / A if abs(A) > 1e-9 else 0.0

            desglose += nota("Criterio: B = 0 y A != 0 -> parabola de eje vertical.")
            desglose += titulo("3) Desarrollo directo: general a canonica")
            desglose += f"**Paso 1.** Agrupar terminos en x y aislar y.\n\n$$ ({r(A)})x^2 + ({r(C)})x = -({r(D)})y - ({r(E)}) $$\n\n"
            desglose += f"**Paso 2.** Factorizar A en el lado izquierdo.\n\n$$ ({r(A)})\\left[x^2 + {r(C / A)}x\\right] = -({r(D)})y - ({r(E)}) $$\n\n"
            desglose += f"**Paso 3.** Completar cuadrado sumando y restando $\\left(\\frac{{{r(C / A)}}}{{2}}\\right)^2 = {r(t)}$.\n\n"
            desglose += f"$$ ({r(A)})\\left[(x + {r(C / (2.0 * A))})^2 - {r(t)}\\right] = -({r(D)})y - ({r(E)}) $$\n\n"
            desglose += f"**Paso 4.** Reordenar constantes y despejar.\n\n$$ ({r(A)})(x - {r(h)})^2 = -({r(D)})y - ({r(k_num)}) $$\n\n"
            if abs(D) > 1e-9:
                desglose += f"$$ (x - {p['h']})^2 = {r(m)}(y - {p['k']}) $$\n\n"
            else:
                desglose += "$$ (x - h)^2 = \\text{constante} $$\n\n"
            desglose += resultado(f"(x - {p['h']})^2 = {r(m)}(y - {p['k']})")
        else:
            k = -D / (2.0 * B)
            t = (D / (2.0 * B))**2
            h_num = E - (D**2 / (4.0 * B))
            m = -C / B if abs(B) > 1e-9 else 0.0

            desglose += nota("Criterio: A = 0 y B != 0 -> parabola de eje horizontal.")
            desglose += titulo("3) Desarrollo directo: general a canonica")
            desglose += f"**Paso 1.** Agrupar terminos en y y aislar x.\n\n$$ ({r(B)})y^2 + ({r(D)})y = -({r(C)})x - ({r(E)}) $$\n\n"
            desglose += f"**Paso 2.** Factorizar B en el lado izquierdo.\n\n$$ ({r(B)})\\left[y^2 + {r(D / B)}y\\right] = -({r(C)})x - ({r(E)}) $$\n\n"
            desglose += f"**Paso 3.** Completar cuadrado sumando y restando $\\left(\\frac{{{r(D / B)}}}{{2}}\\right)^2 = {r(t)}$.\n\n"
            desglose += f"$$ ({r(B)})\\left[(y + {r(D / (2.0 * B))})^2 - {r(t)}\\right] = -({r(C)})x - ({r(E)}) $$\n\n"
            desglose += f"**Paso 4.** Reordenar constantes y despejar.\n\n$$ ({r(B)})(y - {r(k)})^2 = -({r(C)})x - ({r(h_num)}) $$\n\n"
            if abs(C) > 1e-9:
                desglose += f"$$ (y - {p['k']})^2 = {r(m)}(x - {p['h']}) $$\n\n"
            else:
                desglose += "$$ (y - k)^2 = \\text{constante} $$\n\n"
            desglose += resultado(f"(y - {p['k']})^2 = {r(m)}(x - {p['h']})")

    elif tipo == "Circunferencia":
        h = -C / (2.0 * A)
        k = -D / (2.0 * B)
        r2 = p.get("radio", 0.0)**2

        desglose += "---\n\n"
        desglose += titulo("2) Identificacion de la conica")
        desglose += nota("Criterio: A = B != 0 -> circunferencia.")
        desglose += titulo("3) Desarrollo directo: general a canonica")
        desglose += f"**Paso 1.** Dividir toda la ecuacion por A = {r(A)}.\n\n"
        desglose += f"$$ x^2 + y^2 + {r(C / A)}x + {r(D / A)}y + {r(E / A)} = 0 $$\n\n"
        desglose += "**Paso 2.** Agrupar y completar cuadrados en x e y.\n\n"
        desglose += f"$$ (x^2 + {r(C / A)}x) + (y^2 + {r(D / A)}y) = -{r(E / A)} $$\n\n"
        desglose += f"$$ (x - {r(h)})^2 + (y - {r(k)})^2 = {r(r2)} $$\n\n"
        desglose += resultado(f"(x - {p['h']})^2 + (y - {p['k']})^2 = {r(r2)}")

    elif tipo in ["Elipse", "Hiperbola"]:
        h = -C / (2.0 * A)
        k = -D / (2.0 * B)
        M = A * (h**2) + B * (k**2) - E
        a2 = M / A if abs(A) > 1e-9 else 1.0
        b2 = M / B if abs(B) > 1e-9 else 1.0

        desglose += "---\n\n"
        desglose += titulo("2) Identificacion de la conica")
        if tipo == "Elipse":
            desglose += nota("Criterio: A*B > 0 -> elipse.")
        else:
            desglose += nota("Criterio: A*B < 0 -> hiperbola.")

        desglose += titulo("3) Desarrollo directo: general a canonica")
        desglose += f"**Paso 1.** Agrupar terminos por variable.\n\n$$ ({r(A)}x^2 + {r(C)}x) + ({r(B)}y^2 + {r(D)}y) + {r(E)} = 0 $$\n\n"
        desglose += f"**Paso 2.** Factorizar en cada grupo.\n\n$$ ({r(A)})\\left[x^2 + {r(C / A)}x\\right] + ({r(B)})\\left[y^2 + {r(D / B)}y\\right] + {r(E)} = 0 $$\n\n"
        desglose += "**Paso 3.** Completar cuadrados en ambos parentesis.\n\n"
        desglose += f"$$ ({r(A)})(x - {r(h)})^2 + ({r(B)})(y - {r(k)})^2 = {r(M)} $$\n\n"
        desglose += "**Paso 4.** Normalizar dividiendo por el termino del lado derecho.\n\n"

        if tipo == "Elipse":
            a2_f = r(p['a']**2)
            b2_f = r(p['b']**2)
            desglose += resultado(f"\\frac{{(x - {p['h']})^2}}{{{a2_f}}} + \\frac{{(y - {p['k']})^2}}{{{b2_f}}} = 1")
        else:
            ax2 = r(abs(a2))
            by2 = r(abs(b2))
            if a2 > 0:
                canon_hip = f"\\frac{{(x - {p['h']})^2}}{{{ax2}}} - \\frac{{(y - {p['k']})^2}}{{{by2}}} = 1"
            else:
                canon_hip = f"\\frac{{(y - {p['k']})^2}}{{{by2}}} - \\frac{{(x - {p['h']})^2}}{{{ax2}}} = 1"
            desglose += resultado(canon_hip)

    desglose += "---\n\n"
    desglose += titulo("4) Procedimiento inverso: canonica a general")
    desglose += nota("Partir de la canonica, expandir binomios, eliminar denominadores (si aplica) y reagrupar al lado izquierdo.")

    if tipo == "Parabola":
        if abs(B) < 1e-9:
            m = -D / A if abs(A) > 1e-9 else 0.0
            desglose += f"**Paso 1.** Partir de $$ (x - {p['h']})^2 = {r(m)}(y - {p['k']}) $$\n\n"
            desglose += f"**Paso 2.** Expandir $$ x^2 - {r(2 * p['h'])}x + {r(p['h']**2)} = {r(m)}y - {r(m * p['k'])} $$\n\n"
            desglose += f"**Paso 3.** Multiplicar por A = {r(A)} y reordenar.\n\n$$ {ecuacion_gen} $$\n\n"
        else:
            m = -C / B if abs(B) > 1e-9 else 0.0
            desglose += f"**Paso 1.** Partir de $$ (y - {p['k']})^2 = {r(m)}(x - {p['h']}) $$\n\n"
            desglose += f"**Paso 2.** Expandir $$ y^2 - {r(2 * p['k'])}y + {r(p['k']**2)} = {r(m)}x - {r(m * p['h'])} $$\n\n"
            desglose += f"**Paso 3.** Multiplicar por B = {r(B)} y reordenar.\n\n$$ {ecuacion_gen} $$\n\n"

    elif tipo == "Circunferencia":
        h_v, k_v, r_v = p['h'], p['k'], p['radio']
        desglose += f"**Paso 1.** Partir de $$ (x - {h_v})^2 + (y - {k_v})^2 = {r(r_v**2)} $$\n\n"
        desglose += f"**Paso 2.** Expandir $$ x^2 - {r(2*h_v)}x + {r(h_v**2)} + y^2 - {r(2*k_v)}y + {r(k_v**2)} = {r(r_v**2)} $$\n\n"
        desglose += f"**Paso 3.** Multiplicar por A = {r(A)} y reordenar.\n\n$$ {ecuacion_gen} $$\n\n"

    elif tipo == "Elipse":
        a2_v = r(p['a']**2)
        b2_v = r(p['b']**2)
        h_v, k_v = p['h'], p['k']
        desglose += f"**Paso 1.** Partir de $$ \\frac{{(x - {h_v})^2}}{{{a2_v}}} + \\frac{{(y - {k_v})^2}}{{{b2_v}}} = 1 $$\n\n"
        desglose += f"**Paso 2.** Eliminar denominadores: $$ {b2_v}(x - {h_v})^2 + {a2_v}(y - {k_v})^2 = {r(a2_v*b2_v)} $$\n\n"
        desglose += f"**Paso 3.** Expandir y reordenar.\n\n$$ {ecuacion_gen} $$\n\n"

    elif tipo == "Hiperbola":
        ax2 = r(p['a']**2)
        by2 = r(p['b']**2)
        h_v, k_v = p['h'], p['k']
        if p.get("orientacion", "horizontal") == "horizontal":
            canon_inv = f"\\frac{{(x - {h_v})^2}}{{{ax2}}} - \\frac{{(y - {k_v})^2}}{{{by2}}} = 1"
        else:
            canon_inv = f"\\frac{{(y - {k_v})^2}}{{{ax2}}} - \\frac{{(x - {h_v})^2}}{{{by2}}} = 1"
        desglose += f"**Paso 1.** Partir de $$ {canon_inv} $$\n\n"
        desglose += "**Paso 2.** Eliminar denominadores y expandir binomios.\n\n"
        desglose += f"**Paso 3.** Reordenar terminos al lado izquierdo.\n\n$$ {ecuacion_gen} $$\n\n"

    desglose += "---\n\n"
    desglose += "> Verificacion final: la forma canonica y la forma general son equivalentes y representan la misma conica.\n"

    return desglose


def generar_texto_elementos(p):
    if not p or "error" in p:
        return "**Elementos geometricos no disponibles.**"
    
    lines = [f"**Tipo:** {p['tipo']}"]
    
    if p["tipo"] == "Circunferencia":
        lines.append(f"- **Centro:** {p.get('centro', 'N/A')}")
        lines.append(f"- **Radio (r):** {p.get('radio', 'N/A')}")
    elif p["tipo"] == "Elipse":
        lines.append(f"- **Centro:** {p.get('centro', 'N/A')}")
        lines.append(f"- **Semieje mayor (a):** {p.get('a_mayor', 'N/A')}")
        lines.append(f"- **Semieje menor (b):** {p.get('b_menor', 'N/A')}")
        lines.append(f"- **Eje mayor:** {p.get('eje_mayor', 'N/A')}")
        lines.append(f"- **Longitud eje mayor:** {p.get('long_eje_mayor', 'N/A')}")
        lines.append(f"- **Longitud eje menor:** {p.get('long_eje_menor', 'N/A')}")
        lines.append(f"- **Distancia focal (c):** {p.get('c', 'N/A')}")
        lines.append(f"- **Focos:** {p.get('focos', 'N/A')}")
        lines.append(f"- **Vertices:** {p.get('vertices', 'N/A')}")
    elif p["tipo"] == "Hiperbola":
        lines.append(f"- **Centro:** {p.get('centro', 'N/A')}")
        lines.append(f"- **Semieje transverso (a):** {p.get('a', 'N/A')}")
        lines.append(f"- **Semieje conjugado (b):** {p.get('b', 'N/A')}")
        lines.append(f"- **Distancia focal (c):** {p.get('c', 'N/A')}")
        lines.append(f"- **Focos:** {p.get('focos', 'N/A')}")
        lines.append(f"- **Vertices:** {p.get('vertices', 'N/A')}")
        lines.append(f"- **Asintotas:** {p.get('asintotas_texto', 'N/A')}")
    elif p["tipo"] == "Parabola":
        lines.append(f"- **Vertice:** {p.get('vertices', 'N/A')}")
        lines.append(f"- **Foco:** {p.get('focos', 'N/A')}")
        lines.append(f"- **Directriz:** {p.get('directriz', 'N/A')}")
        lines.append(f"- **Parámetro p:** {p.get('p', 'N/A')}")
        lines.append(f"- **Eje:** {p.get('eje', 'N/A')}")
    
    return "\n".join(lines)
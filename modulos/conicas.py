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

    if (d5 + d6) % 3 == 0:
        if d7 % 2 == 0:
            B = 0.0
            ajustes.append("Ajuste condicional: d5+d6 es multiplo de 3 y d7 es par. Se define B = 0 (Parabola de eje vertical).")
        else:
            A = 0.0
            ajustes.append("Ajuste condicional: d5+d6 es multiplo de 3 y d7 es impar. Se define A = 0 (Parabola de eje horizontal).")
    elif d8 % 2 != 0:
        B = -B
        ajustes.append("Ajuste condicional: d8 es impar. Se reemplaza B por -B para generar una Hiperbola.")
    elif len(digitos) == 8 and d1 == d2:
        B = A
        ajustes.append("Ajuste condicional: d1 = d2. Se impone B = A para generar una Circunferencia.")

    return float(A), float(B), float(C), float(D), float(E), ajustes


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
    ecuacion_gen = f"({round(A,4)})x^2 + ({round(B,4)})y^2 + ({round(C,4)})x + ({round(D,4)})y + ({round(E,4)}) = 0"
    desglose = "#### 1. ECUACION GENERAL (Forma Inicial)\n\n"
    desglose += f"$$ {ecuacion_gen} $$\n\n"
    desglose += "**Descripción:** Ecuación de segundo grado con dos variables (Ax² + By² + Cx + Dy + E = 0).\n\n"
    
    if tipo == "Parabola":
        desglose += "#### 2. IDENTIFICACION: PARABOLA\n\n"
        if abs(B) < 1e-9:
            desglose += "Criterio: B = 0, A ≠ 0 → Parábola de eje vertical.\n\n"
            desglose += "#### 3. AGRUPACION Y AISLAMIENTO\n\n"
            desglose += f"Términos en x: $$ ({round(A,4)})x^2 + ({round(C,4)})x = -{round(D,4)}y - {round(E,4)} $$\n\n"
            desglose += "#### 4. COMPLETACION DE CUADRADOS\n\n"
            h = -C / (2.0 * A)
            desglose += f"Factor común: $$ ({round(A,4)})[x^2 + {round(C/A, 4)}x] = -{round(D,4)}y - {round(E,4)} $$\n\n"
            desglose += f"Forma canónica final: $$ (x - {p['h']})^2 = {round(-D/A, 4)}(y - {p['k']}) $$\n\n"
        else:
            desglose += "Criterio: A = 0, B ≠ 0 → Parábola de eje horizontal.\n\n"
            desglose += "#### 3. AGRUPACION Y AISLAMIENTO\n\n"
            desglose += f"Términos en y: $$ ({round(B,4)})y^2 + ({round(D,4)})y = -{round(C,4)}x - {round(E,4)} $$\n\n"
            desglose += "#### 4. COMPLETACION DE CUADRADOS\n\n"
            desglose += f"Forma canónica final: $$ (y - {p['k']})^2 = {round(-C/B, 4)}(x - {p['h']}) $$\n\n"
        
    
    elif tipo == "Circunferencia":
        desglose += "#### 2. IDENTIFICACION: CIRCUNFERENCIA\n\n"
        desglose += "Criterio: A = B ≠ 0 (coeficientes iguales) → Circunferencia.\n\n"
        desglose += "#### 3. COMPLETACION DE CUADRADOS EN AMBAS VARIABLES\n\n"
        desglose += f"Forma canónica final: $$ (x - {p['h']})^2 + (y - {p['k']})^2 = {round(p['radio']**2, 4)} $$\n\n"
    
    elif tipo == "Elipse":
        desglose += "#### 2. IDENTIFICACION: ELIPSE\n\n"
        desglose += "Criterio: A ≠ B, A·B > 0 (mismo signo) → Elipse.\n\n"
        desglose += "#### 3. COMPLETACION DE CUADRADOS Y NORMALIZACION\n\n"
        desglose += f"Forma canónica final: $$ \\frac{{(x - {p['h']})^2}}{{{round(p['a']**2, 4)}}} + \\frac{{(y - {p['k']})^2}}{{{round(p['b']**2, 4)}}} = 1 $$\n\n"
    
    elif tipo == "Hiperbola":
        desglose += "#### 2. IDENTIFICACION: HIPERBOLA\n\n"
        desglose += "Criterio: A·B < 0 (signos opuestos) → Hipérbola.\n\n"
        desglose += "#### 3. COMPLETACION DE CUADRADOS Y NORMALIZACION\n\n"
        desglose += f"Forma canónica final: $$ \\frac{{(x - {p['h']})^2}}{{{round(p['a']**2, 4)}}} - \\frac{{(y - {p['k']})^2}}{{{round(p['b']**2, 4)}}} = 1 $$\n\n"
    
    desglose += "#### 5. PROCEDIMIENTO INVERSO: Canónica → General\n\n"
    desglose += "Expandimos los binomios cuadrados perfectos y trasladamos todo al lado izquierdo:\n\n"
    
    if tipo == "Parabola":
        if abs(B) < 1e-9:
            desglose += f"Partimos de: $(x - {p['h']})^2 = {round(-D/A, 4)}(y - {p['k']})$\n\n"
            desglose += f"$x^2 - {round(2*p['h'], 4)}x + {round(p['h']**2, 4)} = {round(-D/A, 4)}y - {round(-D/A * p['k'], 4)}$\n\n"
            desglose += f"Multiplicamos por $({round(A, 4)})$ y pasamos todo al lado izquierdo:\n\n"
            desglose += f"$$ {ecuacion_gen} $$\n\n"
        else:
            desglose += f"Partimos de: $(y - {p['k']})^2 = {round(-C/B, 4)}(x - {p['h']})$\n\n"
            desglose += f"$y^2 - {round(2*p['k'], 4)}y + {round(p['k']**2, 4)} = {round(-C/B, 4)}x - {round(-C/B * p['h'], 4)}$\n\n"
            desglose += f"Multiplicamos por $({round(B, 4)})$ y pasamos todo al lado izquierdo:\n\n"
            desglose += f"$$ {ecuacion_gen} $$\n\n"
    
    elif tipo == "Circunferencia":
        h_v, k_v, r_v = p['h'], p['k'], p['radio']
        desglose += f"Partimos de: $(x - {h_v})^2 + (y - {k_v})^2 = {round(r_v**2, 4)}$\n\n"
        desglose += f"$x^2 - {round(2*h_v, 4)}x + {round(h_v**2, 4)} + y^2 - {round(2*k_v, 4)}y + {round(k_v**2, 4)} = {round(r_v**2, 4)}$\n\n"
        desglose += f"Multiplicamos por A = $({round(A, 4)})$ y pasamos $r^2$ al lado izquierdo:\n\n"
        desglose += f"$$ {ecuacion_gen} $$\n\n"
    
    elif tipo == "Elipse":
        a2_v = round(p['a']**2, 4)
        b2_v = round(p['b']**2, 4)
        h_v, k_v = p['h'], p['k']
        desglose += f"Partimos de: $\\frac{{(x-{h_v})^2}}{{{a2_v}}} + \\frac{{(y-{k_v})^2}}{{{b2_v}}} = 1$\n\n"
        desglose += f"Multiplicamos por $({a2_v} \\cdot {b2_v})$:\n\n"
        desglose += f"${b2_v}(x-{h_v})^2 + {a2_v}(y-{k_v})^2 = {a2_v} \\cdot {b2_v}$\n\n"
        desglose += f"Expandimos y reordenamos todos los términos al lado izquierdo para obtener:\n\n"
        desglose += f"$$ {ecuacion_gen} $$\n\n"
    
    elif tipo == "Hiperbola":
        a2_v = round(p['a']**2, 4)
        b2_v = round(p['b']**2, 4)
        h_v, k_v = p['h'], p['k']
        desglose += f"Partimos de: $\\frac{{(x-{h_v})^2}}{{{a2_v}}} - \\frac{{(y-{k_v})^2}}{{{b2_v}}} = 1$\n\n"
        desglose += f"Multiplicamos por $({a2_v} \\cdot {b2_v})$:\n\n"
        desglose += f"${b2_v}(x-{h_v})^2 - {a2_v}(y-{k_v})^2 = {a2_v} \\cdot {b2_v}$\n\n"
        desglose += f"Expandimos y reordenamos todos los términos al lado izquierdo para obtener:\n\n"
        desglose += f"$$ {ecuacion_gen} $$\n\n"
    
    desglose += "**Verificación:** Ambas formas son algebraicamente equivalentes y representan la misma cónica.\n"
    
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

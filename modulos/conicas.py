# -*- coding: utf-8 -*-

def aplicar_reglas_ajuste(A, B, C, d):
    """
    Aplica las alteraciones condicionales de la pauta oficial.
    """
    ajustes_aplicados = []
    d8 = d[-1]
    d7 = d[-2]
    d6 = d[-3]
    d5 = d[-4]
    d2 = d[-7]
    d1 = d[-8] if len(d) == 8 else 0
    
    if (d5 + d6) % 3 == 0:
        if d7 % 2 == 0:
            B = 0
            ajustes_aplicados.append("Ajuste condicional: d5+d6 es multiplo de 3 y d7 es par. Se define B = 0 (Parabola de eje vertical).")
        else:
            A = 0
            ajustes_aplicados.append("Ajuste condicional: d5+d6 es multiplo de 3 y d7 es impar. Se define A = 0 (Parabola de eje horizontal).")
            
    elif d8 % 2 != 0:
        B = -B
        ajustes_aplicados.append("Ajuste condicional: d8 es impar. Se reemplaza B por -B para generar una Hiperbola.")
        
    elif len(d) == 8 and d1 == d2:
        B = A
        ajustes_aplicados.append("Ajuste condicional: d1 = d2. Se impone B = A para generar una Circunferencia.")
        
    return A, B, C, ajustes_aplicados

def clasificar_conica_final(A, B):
    if A == 0 and B == 0:
        return "Estructura Degenerada"
    if A == 0 or B == 0:
        return "Parabola"
    if A == B:
        return "Circunferencia"
    if A * B < 0:
        return "Hiperbola"
    return "Elipse"

def generar_desglose_algebraico(A, B, C, D, E, tipo):
    """
    Construye las ecuaciones paso a paso en LaTeX (Directo e Inverso) sin librerias.
    """
    desglose = "#### Desarrollo Directo: Ecuacion General a Canonica\n"
    desglose += "Ecuacion General determinada:\n"
    desglose += f"$$ ({round(A,3)})x^2 + ({round(B,3)})y^2 + ({round(D,3)})x + ({round(E,3)})y = 0 $$\n\n"
    
    desglose += "Asociacion de variables por termino:\n"
    desglose += f"$$ \\left[ ({round(A,3)})x^2 + ({round(D,3)})x \\right] + \\left[ ({round(B,3)})y^2 + ({round(E,3)})y \\right] = 0 $$\n\n"
    
    p_x = round(D / A, 4) if A != 0 else 0
    p_y = round(E / B, 4) if B != 0 else 0
    
    desglose += "Factorizacion de coeficientes principales:\n"
    desglose += f"$$ {round(A,3)} \\cdot \\left( x^2 + ({p_x})x \\right) + {round(B,3)} \\cdot \\left( y^2 + ({p_y})y \\right) = 0 $$\n\n"
    
    h = round(p_x / 2, 4)
    k = round(p_y / 2, 4)
    equi_x = round((h**2) * A, 4)
    equi_y = round((k**2) * B, 4)
    lado_derecho = round(equi_x + equi_y, 4)
    
    desglose += "Completacion de cuadrados perfectos y balance del miembro derecho:\n"
    desglose += f"$$ {round(A,3)} \\cdot \\left( x + {h} \\right)^2 + {round(B,3)} \\cdot \\left( y + {k} \\right)^2 = {lado_derecho} $$\n\n"
    
    den_x = round(lado_derecho / A, 4) if A != 0 else 1
    den_y = round(lado_derecho / B, 4) if B != 0 else 1
    
    desglose += "Forma Canonica Estandar final:\n"
    desglose += f"$$ \\frac{{(x + {h})^2}}{{{den_x}}} + \\frac{{(y + {k})^2}}{{{den_y}}} = 1 $$\n\n"
    
    desglose += "#### Desarrollo Inverso: Ecuacion Canonica a General\n"
    desglose += f"Partiendo de la forma obtenida: $$\\frac{{(x + {h})^2}}{{{den_x}}} + \\frac{{(y + {k})^2}}{{{den_y}}} = 1$$\n\n"
    desglose += f"Multiplicacion por el minimo comun denominador ($ {round(den_x * den_y, 4)} $):\n"
    desglose += f"$$ {den_y} \\cdot (x + {h})^2 + {den_x} \\cdot (y + {k})^2 = {round(den_x * den_y, 4)} $$\n\n"
    desglose += "Desarrollo lineal de los binomios cuadrados perfectos:\n"
    desglose += f"$$ {den_y} \\cdot \\left( x^2 + {round(h * 2, 4)}x + {round(h**2, 4)} \\right) + {den_x} \\cdot \\left( y^2 + {round(k * 2, 4)}y + {round(k**2, 4)} \\right) = {round(den_x * den_y, 4)} $$\n\n"
    desglose += "Distribucion de factores e igualacion a cero:\n"
    desglose += f"$$ ({round(A,3)})x^2 + ({round(B,3)})y^2 + ({round(D,3)})x + ({round(E,3)})y = 0 $$\n"
    
    return desglose
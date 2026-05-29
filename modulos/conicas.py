# -*- coding: utf-8 -*-

def aplicar_reglas_ajuste(A, B, C, d):
    ajustes_aplicados = []
    d8 = d[-1]
    d7 = d[-2]
    d6 = d[-3]
    d5 = d[-4]
    d2 = d[-7]
    d1 = d[-8] if len(d) == 8 else 0
    
    if (d5 + d6) % 3 == 0:
        if d7 % 2 == 0:
            B = 0.0
            ajustes_aplicados.append("Ajuste condicional: d5+d6 es multiplo de 3 y d7 es par. Se define B = 0 (Parabola de eje vertical).")
        else:
            A = 0.0
            ajustes_aplicados.append("Ajuste condicional: d5+d6 es multiplo de 3 y d7 es impar. Se define A = 0 (Parabola de eje horizontal).")
            
    elif d8 % 2 != 0:
        B = -B
        ajustes_aplicados.append("Ajuste condicional: d8 es impar. Se reemplaza B por -B para generar una Hiperbola.")
        
    elif len(d) == 8 and d1 == d2:
        B = A
        ajustes_aplicados.append("Ajuste condicional: d1 = d2. Se impone B = A para generar una Circunferencia.")
        
    return float(A), float(B), float(C), ajustes_aplicados


def clasificar_conica_final(A, B):
    if A == 0 or B == 0:
        return "Parabola"
    elif A == B:
        return "Circunferencia"
    elif A * B < 0:
        return "Hiperbola"
    else:
        return "Elipse"


def generar_desglose_algebraico(A, B, C, D, E, tipo_curva):
    A_f = float(A)
    B_f = float(B)
    D_f = float(D)
    E_f = float(E)
    
    termino_A = f"({round(A_f,3)})x^2" if A_f != 0 else ""
    termino_B = f" + ({round(B_f,3)})y^2" if B_f != 0 else ""
    termino_D = f" + ({round(D_f,3)})x" if D_f != 0 else ""
    termino_E = f" + ({round(E_f,3)})y" if E_f != 0 else ""
    
    ecuacion_gen = f"{termino_A}{termino_B}{termino_D}{termino_E} = 0".replace("= 0 = 0", "= 0")
    if ecuacion_gen.startswith(" + "): 
        ecuacion_gen = ecuacion_gen[3:]
        
    desglose = f"""#### Desarrollo Directo: Ecuacion General a Canonica
$$ {ecuacion_gen} $$

"""
    
    if tipo_curva == "Parabola":
        if A_f == 0 and B_f != 0:
            p_y = round(E_f / B_f, 4)
            k = round(p_y / 2, 4)
            lado_der_c = round((k**2) * B_f, 4)
            factor_comun_x = round(-D_f / B_f, 4)
            val_indep = round(-lado_der_c / D_f, 4) if D_f != 0 else 0.0
            
            desglose += f"""Despeje del termino cuadratico y lineal asociado:
$$ ({round(B_f,3)})y^2 + ({round(E_f,3)})y = {-round(D_f,3)}x $$

Factorizacion por el coeficiente principal:
$$ {round(B_f,3)}(y^2 + {p_y}y) = {-round(D_f,3)}x $$

Completacion de cuadrados perfectos:
$$ {round(B_f,3)}(y + {k})^2 = {-round(D_f,3)}x + {lado_der_c} $$

**Forma Canonica Horizontal Final:**
$$ (y + {k})^2 = {factor_comun_x}(x - {val_indep}) $$
"""
        else:
            p_x = round(D_f / A_f, 4)
            h = round(p_x / 2, 4)
            lado_der_c = round((h**2) * A_f, 4)
            factor_comun_y = round(-E_f / A_f, 4)
            val_indep = round(-lado_der_c / E_f, 4) if E_f != 0 else 0.0
            
            desglose += f"""Despeje del termino cuadratico y lineal asociado:
$$ ({round(A_f,3)})x^2 + ({round(D_f,3)})x = {-round(E_f,3)}y $$

Factorizacion por el coeficiente principal:
$$ {round(A_f,3)}(x^2 + {p_x}x) = {-round(E_f,3)}y $$

Completacion de cuadrados perfectos:
$$ {round(A_f,3)}(x + {h})^2 = {-round(E_f,3)}y + {lado_der_c} $$

**Forma Canonica Vertical Final:**
$$ (x + {h})^2 = {factor_comun_y}(y - {val_indep}) $$
"""
            
        desglose += f"""
#### Desarrollo Inverso: Canonica a General
Al expandir recursivamente el binomio y agrupar de forma lineal los terminos independientes transponiendo los miembros se retorna exactamente a la expresion:
$$ {ecuacion_gen} $$
"""
    else:
        p_x = round(D_f / A_f, 4) if A_f != 0 else 0
        p_y = round(E_f / B_f, 4) if B_f != 0 else 0
        h = round(p_x / 2, 4)
        k = round(p_y / 2, 4)
        equi_x = round((h**2) * A_f, 4)
        equi_y = round((k**2) * B_f, 4)
        lado_derecho = round(equi_x + equi_y, 4)
        den_x = round(lado_derecho / A_f, 4) if A_f != 0 else 1
        den_y = round(lado_derecho / B_f, 4) if B_f != 0 else 1
        
        desglose += f"""Asociacion de componentes: 
$$ \\left[ ({round(A_f,3)})x^2 + ({round(D_f,3)})x \\right] + \\left[ ({round(B_f,3)})y^2 + ({round(E_f,3)})y \\right] = 0 $$

Factorizacion por coeficientes principales: 
$$ {round(A_f,3)}(x^2 + {p_x}x) + {round(B_f,3)}(y^2 + {p_y}y) = 0 $$

Completacion de cuadrados perfectos y balance del miembro derecho:
$$ {round(A_f,3)} \\cdot \\left( x + {h} \\right)^2 + {round(B_f,3)} \\cdot \\left( y + {k} \\right)^2 = {lado_derecho} $$

Forma Canonica Estandar final:
$$ \\frac{{(x + {h})^2}}{{{den_x}}} + \\frac{{(y + {k})^2}}{{{den_y}}} = 1 $$

#### Desarrollo Inverso: Ecuacion Canonica a General
Multiplicacion cruzada por el minimo comun denominador ($ {round(den_x * den_y, 4)} $):
$$ {den_y}(x + {h})^2 + {den_x}(y + {k})^2 = {round(den_x * den_y, 4)} $$

Expansiones cuadraticas y reduccion por agrupacion lineal:
$$ {ecuacion_gen} $$
"""
        
    return desglose
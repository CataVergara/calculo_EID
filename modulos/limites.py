# -*- coding: utf-8 -*-

def identificar_caso_discontinuidad(d8):
    residuo = d8 % 3
    if residuo == 0:
        return "Removible (Caso 1)", "d8 es multiplo de 3."
    elif residuo == 1:
        return "De Salto (Caso 2)", "d8 deja residuo 1 al dividirse por 3."
    else:
        return "Infinita (Caso 3)", "d8 deja residuo 2 al dividirse por 3."

def evaluar_tramos_manualmente(x, caso, d, a):
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
            # Caso infinita: misma formula para todo x != a
            if abs(x - a) < 1e-6:
                return None
            return (d5 + 1) / (x - a)

def obtener_tabla_aproximacion(caso, d, a):
    h_izq = [1.0, 0.1, 0.01, 0.001]
    h_der = [0.001, 0.01, 0.1, 1.0]
    
    datos_izq = []
    for h in h_izq:
        x_val = a - h
        y_val = evaluar_tramos_manualmente(x_val, caso, d, a)
        datos_izq.append({"x": round(x_val, 3), "f(x)": round(y_val, 4) if y_val is not None else "No Def"})
        
    datos_der = []
    for h in h_der:
        x_val = a + h
        y_val = evaluar_tramos_manualmente(x_val, caso, d, a)
        datos_der.append({"x": round(x_val, 3), "f(x)": round(y_val, 4) if y_val is not None else "No Def"})
        
    return datos_izq, datos_der
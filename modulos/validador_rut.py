# -*- coding: utf-8 -*-

def validar_y_procesar_rut(rut_completo):
    """
    Implementa el algoritmo oficial del Modulo 11 de forma manual.
    Retorna: (es_valido, lista_digitos, v_auxiliar, texto_pasos)
    """
    rut_limpio = "".join(c for c in rut_completo if c.isalnum()).upper()
    
    if len(rut_limpio) < 2:
        return False, [], 0, "Error: RUT demasiado corto."
    
    cuerpo = rut_limpio[:-1]
    dv_ingresado = rut_limpio[-1]
    
    if not cuerpo.isdigit():
        return False, [], 0, "Error: El cuerpo debe contener solo numeros."
    
    suma = 0
    multiplicador = 2
    detalles_multiplicacion = []
    
    for i in range(len(cuerpo) - 1, -1, -1):
        digito = int(cuerpo[i])
        producto = digito * multiplicador
        detalles_multiplicacion.append(f"{digito} x {multiplicador} = {producto}")
        suma += producto
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1
        
    resto = suma % 11
    dv_calculado = 11 - resto
    
    if dv_calculado == 11:
        dv_esperado = "0"
    elif dv_calculado == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(dv_calculado)
        
    es_valido = (dv_ingresado == dv_esperado)
    
    texto_pasos = f"Procedimiento Analitico de Validacion:\n"
    texto_pasos += "\n".join(reversed(detalles_multiplicacion))
    texto_pasos += f"\n\n* Suma acumulada: {suma}"
    texto_pasos += f"\n* Residuo ({suma} % 11): {resto}"
    texto_pasos += f"\n* Calculo DV (11 - {resto}): {dv_calculado}"
    texto_pasos += f"\n* Resultado: Esperado '{dv_esperado}' | Ingresado '{dv_ingresado}'"
    
    lista_digitos = [int(d) for d in cuerpo]
    
    if dv_ingresado == "K":
        v_auxiliar = 10
    elif dv_ingresado == "0":
        v_auxiliar = 11
    else:
        v_auxiliar = int(dv_ingresado)
        
    return es_valido, lista_digitos, v_auxiliar, texto_pasos
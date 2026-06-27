# -*- coding: utf-8 -*-


def validar_y_procesar_rut(rut_completo: str) -> tuple[bool, list[int], int, str]:
    letras_invalidas = set(c.upper() for c in rut_completo if c.isalpha() and c.upper() != 'K')
    if letras_invalidas:
        return False, [], 0, f"Error: Letras no permitidas: {', '.join(letras_invalidas)}. Solo se acepta K como dígito verificador."

    rut_limpio = "".join(c for c in rut_completo if c.isalnum()).upper()

    if len(rut_limpio) < 7:
        return False, [], 0, f"Error: RUT demasiado corto. Ingrese al menos 7 dígitos de cuerpo. Ingresado: {rut_completo}"
    if len(rut_limpio) > 9:
        return False, [], 0, f"Error: RUT demasiado largo. Máximo 9 caracteres. Ingresado: {rut_completo}"

    if rut_limpio.isdigit() and len(rut_limpio) in (7, 8):
        cuerpo = rut_limpio
        dv_ingresado: str | None = None
    else:
        cuerpo = rut_limpio[:-1]
        dv_ingresado = rut_limpio[-1]

    if not cuerpo.isdigit():
        return False, [], 0, f"Error: El cuerpo del RUT debe contener solo números. Ingresado: {cuerpo}"

    if dv_ingresado is not None and not (dv_ingresado.isdigit() or dv_ingresado == "K"):
        return False, [], 0, f"Error: Dígito verificador inválido. Debe ser número (0-9) o K. Ingresado: {dv_ingresado}"

    suma = 0
    multiplicador = 2
    detalles_multiplicacion: list[str] = []
    for i in range(len(cuerpo) - 1, -1, -1):
        digito = int(cuerpo[i])
        producto = digito * multiplicador
        detalles_multiplicacion.append(f"{digito} × {multiplicador} = {producto}")
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

    if dv_ingresado is not None and dv_ingresado != dv_esperado:
        return False, [], 0, (
            f"Error: Dígito verificador incorrecto.\n"
            f"   Esperado: {dv_esperado}\n"
            f"   Ingresado: {dv_ingresado}"
        )

    texto_pasos = f"Procedimiento Analítico de Validación (Módulo 11):\n"
    texto_pasos += "\n".join(reversed(detalles_multiplicacion))
    texto_pasos += f"\n\n• Suma acumulada: {suma}"
    texto_pasos += f"\n• Residuo ({suma} % 11): {resto}"
    texto_pasos += f"\n• Cálculo DV (11 - {resto}): {dv_calculado}"

    if dv_ingresado is None:
        texto_pasos += f"\n• DV ingresado: (no ingresado)"
        texto_pasos += f"\n• Resultado: DV autocalculado = '{dv_esperado}' ✓ Válido"
    else:
        texto_pasos += f"\n• Resultado: DV = '{dv_esperado}' ✓ Válido"

    lista_digitos = [int(d) for d in cuerpo]

    if dv_esperado == "K":
        v_auxiliar = 10
    elif dv_esperado == "0":
        v_auxiliar = 11
    else:
        v_auxiliar = int(dv_esperado)

    return True, lista_digitos, v_auxiliar, texto_pasos

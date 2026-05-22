# -*- coding: utf-8 -*-
import streamlit as st

# 1. CONFIGURACIÓN DEL ENTORNO DE TRABAJO
st.set_page_config(
    page_title="MAT1186 - Panel Analitico", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. PROCESADOR DE RUT ROBUSTO (CON CORRECCIÓN AUTOMÁTICA PARA PRUEBAS)
def procesar_rut_sistema(rut_input):
    # Limpiar caracteres especiales
    rut_limpio = ""
    for caracter in rut_input:
        if caracter.isalnum():
            rut_limpio += caracter.upper()
            
    if len(rut_limpio) < 2:
        return False, [0], 1, "RUT demasiado corto"
        
    cuerpo = rut_limpio[:-1]
    dv_ingresado = rut_limpio[-1]
    
    if not cuerpo.isdigit():
        return False, [0], 1, "Cuerpo no numerico"
        
    # Calcular el Modulo 11 real
    suma = 0
    multiplicador = 2
    for i in range(len(cuerpo) - 1, -1, -1):
        suma += int(cuerpo[i]) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1
        
    resto = suma % 11
    dv_calculado = 11 - resto
    
    if dv_calculado == 11:
        dv_esperado = "0"
    elif dv_calculado == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(dv_calculado)
        
    # Arreglo de digitos del cuerpo
    lista_digitos = [int(d) for d in cuerpo]
    
    # Determinar que DV usar para no romper la app en las pruebas
    dv_final = dv_ingresado
    mensaje_estado = f"RUT Valido Oficialmente. DV esperado: {dv_esperado}"
    
    if dv_ingresado != dv_esperado:
        # Si el usuario ingresa un DV incorrecto, el sistema lo corrige para permitir la simulacion
        dv_final = dv_esperado
        mensaje_estado = f"Modo Simulacion: DV corregido de '{dv_ingresado}' a '{dv_esperado}' para forzar calculos."
        
    # Asignar variable auxiliar v segun el DV corregido/esperado
    if dv_final == "K":
        v_auxiliar = 10
    elif dv_final == "0":
        v_auxiliar = 11
    else:
        v_auxiliar = int(dv_final)
        
    return True, lista_digitos, v_auxiliar, mensaje_estado

def generar_desglose_algebraico_local(A, B, D, E):
    desglose = "#### Desarrollo Directo: Ecuacion General a Canonica\n"
    desglose += "Ecuacion General determinada a partir de los digitos reales:\n"
    desglose += f"$$ ({round(A,3)})x^2 + ({round(B,3)})y^2 + ({round(D,3)})x + ({round(E,3)})y = 0 $$\n\n"
    
    desglose += "Asociacion de componentes variables:\n"
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
    
    desglose += "Completacion de cuadrados perfectos y equilibrio del miembro derecho:\n"
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

# 3. INTERFAZ VISUAL
st.title("SISTEMA DE EVALUACION MATEMATICA MODULAR")
st.caption("Evaluacion Integrada de Desempeño 1 | Departamento de Ingenieria Civil en Informatica")
st.markdown("---")

st.subheader("Ingreso de Credenciales de Usuario")
col_in, col_st = st.columns([2, 2], gap="large")

with col_in:
    # Caja libre interactiva
    rut_ingresado = st.text_input("Identificador (RUT con guion o continuo):", "21.451.190-8")
    ejecucion, digitos, v_aux, msg_sistema = procesar_rut_sistema(rut_ingresado)

with col_st:
    if ejecucion:
        st.success(f"Estado: {msg_sistema} | Auxiliar v = {v_aux}")
    else:
        st.error(f"Estado de Error: {msg_sistema}")

st.markdown("---")

if ejecucion:
    tab1, tab2, tab3 = st.tabs([
        "SECCIONES CONICAS", 
        "LIMITES Y CONTINUIDAD", 
        "VALIDACION DE COMPETENCIAS"
    ])
    
    # -------------------------------------------------------------------------
    # PESTAÑA 1: SECCIONES CÓNICAS
    # -------------------------------------------------------------------------
    with tab1:
        st.subheader("Modelamiento de la Seccion Conica")
        
        # Mapeo invertido asegurado para evitar desbordamiento de arreglos
        d8 = digitos[-1]
        d7 = digitos[-2] if len(digitos) >= 2 else 0
        d6 = digitos[-3] if len(digitos) >= 3 else 0
        d5 = digitos[-4] if len(digitos) >= 4 else 0
        d4 = digitos[-5] if len(digitos) >= 5 else 0
        d3 = digitos[-6] if len(digitos) >= 6 else 0
        d2 = digitos[-7] if len(digitos) >= 7 else 0
        d1 = digitos[-8] if len(digitos) >= 8 else 0
        
        A = (d1 + d2) / v_aux
        B = (d3 + d4) / v_aux
        C = -(d5 + d6)
        D = -(d7 + d8)
        E = d1 + d3 + d5 + d7
        
        lista_ajustes = []
        if (d5 + d6) % 3 == 0:
            if d7 % 2 == 0:
                B = 0
                lista_ajustes.append("Ajuste condicional: d5+d6 es multiplo de 3 y d7 es par. Se define B = 0 (Parabola vertical).")
            else:
                A = 0
                lista_ajustes.append("Ajuste condicional: d5+d6 es multiplo de 3 y d7 es impar. Se define A = 0 (Parabola horizontal).")
        elif d8 % 2 != 0:
            B = -B
            lista_ajustes.append("Ajuste condicional: d8 es impar. Se define B = -B para forzar una Hiperbola.")
        elif len(digitos) == 8 and d1 == d2:
            B = A
            lista_ajustes.append("Ajuste condicional: d1 = d2. Se define B = A para forzar una Circunferencia.")
            
        if A == 0 or B == 0:
            tipo_curva = "Parabola"
        elif A == B:
            tipo_curva = "Circunferencia"
        elif A * B < 0:
            tipo_curva = "Hiperbola"
        else:
            tipo_curva = "Elipse"
            
        c1, c2 = st.columns([1, 2], gap="medium")
        with c1:
            st.metric(label="Lugar Geometrico Determinado", value=tipo_curva)
            st.markdown("**Matriz de Coeficientes:**")
            st.code(f"A = {round(A,4)}\nB = {round(B,4)}\nC = {round(C,4)}\nD = {round(D,4)}\nE = {round(E,4)}", language="python")
        
        with c2:
            st.markdown("**Criterios de Consistencia Aplicados:**")
            if lista_ajustes:
                for aj in lista_ajustes:
                    st.info(aj)
            else:
                st.caption("Comportamiento natural: Coeficientes base determinados de forma lineal.")
                
        st.markdown("### Desarrollo Algebraico Compilado")
        col_des, col_gr = st.columns([3, 2], gap="large")
        
        with col_des:
            with st.container(border=True):
                st.markdown(generar_desglose_algebraico_local(A, B, D, E))
                
        with col_gr:
            with st.container(border=True):
                st.markdown("#### Proyeccion de la Curva")
                curva_puntos = [((x**2 * A) + (x * D)) * 0.05 for x in range(-30, 31)]
                st.line_chart(curva_puntos, use_container_width=True)
                st.caption("Representacion cartesiana estimada en base a los componentes cuadraticos.")
            
    # -------------------------------------------------------------------------
    # PESTAÑA 2: LÍMITES Y CONTINUIDAD
    # -------------------------------------------------------------------------
    with tab2:
        st.subheader("Analisis Funcional de Regiones por Tramo")
        
        residuo = d8 % 3
        if residuo == 0:
            caso_nombre, justificacion_caso = "Removible (Caso 1)", "d8 es multiplo de 3."
        elif residuo == 1:
            caso_nombre, justificacion_caso = "De Salto (Caso 2)", "d8 deja residuo 1 al dividirse por 3."
        else:
            caso_nombre, justificacion_caso = "Infinita (Caso 3)", "d8 deja residuo 2 al dividirse por 3."
            
        a_critico = float(d3)
        st.warning(f"Caso de Analisis Seleccionado: {caso_nombre} | Punto Critico a = {a_critico}")
        
        h_izq = [1.0, 0.1, 0.01, 0.001]
        h_der = [0.001, 0.01, 0.1, 1.0]
        
        t_izq = []
        for h in h_izq:
            x_v = a_critico - h
            y_v = x_v + (d1 if "Removible" in caso_nombre else d2 if "De Salto" in caso_nombre else 0)
            if "Infinita" in caso_nombre: y_v = (d5 + 1) / (x_v - a_critico)
            t_izq.append({"x": round(x_v, 3), "f(x)": round(y_v, 4)})
            
        t_der = []
        for h in h_der:
            x_v = a_critico + h
            y_v = x_v + (d1 if "Removible" in caso_nombre else d4 if "De Salto" in caso_nombre else d5)
            t_der.append({"x": round(x_v, 3), "f(x)": round(y_v, 4)})
            
        st.markdown("### Evidencia Numerica Lateral")
        c_t1, c_t2 = st.columns(2, gap="medium")
        with c_t1:
            with st.container(border=True):
                st.markdown("**Aproximacion por la Izquierda ($x \\to a^-$)**")
                st.table(t_izq)
        with c_t2:
            with st.container(border=True):
                st.markdown("**Aproximacion por la Derecha ($x \\to a^+$)**")
                st.table(t_der)

    # -------------------------------------------------------------------------
    # PESTAÑA 3: VALIDACIÓN DE COMPETENCIAS
    # -------------------------------------------------------------------------
    with tab3:
        st.subheader("Panel de Auditoria y Verificacion Analitica")
        st.caption("Formulario de contraste tecnico para evaluacion presencial.")
        
        with st.container(border=True):
            st.markdown("#### Componente A: Parametros del Lugar Geometrico")
            r1, r2, r3 = st.columns(3)
            with r1:
                st.text_input("Abscisa del Centro (h):", placeholder="Esperando entrada...", key="v_h")
            with r2:
                st.text_input("Ordenada del Centro (k):", placeholder="Esperando entrada...", key="v_k")
            with r3:
                st.text_input("Focos y Elementos Lineales:", placeholder="Ejemplo: F(h+c, k)", key="v_foc")
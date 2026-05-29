# -*- coding: utf-8 -*-
import streamlit as st

# 1. CONFIGURACIÓN DEL ENTORNO DE TRABAJO (TEMA NEGRO)
st.set_page_config(
    page_title="MAT1186 - Panel Analitico", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)


def procesar_rut_sistema(rut_input):
    # Si el usuario no ha escrito nada, mantenemos un estado neutro controlado
    if not rut_input.strip():
        return None, [0]*8, 1, "Esperando ingreso de credenciales..."

    rut_limpio = ""
    for caracter in rut_input:
        if caracter.isalnum():
            rut_limpio += caracter.upper()
            
    if len(rut_limpio) < 2:
        return False, [0]*8, 1, "RUT demasiado corto"
        
    cuerpo_str = rut_limpio[:-1]
    dv_ingresado = rut_limpio[-1]
    
    if not cuerpo_str.isdigit():
        return False, [0]*8, 1, "El cuerpo debe contener solo numeros"
        
    # Multiplicación y sumatoria manual para Módulo 11 (Página 2)
    suma = 0
    multiplicador = 2
    for i in range(len(cuerpo_str) - 1, -1, -1):
        suma += int(cuerpo_str[i]) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1
        
    resto = suma % 11
    dv_calculado = 11 - resto
    dv_esperado = "0" if dv_calculado == 11 else ("K" if dv_calculado == 10 else str(dv_calculado))
    
    # Manejo dinámico del largo del RUT (Soporta 7 u 8 dígitos rellenando con 0 a la izquierda) (Página 2)
    cuerpo_formateado = cuerpo_str.zfill(8)
    lista_digitos = [int(d) for d in cuerpo_formateado]
    
    dv_final = dv_ingresado
    mensaje_estado = f"RUT Valido Oficialmente. DV esperado: {dv_esperado}"
    
    if dv_ingresado != dv_esperado:
        dv_final = dv_esperado
        mensaje_estado = f"Modo Simulacion: DV corregido de '{dv_ingresado}' a '{dv_esperado}' para habilitar pruebas."
        
    
    if dv_final == "K":
        v_auxiliar = 10
    elif dv_final == "0":
        v_auxiliar = 11
    else:
        v_auxiliar = int(dv_final)
        
    return True, lista_digitos, v_auxiliar, mensaje_estado


def generar_desglose_algebraico_local(A, B, D, E):
    desglose = "#### Desarrollo Directo: Ecuacion General a Canonica\n"
    desglose += f"$$ ({round(A,3)})x^2 + ({round(B,3)})y^2 + ({round(D,3)})x + ({round(E,3)})y = 0 $$\n\n"
    desglose += f"Asociacion: $$ \\left[ ({round(A,3)})x^2 + ({round(D,3)})x \\right] + \\left[ ({round(B,3)})y^2 + ({round(E,3)})y \\right] = 0 $$\n\n"
    p_x = round(D / A, 4) if A != 0 else 0
    p_y = round(E / B, 4) if B != 0 else 0
    desglose += f"Factorizacion: $$ {round(A,3)}(x^2 + {p_x}x) + {round(B,3)}(y^2 + {p_y}y) = 0 $$\n\n"
    h = round(p_x / 2, 4)
    k = round(p_y / 2, 4)
    equi_x = round((h**2) * A, 4)
    equi_y = round((k**2) * B, 4)
    lado_derecho = round(equi_x + equi_y, 4)
    desglose += f"Completacion: $$ {round(A,3)}(x + {h})^2 + {round(B,3)}(y + {k})^2 = {lado_derecho} $$\n\n"
    den_x = round(lado_derecho / A, 4) if A != 0 else 1
    den_y = round(lado_derecho / B, 4) if B != 0 else 1
    desglose += f"Forma Canonica Estandar: $$ \\frac{{(x + {h})^2}}{{{den_x}}} + \\frac{{(y + {k})^2}}{{{den_y}}} = 1 $$\n\n"
    desglose += "#### Desarrollo Inverso: Ecuacion Canonica a General\n"
    desglose += f"$$ {den_y}(x + {h})^2 + {den_x}(y + {k})^2 = {round(den_x * den_y, 4)} $$\n\n"
    desglose += f"Ecuacion General Restablecida: $$ ({round(A,3)})x^2 + ({round(B,3)})y^2 + ({round(D,3)})x + ({round(E,3)})y = 0 $$\n"
    return desglose


st.title("SISTEMA DE EVALUACION MATEMATICA MODULAR")
st.caption("Evaluacion Integrada de Desempeño N°1 | Departamento de Ingenieria Civil en Informatica")
st.markdown("---")

st.subheader("Ingreso de Credenciales de Usuario")
col_in, col_st = st.columns([2, 2], gap="large")

with col_in:
    # Campo de texto modificado: Inicialmente vacío por defecto
    rut_ingresado = st.text_input("Identificador (Soporta 7 u 8 digitos con/sin guion):", value="")
    ejecucion, digitos, v_aux, msg_sistema = procesar_rut_sistema(rut_ingresado)

with col_st:
    if rut_ingresado.strip():
        if ejecucion:
            st.success(f"Estado: {msg_sistema} | Auxiliar v = {v_aux}")
        else:
            st.error(f"Estado de Error: {msg_sistema}")
    else:
        # Mensaje pasivo elegante mientras el campo esté vacío
        st.info("Sistema listo. Ingrese un identificador de usuario para inicializar los modulos analiticos.")

st.markdown("---")

# CONTROL DE FLUJO CONDICIONAL: Solo si el RUT es válido se monta el entorno matemático
if rut_ingresado.strip() and ejecucion:
    tab1, tab2, tab3 = st.tabs([
        "SECCIONES CONICAS", 
        "LIMITES Y CONTINUIDAD", 
        "VALIDACION DE COMPETENCIAS"
    ])
    
    
    d1, d2, d3, d4, d5, d6, d7, d8 = digitos
    
    # -------------------------------------------------------------------------
    # PESTAÑA 1: SECCIONES CÓNICAS (PÁGINA 3)
    # -------------------------------------------------------------------------
    with tab1:
        st.subheader("Modelamiento de la Seccion Conica")
        
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
            lista_ajustes.append("Ajuste condicional: d8 es impar. Se define B = -B para generar una Hiperbola.")
        elif d1 == d2 and d1 != 0:
            B = A
            lista_ajustes.append("Ajuste condicional: d1 = d2. Se define B = A para generar una Circunferencia.")
            
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
                st.caption("Comportamiento natural: Coeficientes determinados de forma directa por la estructura del RUT.")
                
        st.markdown("### Desarrollo Algebraico Compilado (Ida y Vuelta)")
        col_des, col_gr = st.columns([3, 2], gap="large")
        
        with col_des:
            with st.container(border=True):
                st.markdown(generar_desglose_algebraico_local(A, B, D, E))
                
        with col_gr:
            with st.container(border=True):
                st.markdown("#### Proyeccion de la Curva")
                curva_puntos = [((x**2 * A) + (x * D)) * 0.05 for x in range(-30, 31)]
                st.line_chart(curva_puntos, use_container_width=True)

    # -------------------------------------------------------------------------
    # PESTAÑA 2: LÍMITES Y CONTINUIDAD (FASE 6 - PÁGINAS 7 Y 8)
    # -------------------------------------------------------------------------
    with tab2:
        st.subheader("Modulo de Analisis Funcional por Tramo")
        
        residuo_limite = d8 % 3
        a_critico = float(d3)
        
        if residuo_limite == 0:
            caso_nombre = "Caso 1: Discontinuidad Removible"
            justificacion_caso = f"d8 ({d8}) es multiplo de 3."
        elif residuo_limite == 1:
            caso_nombre = "Caso 2: Discontinuidad de Salto"
            justificacion_caso = f"d8 ({d8}) deja residuo 1 al dividirse por 3."
        else:
            caso_nombre = "Caso 3: Discontinuidad Infinita"
            justificacion_caso = f"d8 ({d8}) deja residuo 2 al dividirse por 3."
            
        st.warning(f"Entorno Activo: {caso_nombre} | Punto Critico de Analisis a = {a_critico}")
        st.caption(f"Justificacion algoritmica de seleccion: {justificacion_caso}")
        
        st.markdown("### Justificacion Algebraica Automatizada")
        with st.container(border=True):
            if residuo_limite == 0:
                st.markdown(f"**Ecuacion por tramos asignada :**")
                st.markdown(f"$$ f_1(x) = \\frac{{(x - {a_critico})(x + {d1})}}{{x - {a_critico}}} \\quad \\text{{si }} x < {a_critico} $$")
                st.markdown(f"$$ f_2(x) = x + {d1} \\quad \\text{{si }} x \\ge {a_critico} $$")
                st.markdown("**Procedimiento de Simplificacion Manual:**")
                st.info(f"Al evaluar x = {a_critico}, f_1({a_critico}) se indetermina de la forma 0/0. Cancelando el factor común lineal (x - {a_critico}), la expresión se reduce a x + {d1}. Por tanto, el limite por izquierda existe y es {a_critico + d1}, coincidiendo con el tramo derecho. La discontinuidad es removible porque f({a_critico}) original no esta definida.")
            elif residuo_limite == 1:
                st.markdown(f"**Ecuacion por tramos asignada :**")
                st.markdown(f"$$ f(x) = \\begin{{cases}} x + {d2} & \\text{{si }} x < {a_critico} \\\\ x + {d4} & \\text{{si }} x \\ge {a_critico} \\end{{cases}} $$")
                st.markdown("**Analisis de Limites Laterales:**")
                st.info(f"Limite izquierdo: {a_critico} + {d2} = {a_critico + d2}. Limite derecho: {a_critico} + {d4} = {a_critico + d4}. Al ser distintos, se comprueba analiticamente la existencia de un salto finito en el punto de corte.")
            else:
                st.markdown(f"**Ecuacion por tramos asignada:**")
                st.markdown(f"$$ f_1(x) = \\frac{{{d5} + 1}}{{x - {a_critico}}} \\quad \\text{{si }} x < {a_critico} $$")
                st.markdown(f"$$ f_2(x) = x + {d5} \\quad \\text{{si }} x \\ge {a_critico} $$")
                st.markdown("**Analisis Asintotico:**")
                st.info(f"El denominator del primer tramo tiende a 0 al aproximarse por la izquierda, haciendo que f(x) decrezca hacia $-\\infty$. Esto confirma analiticamente una Asintota Vertical en x = {a_critico}.")

        
        h_izq = [1.0, 0.1, 0.01, 0.001]
        h_der = [0.001, 0.01, 0.1, 1.0]
        
        t_izq = []
        for h in h_izq:
            x_v = a_critico - h
            if residuo_limite == 0:   y_v = x_v + d1
            elif residuo_limite == 1: y_v = x_v + d2
            else:                     y_v = (d5 + 1) / (x_v - a_critico)
            t_izq.append({"x": round(x_v, 3), "f(x)": round(y_v, 4)})
            
        t_der = []
        for h in h_der:
            x_v = a_critico + h
            y_v = x_v + (d1 if residuo_limite == 0 else d4 if residuo_limite == 1 else d5)
            t_der.append({"x": round(x_v, 3), "f(x)": round(y_v, 4)})
            
        st.markdown("### Evidencia Numerica Lateral (Contraste)")
        c_t1, c_t2 = st.columns(2, gap="medium")
        with c_t1:
            with st.container(border=True):
                st.markdown("**Aproximacion por la Izquierda ($x \\to a^-$)**")
                st.table(t_izq)
        with c_t2:
            with st.container(border=True):
                st.markdown("**Aproximacion por la Derecha ($x \\to a^+$)**")
                st.table(t_der)
            
        st.markdown("### Representacion Grafica por Tramos")
        with st.container(border=True):
            puntos_eje_y = []
            rango_x = [a_critico + (step / 10.0) for step in range(-20, 21)]
            for x in rango_x:
                if x < a_critico:
                    if residuo_limite == 0:   y_val = x + d1
                    elif residuo_limite == 1: y_val = x + d2
                    else:                     y_val = (d5 + 1) / (x - a_critico)
                else:
                    if residuo_limite == 0:   y_val = x + d1
                    elif residuo_limite == 1: y_val = x + d4
                    else:                     y_val = x + d5
                puntos_eje_y.append(y_val if (y_val is not None and abs(y_val) < 150) else None)
            st.line_chart(puntos_eje_y, use_container_width=True)

    # -------------------------------------------------------------------------
    # PESTAÑA 3: VALIDACIÓN DE COMPETENCIAS (CAMPOS VACÍOS OBLIGATORIOS)
    # -------------------------------------------------------------------------
    with tab3:
        st.subheader("Panel de Auditoria y Verificacion Analitica")
        st.caption("Campos en blanco obligatorios.")
        
        with st.container(border=True):
            st.markdown("#### Componente A: Elementos Estructurales de la Conica")
            r1, r2, r3 = st.columns(3)
            with r1:
                st.text_input("Ubicacion del Centro u Origen (h, k):", placeholder="Esperando analisis...", key="v_h")
            with r2:
                st.text_input("Coordenadas de los Vertices:", placeholder="Esperando analisis...", key="v_k")
            with r3:
                st.text_input("Coordenadas de los Focos Asociados:", placeholder="Ejemplo: F(h+c, k)", key="v_foc")
                
        st.markdown("## ")
        
        with st.container(border=True):
            st.markdown("#### Componente B: Comportamiento de Limites y Continuidad")
            r4, r5, r6 = st.columns(3)
            with r4:
                st.text_input("Valor del Limite Lateral Izquierdo:", placeholder="Numerico o infinito...", key="v_lizq")
            with r5:
                st.text_input("Valor del Limite Lateral Derecho:", placeholder="Numerico o infinito...", key="v_lder")
            with r6:
                st.selectbox(
                    "Dictamen Final de Continuidad:", 
                    [
                        "Seleccione una alternativa...", 
                        "Funcion Continua en el punto de corte", 
                        "Discontinuidad Evitable / Removible", 
                        "Discontinuidad de Salto Finito", 
                        "Discontinuidad Esencial / Infinita"
                    ], 
                    key="v_cont"
                )
elif rut_ingresado.strip() and not ejecucion:
    # Si escribieron un texto pero no es numerico o es mas corto que un RUT basico
    st.info("Estructurando entorno seguro. Por favor ingrese un formato de RUT valido.")
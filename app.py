# -*- coding: utf-8 -*-
import streamlit as st
from modulos.validador_rut import validar_y_procesar_rut
from modulos.conicas import aplicar_reglas_ajuste, clasificar_conica_final, generar_desglose_algebraico

st.set_page_config(
    page_title="MAT1186 - Panel Analitico", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

st.title("SISTEMA DE EVALUACION MATEMATICA MODULAR")
st.caption("Evaluacion Integrada de Desempeño N°1 | Departamento de Ingenieria Civil en Informatica")
st.markdown("---")

st.subheader("Ingreso de Credenciales de Usuario")
col_in, col_st = st.columns([2, 2], gap="large")

with col_in:
    rut_ingresado = st.text_input("Identificador (Soporta 7 u 8 digitos con/sin guion):", value="")

ejecucion = False
digitos = [0]*8
v_aux = 1
texto_pasos_rut = ""

if rut_ingresado.strip():
    es_valido, digitos_raw, v_aux, texto_pasos_rut = validar_y_procesar_rut(rut_ingresado)
    cuerpo_formateado = "".join(str(d) for d in digitos_raw).zfill(8)
    digitos = [int(d) for d in cuerpo_formateado]
    ejecucion = True 
    
    with col_st:
        if es_valido:
            st.success(f"Estado: RUT Valido Oficialmente | Auxiliar v = {v_aux}")
        else:
            st.warning(f"Modo Simulacion Activo (DV Corregido) | Auxiliar v = {v_aux}")
else:
    with col_st:
        st.info("Sistema listo. Ingrese un identificador de usuario para inicializar los modulos analiticos.")

st.markdown("---")

if rut_ingresado.strip() and ejecucion:
    tab1, tab2, tab3 = st.tabs([
        "SECCIONES CONICAS", 
        "LIMITES Y CONTINUIDAD", 
        "VALIDACION DE COMPETENCIAS"
    ])
    
    d1, d2, d3, d4, d5, d6, d7, d8 = digitos
    
    with tab1:
        st.subheader("Modelamiento de la Seccion Conica")
        
        A_base = (d1 + d2) / v_aux
        B_base = (d3 + d4) / v_aux
        C_base = -(d5 + d6)
        D_base = -(d7 + d8)
        E_base = d1 + d3 + d5 + d7
        
        A, B, C, lista_ajustes = aplicar_reglas_ajuste(A_base, B_base, C_base, digitos)
        tipo_curva = clasificar_conica_final(A, B)
            
        c1, c2 = st.columns([1, 2], gap="medium")
        with c1:
            st.metric(label="Lugar Geometrico Determinado", value=tipo_curva)
            st.markdown("**Matriz de Coeficientes Final:**")
            st.code(f"A = {round(A,4)}\nB = {round(B,4)}\nC = {round(C,4)}\nD = {round(D_base,4)}\nE = {round(E_base,4)}", language="python")
        
        with c2:
            st.markdown("**Procedimiento de Validacion de Credenciales:**")
            with st.expander("Ver sumatoria manual Módulo 11"):
                st.text(texto_pasos_rut)
                
            if lista_ajustes:
                st.markdown("**Criterios de Consistencia Aplicados:**")
                for aj in lista_ajustes:
                    st.info(aj)
                
        st.markdown("### Desarrollo Algebraico Compilado (Ida y Vuelta)")
        col_des, col_gr = st.columns([3, 2], gap="large")
        
        with col_des:
            with st.container(border=True):
                st.markdown(generar_desglose_algebraico(A, B, C, D_base, E_base, tipo_curva))
                
        with col_gr:
            with st.container(border=True):
                st.markdown("#### Proyeccion de la Curva")
                if A == 0 and B != 0:
                    curva_puntos = [((x**2 * B) + (x * E_base)) * 0.05 for x in range(-30, 31)]
                else:
                    curva_puntos = [((x**2 * A) + (x * D_base)) * 0.05 for x in range(-30, 31)]
                st.line_chart(curva_puntos, use_container_width=True)

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
                st.markdown(f"**Ecuacion por tramos asignada:**")
                st.markdown(f"$$ f_1(x) = \\frac{{(x - {a_critico})(x + {d1})}}{{x - {a_critico}}} \\quad \\text{{si }} x < {a_critico} $$")
                st.markdown(f"$$ f_2(x) = x + {d1} \\quad \\text{{si }} x \\ge {a_critico} $$")
                st.markdown("**Procedimiento de Simplificacion Manual:**")
                st.info(f"Al evaluar x = {a_critico}, f_1({a_critico}) se indetermina de la forma 0/0. Cancelando el factor común lineal (x - {a_critico}), la expresión se reduce a x + {d1}. Por tanto, el limite por izquierda existe y es {a_critico + d1}, coincidiendo con el tramo derecho. La discontinuidad es removible porque f({a_critico}) original no esta definida.")
            elif residuo_limite == 1:
                st.markdown(f"**Ecuacion por tramos asignada:**")
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

    with tab3:
        st.subheader("Panel de Auditoria y Verificacion Analitica")
        st.caption("Campos en blanco obligatorios de acuerdo a las Fases 4 y 6 de la rubrica.")
        
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
    st.info("Estructurando entorno seguro. Por favor ingrese un formato de RUT valido.")
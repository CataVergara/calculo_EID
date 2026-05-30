# -*- coding: utf-8 -*-
import streamlit as st
from modulos.validador_rut import validar_y_procesar_rut
from modulos.conicas import (
    generar_coeficientes,
    aplicar_reglas_ajuste,
    calcular_discriminante,
    clasificar_conica,
    completar_cuadrados,
    generar_desglose_algebraico,
    generar_texto_elementos
)
from modulos.graficador import crear_datos_grafico

st.set_page_config(
    page_title="MAT1186 - Panel Analitico",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("SISTEMA DE EVALUACION MATEMATICA MODULAR")
st.caption("Evaluacion Integrada de Desempeno N°1 | Departamento de Ingenieria Civil en Informatica")
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

        A_base, B_base, C_base, D_base, E_base, F_base = generar_coeficientes(digitos, v_aux)
        A, B, C, lista_ajustes = aplicar_reglas_ajuste(A_base, B_base, C_base, digitos)
        disc = calcular_discriminante(A, B, C)
        tipo_curva = clasificar_conica(A, B, C)

        st.markdown(f"**Lugar Geometrico Determinado:** `{tipo_curva}`")
        st.markdown(f"**Discriminante (B² - 4AC):** `{round(disc, 6)}`")

        c1, c2, c3 = st.columns([1, 1, 1], gap="medium")
        with c1:
            st.markdown("**Coeficientes de la Ecuacion General:**")
            st.code(
                f"A (x²) = {round(A,6)}\n"
                f"B (xy) = {round(B,6)}\n"
                f"C (y²) = {round(C,6)}\n"
                f"D (x)  = {round(D_base,6)}\n"
                f"E (y)  = {round(E_base,6)}\n"
                f"F      = {round(F_base,6)}",
                language="python"
            )

        with c2:
            st.markdown("**Interpretacion del Discriminante:**")
            if abs(disc) < 1e-12:
                st.info(f"B² - 4AC = {disc} = 0 → Parabola")
            elif disc < 0:
                if abs(A - C) < 1e-12 and abs(B) < 1e-12 and abs(A) > 1e-12:
                    st.info(f"B² - 4AC = {disc} < 0 y A = C → Circunferencia")
                else:
                    st.info(f"B² - 4AC = {disc} < 0 → Elipse")
            else:
                st.info(f"B² - 4AC = {disc} > 0 → Hiperbola")

        with c3:
            st.markdown("**Procedimiento de Validacion de Credenciales:**")
            with st.expander("Ver sumatoria manual Modulo 11"):
                st.text(texto_pasos_rut)

            if lista_ajustes:
                st.markdown("**Criterios de Consistencia Aplicados:**")
                for aj in lista_ajustes:
                    st.info(aj)

        st.markdown("### Desarrollo Algebraico: General → Canonica")
        col_des, col_gr = st.columns([3, 2], gap="large")

        with col_des:
            with st.container(border=True):
                params = completar_cuadrados(A, B, C, D_base, E_base, F_base, tipo_curva)
                desglose = generar_desglose_algebraico(A, B, C, D_base, E_base, F_base, tipo_curva, params)
                st.markdown(desglose)

        with col_gr:
            with st.container(border=True):
                st.markdown("#### Proyeccion de la Curva")
                datos_grafico = crear_datos_grafico(tipo_curva, params)
                curva = datos_grafico["curva"]
                if curva:
                    pts_x = [p["x"] for p in curva]
                    pts_y = [p["y"] for p in curva]
                    st.line_chart({"x": pts_x, "y": pts_y}, x="x", y="y", use_container_width=True)
                else:
                    st.warning("No se pudieron generar puntos para la grafica.")

        st.markdown("### Elementos Geometricos de la Conica")
        with st.container(border=True):
            texto_elem = generar_texto_elementos(params)
            st.markdown(texto_elem)

        st.markdown("### Representacion Visual de Elementos")
        with st.container(border=True):
            datos_graf = crear_datos_grafico(tipo_curva, params)
            elementos_pts = datos_graf["elementos"]
            asintotas_pts = datos_graf["asintotas"]

            if elementos_pts:
                st.markdown("**Puntos de interes:**")
                e_x = [p["x"] for p in elementos_pts]
                e_y = [p["y"] for p in elementos_pts]
                e_labels = [p["label"] for p in elementos_pts]
                st.scatter_chart(
                    {"x": e_x, "y": e_y, "elemento": e_labels},
                    x="x", y="y", color="elemento",
                    use_container_width=True
                )
            else:
                st.info("Datos de elementos geometricos no disponibles.")

            if asintotas_pts:
                st.markdown("**Asintotas:**")
                a_x = [p["x"] for p in asintotas_pts]
                a_y = [p["y"] for p in asintotas_pts]
                st.line_chart({"x": a_x, "y": a_y}, x="x", y="y", use_container_width=True)

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
                st.markdown("**Ecuacion asignada (discontinuidad removible):**")
                st.markdown(f"$$ f(x) = \\frac{{(x - {a_critico})(x + {d1})}}{{x - {a_critico}}}, \\quad x \\neq {a_critico} $$")
                st.markdown("**Procedimiento:**")
                st.info(
                    f"1. En x = {a_critico}, el denominador se anula: f({a_critico}) = 0/0 (indeterminacion).\n\n"
                    f"2. Simplificando algebraicamente: f(x) = x + {d1}, x ≠ {a_critico}.\n\n"
                    f"3. El limite cuando x→{a_critico} existe y vale {a_critico + d1}, "
                    f"pero f({a_critico}) no esta definida (agujero).\n\n"
                    f"4. Por tanto, la discontinuidad es **removible**."
                )
            elif residuo_limite == 1:
                st.markdown("**Ecuacion por tramos asignada:**")
                st.markdown(f"$$ f(x) = \\begin{{cases}} x + {d2} & \\text{{si }} x < {a_critico} \\\\ x + {d4} & \\text{{si }} x \\ge {a_critico} \\end{{cases}} $$")
                st.markdown("**Analisis de Limites Laterales:**")
                st.info(
                    f"Limite izquierdo: lim_(x→{a_critico}⁻) (x + {d2}) = {a_critico + d2}.\n\n"
                    f"Limite derecho: lim_(x→{a_critico}⁺) (x + {d4}) = {a_critico + d4}.\n\n"
                    f"Al ser {a_critico + d2} ≠ {a_critico + d4}, el limite bilateral no existe.\n\n"
                    f"Se comprueba analiticamente la existencia de un **salto finito** en x = {a_critico}."
                )
            else:
                st.markdown("**Ecuacion asignada (discontinuidad infinita):**")
                st.markdown(f"$$ f(x) = \\frac{{{d5} + 1}}{{x - {a_critico}}}, \\quad x \\neq {a_critico} $$")
                st.markdown("**Analisis Asintotico:**")
                st.info(
                    f"1. Cuando x→{a_critico}⁻, el denominador (x - {a_critico}) → 0⁻, "
                    f"por lo que f(x) → -∞.\n\n"
                    f"2. Cuando x→{a_critico}⁺, el denominador (x - {a_critico}) → 0⁺, "
                    f"por lo que f(x) → +∞.\n\n"
                    f"3. Los limites laterales son infinitos y de distinto signo.\n\n"
                    f"4. Existe una **asintota vertical** en x = {a_critico}. "
                    f"La discontinuidad es **infinita/esencial**."
                )

        h_izq = [1.0, 0.1, 0.01, 0.001]
        h_der = [0.001, 0.01, 0.1, 1.0]

        t_izq = []
        for h in h_izq:
            x_v = a_critico - h
            if residuo_limite == 0:
                if abs(x_v - a_critico) < 1e-12:
                    y_v = None
                else:
                    y_v = (x_v - a_critico) * (x_v + d1) / (x_v - a_critico)
            elif residuo_limite == 1:
                y_v = x_v + d2
            else:
                y_v = (d5 + 1) / (x_v - a_critico)
            t_izq.append({"x": round(x_v, 3), "f(x)": round(y_v, 4) if y_v is not None else "No def."})

        t_der = []
        for h in h_der:
            x_v = a_critico + h
            if residuo_limite == 0:
                if abs(x_v - a_critico) < 1e-12:
                    y_v = None
                else:
                    y_v = (x_v - a_critico) * (x_v + d1) / (x_v - a_critico)
            elif residuo_limite == 1:
                y_v = x_v + d4
            else:
                y_v = (d5 + 1) / (x_v - a_critico)
            t_der.append({"x": round(x_v, 3), "f(x)": round(y_v, 4) if y_v is not None else "No def."})

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
                if abs(x - a_critico) < 1e-12:
                    puntos_eje_y.append(None)
                    continue
                if x < a_critico:
                    if residuo_limite == 0:
                        y_val = (x - a_critico) * (x + d1) / (x - a_critico)
                    elif residuo_limite == 1:
                        y_val = x + d2
                    else:
                        y_val = (d5 + 1) / (x - a_critico)
                else:
                    if residuo_limite == 0:
                        y_val = (x - a_critico) * (x + d1) / (x - a_critico)
                    elif residuo_limite == 1:
                        y_val = x + d4
                    else:
                        y_val = (d5 + 1) / (x - a_critico)
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
            st.markdown("**Complete los siguientes campos manualmente durante la defensa:**")
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

            st.markdown("---")
            r7, r8, r9 = st.columns(3)
            with r7:
                st.text_input("Valor de f(a) en el punto critico:", placeholder="Indefinido / valor numerico...", key="v_fa")
            with r8:
                st.text_input("El limite bilateral existe:", placeholder="Si / No / No aplica...", key="v_existe")
            with r9:
                st.text_input("Justificacion matematica:", placeholder="Escriba su justificacion...", key="v_just")

elif rut_ingresado.strip() and not ejecucion:
    st.info("Estructurando entorno seguro. Por favor ingrese un formato de RUT valido.")

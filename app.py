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
from modulos.limites import (
    identificar_caso_discontinuidad,
    generar_tabla_aproximacion,
    generar_puntos_grafica,
    generar_texto_justificacion
)

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
                ejes = datos_grafico["ejes"]
                if curva:
                    pts_x = [p["x"] for p in curva] + [p["x"] for p in ejes]
                    pts_y = [p["y"] for p in curva] + [p["y"] for p in ejes]
                    pts_s = ["curva"] * len(curva) + [p["label"] for p in ejes]
                    st.line_chart(
                        {"x": pts_x, "y": pts_y, "serie": pts_s},
                        x="x", y="y", color="serie",
                        use_container_width=True
                    )
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
            ejes = datos_graf["ejes"]

            tx, ty, ts = [], [], []
            for p in ejes:
                tx.append(p["x"]); ty.append(p["y"]); ts.append(p["label"])
            if asintotas_pts:
                for p in asintotas_pts:
                    tx.append(p["x"]); ty.append(p["y"]); ts.append("asintota")
            if elementos_pts:
                for p in elementos_pts:
                    tx.append(p["x"]); ty.append(p["y"]); ts.append(p["label"])

            if tx:
                st.line_chart(
                    {"x": tx, "y": ty, "serie": ts},
                    x="x", y="y", color="serie",
                    use_container_width=True
                )
            if not elementos_pts:
                st.info("Datos de elementos geometricos no disponibles.")

    with tab2:
        st.subheader("Modulo de Analisis Funcional por Tramo")

        a_critico = float(d3)
        caso, justificacion_caso = identificar_caso_discontinuidad(d8)
        if "Removible" in caso:
            caso_nombre = "Caso 1: Discontinuidad Removible"
        elif "De Salto" in caso:
            caso_nombre = "Caso 2: Discontinuidad de Salto"
        else:
            caso_nombre = "Caso 3: Discontinuidad Infinita"

        st.warning(f"Entorno Activo: {caso_nombre} | Punto Critico de Analisis a = {a_critico}")
        st.caption(f"Justificacion algoritmica de seleccion: {justificacion_caso}")

        st.markdown("### Justificacion Algebraica Automatizada")
        with st.container(border=True):
            texto_just = generar_texto_justificacion(caso, digitos, a_critico)
            if "Removible" in caso:
                st.markdown(f"$$ f(x) = \\frac{{(x - {a_critico})(x + {d1})}}{{x - {a_critico}}}, \\quad x \\neq {a_critico} $$")
                st.markdown("**Procedimiento:**")
            elif "De Salto" in caso:
                st.markdown(f"$$ f(x) = \\begin{{cases}} x + {d2} & \\text{{si }} x < {a_critico} \\\\ x + {d4} & \\text{{si }} x \\ge {a_critico} \\end{{cases}} $$")
                st.markdown("**Analisis de Limites Laterales:**")
            else:
                st.markdown(f"$$ f(x) = \\frac{{{d5} + 1}}{{x - {a_critico}}}, \\quad x \\neq {a_critico} $$")
                st.markdown("**Analisis Asintotico:**")
            st.info(texto_just)

        t_izq, t_der = generar_tabla_aproximacion(caso, digitos, a_critico)

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
            puntos_eje_y = generar_puntos_grafica(caso, digitos, a_critico, rango=2.0, pasos=40)
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

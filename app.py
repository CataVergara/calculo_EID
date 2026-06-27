# -*- coding: utf-8 -*-
import streamlit as st
from modulos.validador_rut import validar_y_procesar_rut
from modulos.conicas import (
    generar_coeficientes,
    aplicar_reglas_ajuste,
    aplicar_reglas_individualmente,
    clasificar_conica,
    completar_cuadrados,
    generar_desglose_algebraico,
    generar_texto_elementos
)
from modulos.graficador import crear_datos_grafico
from modulos.limites import (
    obtener_tabla_aproximacion,
    obtener_puntos_grafica,
    obtener_texto_justificacion
)

st.set_page_config(
    page_title="MAT1186 - Análisis de Cónicas",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #f0f2f6;
        padding: 6px 10px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    }
    /* Metric cards */
    [data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 10px 14px;
    }
    /* Expander */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #495057;
    }
    /* Containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 100%);
            color: white; padding: 22px 30px; border-radius: 14px; margin-bottom: 18px;">
    <h2 style="margin:0; font-size:1.6rem; letter-spacing:0.5px;"> Sistema de Análisis Matemático Modular</h2>
    <p style="margin:6px 0 0 0; opacity:0.85; font-size:0.9rem;">
        Evaluación Integrada de Desempeño N°1 &nbsp;·&nbsp;
        MAT1186 Introducción al Cálculo &nbsp;·&nbsp;
        Ingeniería Civil en Informática
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("###  Ingreso de RUT")
col_in, col_st = st.columns([2, 2], gap="large")

with col_in:
    rut_ingresado = st.text_input("RUT (con o sin guion, ej: 12345678-9 o 12345678K):", value="", placeholder="Ej: 12345678-9", max_chars=10)

ejecucion = False
digitos = [0]*8
v_aux = 1
texto_pasos_rut = ""

# Sanitizar entrada: solo números, K y guión
rut_sanitizado = "".join(c.upper() for c in rut_ingresado if c.isdigit() or c.upper() == 'K' or c == '-')
if rut_sanitizado != rut_ingresado and rut_ingresado.strip():
    with col_st:
        st.warning("Atención: Se permiten solo números, K y guión (-)")
    rut_ingresado = rut_sanitizado

if rut_ingresado.strip():
    es_valido, digitos_raw, v_aux, texto_pasos_rut = validar_y_procesar_rut(rut_ingresado)
    
    if not es_valido:
        with col_st:
            st.error(texto_pasos_rut)
        ejecucion = False
    else:
        cuerpo_formateado = "".join(str(d) for d in digitos_raw).zfill(8)
        digitos = [int(d) for d in cuerpo_formateado]
        ejecucion = True
        with col_st:
            st.success(f"OK RUT Válido | Dígitos: {cuerpo_formateado} | Variable auxiliar: v = {v_aux}")
            if v_aux == 10:
                st.markdown("> **Nota:** El dígito verificador K representa v_auxiliar = 10 en los cálculos")
else:
    with col_st:
        st.info("Sistema listo. Ingrese un identificador de usuario para inicializar los modulos analiticos.")

st.markdown("---")

if rut_ingresado.strip() and ejecucion:
    tab1, tab2, tab3 = st.tabs([
        " Secciones Cónicas",
        " Límites y Continuidad",
        " Validación de Competencias"
    ])

    d1, d2, d3, d4, d5, d6, d7, d8 = digitos

    with tab1:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #e8f4f8 0%, #f0f8ee 100%);
                    padding:16px 20px; border-radius:12px; margin-bottom:16px;">
        <h3 style="margin:0; color:#1e3a5f;"> Fase 1: Modelamiento de la Sección Cónica</h3>
        </div>""", unsafe_allow_html=True)

        A_base, B_base, C_base, D_base, E_base, F_base = generar_coeficientes(digitos, v_aux)
        A, B, C, D, E, lista_ajustes = aplicar_reglas_ajuste(A_base, B_base, C_base, D_base, E_base, digitos)
        tipo_curva = clasificar_conica(A, B)

        colores = {"Circunferencia": "#2196F3", "Elipse": "#4CAF50", "Hiperbola": "#F44336", "Parabola": "#FF9800"}
        color_badge = colores.get(tipo_curva, "#607D8B")
        st.markdown(
            f'<div style="display:inline-block; background:{color_badge}; color:white; '
            f'padding:8px 24px; border-radius:25px; font-weight:700; font-size:1.1rem; margin:12px 0 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">'
            f'Cónica Identificada: {tipo_curva}</div>',
            unsafe_allow_html=True
        )

        with st.container(border=True):
            st.markdown("### Coeficientes de la Ecuación General")
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("A (x²)", round(A, 4))
            m2.metric("B (y²)", round(B, 4))
            m3.metric("C (x)", round(C, 4))
            m4.metric("D (y)", round(D, 4))
            m5.metric("E", round(E, 4))
            
            st.divider()
            
            with st.expander(" Ver construcción paso a paso de coeficientes"):
                st.markdown(
                    f"**Fórmulas aplicadas (Fase 1):**\n\n"
                    f"- $A = \\frac{{d_1 + d_2}}{{v}} = \\frac{{{d1} + {d2}}}{{{v_aux}}} = {round(A_base, 6)}$\n\n"
                    f"- $B = \\frac{{d_3 + d_4}}{{v}} = \\frac{{{d3} + {d4}}}{{{v_aux}}} = {round(B_base, 6)}$\n\n"
                    f"- $C = -(d_5 + d_6) = -({d5} + {d6}) = {round(C_base, 6)}$\n\n"
                    f"- $D = -(d_7 + d_8) = -({d7} + {d8}) = {round(D_base, 6)}$\n\n"
                    f"- $E = d_1 + d_3 + d_5 + d_7 = {d1} + {d3} + {d5} + {d7} = {round(E_base, 6)}$\n\n"
                    f"**Variable auxiliar:** $v = {v_aux}$ "
                    f"({'DV = K' if v_aux == 10 else 'DV = 0' if v_aux == 11 else f'DV = {v_aux}'})"
                )

        st.markdown("")
        
        with st.container(border=True):
            st.markdown("### Validación de Credenciales (Módulo 11)")
            with st.expander("OK Ver sumatoria manual del Módulo 11", expanded=False):
                st.code(texto_pasos_rut, language="text")

            resultados_individuales = aplicar_reglas_individualmente(A_base, B_base, C_base, D_base, E_base, digitos)

            if resultados_individuales:
                st.markdown("### Resultados por Criterio de Consistencia")
                for idx, (A_r, B_r, C_r, D_r, E_r, desc) in enumerate(resultados_individuales, 1):
                    tipo_r = clasificar_conica(A_r, B_r)
                    color_r = colores.get(tipo_r, "#607D8B")
                    with st.container(border=True):
                        cols = st.columns([3, 1])
                        with cols[0]:
                            st.markdown(f"**Resultado {idx}:** {desc}")
                        with cols[1]:
                            st.markdown(
                                f'<div style="text-align:right;">'
                                f'<span style="display:inline-block; background:{color_r}; color:white; '
                                f'padding:4px 14px; border-radius:15px; font-weight:600; font-size:0.85rem;">'
                                f'{tipo_r}</span></div>',
                                unsafe_allow_html=True
                            )

                        c1, c2, c3, c4, c5 = st.columns(5)
                        c1.metric("A (x²)", round(A_r, 4))
                        c2.metric("B (y²)", round(B_r, 4))
                        c3.metric("C (x)", round(C_r, 4))
                        c4.metric("D (y)", round(D_r, 4))
                        c5.metric("E", round(E_r, 4))

                        with st.expander("Ver desarrollo algebraico, gráfico y elementos geométricos"):
                            try:
                                params_r = completar_cuadrados(A_r, B_r, C_r, D_r, E_r, tipo_r)
                                desglose_r = generar_desglose_algebraico(A_r, B_r, C_r, D_r, E_r, tipo_r, params_r)
                                st.markdown(desglose_r)

                                datos_r = crear_datos_grafico(tipo_r, params_r)
                                curva_r = datos_r["curva"]
                                if curva_r:
                                    pts_x = [p["x"] for p in curva_r]
                                    pts_y = [p["y"] for p in curva_r]
                                    st.line_chart({"x": pts_x, "y": pts_y}, x="x", y="y", use_container_width=True)

                                st.markdown("**Elementos Geométricos:**")
                                st.markdown(generar_texto_elementos(params_r))
                            except Exception as err:
                                st.warning(f"No se pudo generar el desarrollo completo: {err}")

        st.markdown("")
        st.divider()
        st.markdown("")

        st.markdown("""
        <div style="background:linear-gradient(135deg, #f0f2e8 0%, #f8f6f0 100%);
                    padding:16px 20px; border-radius:12px; margin-bottom:16px;">
        <h3 style="margin:0; color:#5d4e37;"> Fase 2: Desarrollo Algebraico (General → Canónica)</h3>
        </div>""", unsafe_allow_html=True)

        col_des, col_gr = st.columns([3, 2], gap="large")

        with col_des:
            with st.container(border=True):
                try:
                    params = completar_cuadrados(A, B, C, D, E, tipo_curva)
                    desglose = generar_desglose_algebraico(A, B, C, D, E, tipo_curva, params)
                    st.markdown(desglose)
                except Exception as err:
                    st.error(f"Error: Error al calcular forma canónica: {err}")
                    params = {"tipo": tipo_curva}

        with col_gr:
            with st.container(border=True):
                st.markdown("####  Gráfico de la Curva")
                try:
                    datos_grafico = crear_datos_grafico(tipo_curva, params)
                    curva = datos_grafico["curva"]
                    ejes = datos_grafico.get("ejes", [])
                    if curva:
                        pts_x = [p["x"] for p in curva] + [p["x"] for p in ejes]
                        pts_y = [p["y"] for p in curva] + [p["y"] for p in ejes]
                        pts_s = ["curva"] * len(curva) + [p["label"] for p in ejes]
                        st.line_chart(
                            {"x": pts_x, "y": pts_y, "serie": pts_s},
                            x="x", y="y", color="serie",
                            use_container_width=True
                        )
                    elif tipo_curva == "Circunferencia" and params.get("punto", False):
                        h_v, k_v = params.get("h", 0), params.get("k", 0)
                        st.info("Info: Circunferencia degenerada: la ecuación representa un único punto.")
                        st.markdown(
                            f"> **Explicación matemática:** Al completar cuadrados, el radio² calculado "
                            f"es $r^2 = 0$. La ecuación tiene exactamente una solución real: "
                            f"el punto $({h_v},\ {k_v})$."
                        )
                    elif tipo_curva == "Circunferencia" and params.get("imaginaria", False):
                        r2_val = params.get("r_cuad", 0)
                        h_v, k_v = params.get("h", 0), params.get("k", 0)
                        st.warning("Atención: Circunferencia imaginaria: no existen puntos reales.")
                        st.markdown(
                            f"> **Explicación matemática:** Al completar cuadrados, el radio² calculado "
                            f"es $r^2 = {r2_val} < 0$.  \n"
                            f"> Esto significa que la ecuación generada por este RUT no tiene "
                            f"solución real en el plano cartesiano.  \n"
                            f"> El centro sería $({h_v},\ {k_v})$ pero no existe ningún punto "
                            f"$(x, y)$ que satisfaga la ecuación."
                        )
                    elif tipo_curva == "Elipse" and params.get("imaginaria", False):
                        M_val = params.get("M", 0)
                        h_v, k_v = params.get("h", 0), params.get("k", 0)
                        st.warning("Atención: Elipse imaginaria: no existen puntos reales.")
                        st.markdown(
                            f"> **Explicación matemática:** Al completar cuadrados se obtiene "
                            f"$M = {M_val} \\leq 0$.  \n"
                            f"> Esto implica que $a^2 = M/A < 0$ y $b^2 = M/B < 0$, "
                            f"por lo que no existen valores reales de $a$ y $b$.  \n"
                            f"> La ecuación generada por este RUT no representa una elipse real "
                            f"en el plano cartesiano."
                        )
                    else:
                        st.warning("Atención: No se pudieron generar puntos para la gráfica.")
                except Exception as err:
                    st.error(f"Error: Error al graficar: {err}")
                    datos_grafico = {"curva": [], "asintotas": [], "elementos": []}

        st.markdown("")
        st.divider()
        st.markdown("")

        st.markdown("""
        <div style="background:linear-gradient(135deg, #f0e8f8 0%, #f8f0f6 100%);
                    padding:16px 20px; border-radius:12px; margin-bottom:16px;">
        <h3 style="margin:0; color:#4a235a;">Fase 3: Elementos Geométricos de la Cónica</h3>
        </div>""", unsafe_allow_html=True)

        with st.container(border=True):
            st.info("Complete estos campos durante la evaluación oral (sin autocompletado).")
            col_e1, col_e2, col_e3 = st.columns(3)
            with col_e1:
                st.text_input(
                    "Centro / origen:",
                    placeholder="(h, k)",
                    key="oral_centro_tab1"
                )
                st.text_input(
                    "Vértices:",
                    placeholder="V1(...), V2(...)",
                    key="oral_vertices_tab1"
                )
            with col_e2:
                st.text_input(
                    "Focos:",
                    placeholder="F1(...), F2(...)",
                    key="oral_focos_tab1"
                )
                st.text_input(
                    "Eje mayor / transverso:",
                    placeholder="horizontal o vertical",
                    key="oral_eje_mayor_tab1"
                )
            with col_e3:
                st.text_input(
                    "Eje menor / conjugado:",
                    placeholder="valor o descripción",
                    key="oral_eje_menor_tab1"
                )
                st.text_input(
                    "Directriz (si aplica):",
                    placeholder="x = ... o y = ...",
                    key="oral_directriz_tab1"
                )

        st.markdown("")
        
        st.markdown("""
        <div style="background:linear-gradient(135deg, #e8f8f0 0%, #f0f8f6 100%);
                    padding:16px 20px; border-radius:12px; margin-bottom:16px;">
        <h3 style="margin:0; color:#1b5e20;"> Fase 4: Representación Visual de Elementos</h3>
        </div>""", unsafe_allow_html=True)

        with st.container(border=True):
            elementos_pts = datos_grafico["elementos"]
            asintotas_pts = datos_grafico["asintotas"]

            if elementos_pts:
                st.markdown("** Puntos de Interés:**")
                e_x = [p["x"] for p in elementos_pts]
                e_y = [p["y"] for p in elementos_pts]
                e_labels = [p["label"] for p in elementos_pts]
                st.scatter_chart(
                    {"x": e_x, "y": e_y, "elemento": e_labels},
                    x="x", y="y", color="elemento",
                    use_container_width=True
                )
            else:
                st.info("Info: Datos de elementos geométricos no disponibles.")

            if asintotas_pts or tipo_curva == "Hiperbola":
                st.markdown("** Asíntotas Lineales Proyectadas:**")
                if asintotas_pts:
                    a_x = [p["x"] for p in asintotas_pts]
                    a_y = [p["y"] for p in asintotas_pts]
                    st.line_chart({"x": a_x, "y": a_y}, x="x", y="y", use_container_width=True)
                else:
                    st.info("Info: Calculando pendientes límites para las asíntotas de la hipérbola.")

    with tab2:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #e8f4f8 0%, #f0f8ee 100%);
                    padding:16px 20px; border-radius:12px; margin-bottom:16px;">
        <h3 style="margin:0; color:#1e3a5f;"> Módulo de Análisis Funcional por Tramo</h3>
        </div>""", unsafe_allow_html=True)

        residuo_limite = d8 % 3
        a_critico = float(d3)
        caso_label = ["Removible", "De Salto", "Infinita"][residuo_limite]

        iconos_caso = {0: "", 1: "", 2: ""}
        if residuo_limite == 0:
            caso_nombre = "Discontinuidad Removible (Caso 1)"
        elif residuo_limite == 1:
            caso_nombre = "Discontinuidad de Salto (Caso 2)"
        else:
            caso_nombre = "Discontinuidad Infinita (Caso 3)"

        with st.container(border=True):
            st.markdown("### Parámetros de la Función")
            col_caso_a, col_caso_b, col_caso_c = st.columns(3)
            col_caso_a.metric("Tipo de discontinuidad", caso_nombre)
            col_caso_b.metric("Punto crítico a", a_critico)
            col_caso_c.metric("Regla (d8 % 3)", f"d8={d8} → residuo {residuo_limite}")
        
        st.markdown("")
        st.markdown("")
        st.divider()
        st.markdown("")
        
        st.markdown("""
        <div style="background:linear-gradient(135deg, #f0e8f8 0%, #f8f0f6 100%);
                    padding:16px 20px; border-radius:12px; margin-bottom:16px;">
        <h3 style="margin:0; color:#4a235a;"> Fase 1: Justificación Algebraica Automatizada</h3>
        </div>""", unsafe_allow_html=True)
        
        with st.container(border=True):
            if residuo_limite == 0:
                st.markdown("** Ecuación asignada (discontinuidad removible):**")
                st.markdown(f"$$ f(x) = \\frac{{(x - {a_critico})(x + {d1})}}{{x - {a_critico}}}, \\quad x \\neq {a_critico} $$")
                st.markdown("** Procedimiento paso a paso:**")
                st.markdown(
                    f"**Paso 1.** Identificar la indeterminación: al evaluar $x = {a_critico}$, el numerador y denominador se anulan simultáneamente:"
                )
                st.markdown(f"$$ f({a_critico}) = \\frac{{({a_critico} - {a_critico})({a_critico} + {d1})}}{{{a_critico} - {a_critico}}} = \\frac{{0 \\cdot {a_critico + d1}}}{{0}} \\quad \\text{{(indeterminación 0/0)}} $$")
                st.markdown(
                    f"**Paso 2.** Simplificar cancelando el factor común $(x - {a_critico})$:"
                )
                st.markdown(f"$$ f(x) = \\frac{{\\cancel{{(x - {a_critico})}}(x + {d1})}}{{\\cancel{{(x - {a_critico})}}}} = x + {d1}, \\quad x \\neq {a_critico} $$")
                st.markdown(f"**Paso 3.** Calcular el límite y verificar continuidad en $x = {a_critico}$:")
                st.markdown(f"$$ \\lim_{{x \\to {a_critico}}} f(x) = {a_critico} + {d1} = {a_critico + d1} $$")
                st.success(
                    f"OK El límite existe y vale {a_critico + d1}.\n\n"
                    f"OK Sin embargo, f({a_critico}) no está definida en la función original (agujero en la gráfica).\n\n"
                    f"OK Como el límite existe pero f(a) no está definida → **Discontinuidad Removible**."
                )
            elif residuo_limite == 1:
                st.markdown("** Ecuación por tramos asignada:**")
                st.markdown(f"$$ f(x) = \\begin{{cases}} x + {d2} & \\text{{si }} x < {a_critico} \\\\ x + {d4} & \\text{{si }} x \\ge {a_critico} \\end{{cases}} $$")
                st.markdown("** Análisis de Límites Laterales:**")
                lim_izq = a_critico + d2
                lim_der = a_critico + d4
                fa_salto = a_critico + d4
                if d2 != d4:
                    st.warning(
                        f"Atención: Límite izquierdo: $\\lim_{{x \\to {a_critico}^-}} (x + {d2}) = {lim_izq}$\n\n"
                        f"Atención: Límite derecho: $\\lim_{{x \\to {a_critico}^+}} (x + {d4}) = {lim_der}$\n\n"
                        f"Atención: Como {lim_izq} ≠ {lim_der}, el límite bilateral **no existe**.\n\n"
                        f"Atención: Valor de la función en el punto: $f({a_critico}) = {a_critico} + {d4} = {fa_salto}$ (definida, pero ≠ límite lateral izquierdo).\n\n"
                        f"Atención: Hay un salto finito de magnitud |{lim_der} - {lim_izq}| = {abs(lim_der - lim_izq)} en x = {a_critico}.\n\n"
                        f"OK **Clasificación: Discontinuidad de Salto Finito.**"
                    )
                else:
                    fa = lim_der
                    st.success(
                        f"OK Límite izquierdo: $\\lim_{{x \\to {a_critico}^-}} (x + {d2}) = {lim_izq}$\n\n"
                        f"OK Límite derecho: $\\lim_{{x \\to {a_critico}^+}} (x + {d4}) = {lim_der}$\n\n"
                        f"OK Como {lim_izq} = {lim_der}, el límite bilateral **existe** y vale {lim_izq}.\n\n"
                        f"OK Además, f({a_critico}) = {a_critico} + {d4} = {fa} = límite.\n\n"
                        f"OK **La función es continua en x = {a_critico}** (caso especial: d2 = d4)."
                    )
            else:
                st.markdown("** Ecuación asignada (discontinuidad infinita):**")
                st.markdown(f"$$ f(x) = \\frac{{{d5} + 1}}{{x - {a_critico}}}, \\quad x \\neq {a_critico} $$")
                st.markdown("** Análisis Asintótico:**")
                st.error(
                    f"Error Cuando x→{a_critico}⁻, el denominador (x - {a_critico}) → 0⁻, por lo que f(x) → -∞.\n\n"
                    f"Error Cuando x→{a_critico}⁺, el denominador (x - {a_critico}) → 0⁺, por lo que f(x) → +∞.\n\n"
                    f"Error Los límites laterales son infinitos y de distinto signo → el límite **no existe**.\n\n"
                    f"Error Valor de la función en el punto: $f({a_critico})$ **no está definida** (denominador = 0 cuando x = {a_critico}).\n\n"
                    f"Error Existe una **asíntota vertical** en x = {a_critico}. La discontinuidad es **infinita/esencial**."
                )

        st.markdown("")
        st.divider()
        st.markdown("")

        st.markdown("""
        <div style="background:linear-gradient(135deg, #e8f8f0 0%, #f0f8f6 100%);
                    padding:16px 20px; border-radius:12px; margin-bottom:16px;">
        <h3 style="margin:0; color:#1b5e20;"> Fase 2: Evidencia Numérica por Aproximación</h3>
        </div>""", unsafe_allow_html=True)

        t_izq, t_der = obtener_tabla_aproximacion(caso_label, digitos, a_critico)

        st.markdown("")
        
        with st.container(border=True):
            st.markdown("### Tablas de Aproximación Numérica")
            c_t1, c_t2 = st.columns(2, gap="large")
            with c_t1:
                st.markdown("** Aproximación Izquierda** ($x \\to a^-$)")
                st.table(t_izq)
            with c_t2:
                st.markdown("** Aproximación Derecha** ($x \\to a^+$)")
                st.table(t_der)

        st.markdown("")
        st.divider()
        st.markdown("")

        st.markdown("""
        <div style="background:linear-gradient(135deg, #f8e8e8 0%, #f8f0f0 100%);
                    padding:16px 20px; border-radius:12px; margin-bottom:16px;">
        <h3 style="margin:0; color:#b71c1c;">Fase 3: Representación Gráfica por Tramos</h3>
        </div>""", unsafe_allow_html=True)
        with st.container(border=True):
            puntos_eje_y = obtener_puntos_grafica(caso_label, digitos, a_critico, rango=2.0, pasos=40)
            if residuo_limite == 0:
                lim_val = float(a_critico + d1)
                spec = {
                    "layer": [
                        {
                            "data": {"values": puntos_eje_y},
                            "mark": {"type": "line", "color": "#1f77b4"},
                            "encoding": {
                                "x": {"field": "x", "type": "quantitative", "title": "x"},
                                "y": {"field": "y", "type": "quantitative", "title": "y"}
                            }
                        },
                        {
                            "data": {"values": [{"hx": float(a_critico), "hy": lim_val}]},
                            "mark": {"type": "point", "filled": False, "size": 200,
                                     "color": "red", "strokeWidth": 2.5},
                            "encoding": {
                                "x": {"field": "hx", "type": "quantitative"},
                                "y": {"field": "hy", "type": "quantitative"}
                            }
                        }
                    ]
                }
                st.vega_lite_chart(spec, use_container_width=True)
                st.caption(f" El círculo vacío rojo en x = {a_critico} representa el punto no definido (agujero). "
                           f"El límite vale {lim_val} pero f({a_critico}) no existe en la función original.")
            elif residuo_limite == 1:
                lim_izq_g = float(a_critico + d2)
                lim_der_g = float(a_critico + d4)
                pts_izq = [p for p in puntos_eje_y if p["x"] < a_critico]
                pts_der = [p for p in puntos_eje_y if p["x"] >= a_critico]
                spec = {
                    "layer": [
                        {
                            "data": {"values": pts_izq},
                            "mark": {"type": "line", "color": "#1f77b4"},
                            "encoding": {
                                "x": {"field": "x", "type": "quantitative", "title": "x"},
                                "y": {"field": "y", "type": "quantitative", "title": "y"}
                            }
                        },
                        {
                            "data": {"values": pts_der},
                            "mark": {"type": "line", "color": "#1f77b4"},
                            "encoding": {
                                "x": {"field": "x", "type": "quantitative"},
                                "y": {"field": "y", "type": "quantitative"}
                            }
                        },
                        {
                            "data": {"values": [{"hx": float(a_critico), "hy": lim_izq_g}]},
                            "mark": {"type": "point", "filled": False, "size": 200,
                                     "color": "red", "strokeWidth": 2.5},
                            "encoding": {
                                "x": {"field": "hx", "type": "quantitative"},
                                "y": {"field": "hy", "type": "quantitative"}
                            }
                        },
                        {
                            "data": {"values": [{"hx": float(a_critico), "hy": lim_der_g}]},
                            "mark": {"type": "point", "filled": True, "size": 150, "color": "red"},
                            "encoding": {
                                "x": {"field": "hx", "type": "quantitative"},
                                "y": {"field": "hy", "type": "quantitative"}
                            }
                        }
                    ]
                }
                st.vega_lite_chart(spec, use_container_width=True)
                st.caption(f" Círculo vacío en ({a_critico}, {lim_izq_g}): límite por izquierda (no alcanzado).  "
                           f" Círculo relleno en ({a_critico}, {lim_der_g}): valor real f({a_critico}).")
            else:
                st.line_chart(puntos_eje_y, x="x", y="y", use_container_width=True)

    with tab3:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #e8f4f8 0%, #f0f8ee 100%);
                    padding:16px 20px; border-radius:12px; margin-bottom:16px;">
        <h3 style="margin:0; color:#1e3a5f;"> Panel de Auditoría para Defensa Oral</h3>
        <p style="margin:6px 0 0 0; font-size:0.9rem; opacity:0.85;">Complete los campos durante la defensa oral</p>
        </div>""", unsafe_allow_html=True)

        # =====================================================================
        # SECCION A: COEFICIENTES Y CLASIFICACION (Fase 4 - Criterios 18 a 24)
        # =====================================================================
        st.markdown("""
        <div style="background:#e8f4f8; border-left:5px solid #2d6a9f;
                    padding:14px 16px; border-radius:6px; margin:16px 0;">
        <b style="font-size:1.05rem;"> SECCIÓN A: Cónica — Coeficientes y Clasificación</b><br>
        <small style="opacity:0.85;">El sistema genera los valores. El estudiante justifica matemáticamente la clasificación.</small>
        </div>""", unsafe_allow_html=True)
        
        with st.container(border=True):

            row_a1, row_a2 = st.columns([1, 1], gap="large")
            
            with row_a1:
                st.markdown("### Coeficientes Calculados")
                st.number_input("Coeficiente A (x²):", value=round(A, 6), disabled=True, key="coef_a")
                st.number_input("Coeficiente B (y²):", value=round(B, 6), disabled=True, key="coef_b")
                st.number_input("Coeficiente C (x):", value=round(C, 6), disabled=True, key="coef_c")
                st.number_input("Coeficiente D (y):", value=round(D, 6), disabled=True, key="coef_d")
                st.number_input("Coeficiente E (cte):", value=round(E, 6), disabled=True, key="coef_e")
                
            with row_a2:
                st.markdown("### Clasificacion de Conica")
                st.selectbox(
                    "Tipo de cónica identificado:",
                    ["Seleccionar...", "Circunferencia", "Elipse", "Hiperbola", "Parabola"],
                    key="conica_tipo_auditar"
                )
                st.text_area(
                    "Justificacion de la clasificacion (¿Por qué se determinó este tipo?):",
                    placeholder="Ej: A≠0, B≠0, A≠B, A·B>0 → Elipse; o A=0 o B=0 → Parabola",
                    height=150,
                    key="clasificacion_justi"
                )
            
            st.markdown("---")
            
            # Elementos geometricos (Criterion 23-24)
            st.markdown("### Elementos Geometricos Canonicos")
            col_elem_a, col_elem_b, col_elem_c = st.columns(3)
            
            with col_elem_a:
                st.text_input(
                    "Centro u Origen (h, k):",
                    placeholder="Ej: (1, -2) o (0, 0)",
                    key="elem_centro"
                )
            
            with col_elem_b:
                st.text_input(
                    "Vertices (principales):",
                    placeholder="Ej: V(3, 0), V(-3, 0)",
                    key="elem_vertices"
                )
            
            with col_elem_c:
                st.text_input(
                    "Focos (si existen):",
                    placeholder="Ej: F(2.24, 0), F(-2.24, 0)",
                    key="elem_focos"
                )
            
            # Parametros especiales (Criterion 25)
            col_param_a, col_param_b, col_param_c = st.columns(3)
            
            with col_param_a:
                st.text_input(
                    "Eje de simetria (si aplica):",
                    placeholder="Ej: y = 0 (eje x) o x = 1",
                    key="elem_ejes"
                )
            
            with col_param_b:
                st.text_input(
                    "Directriz (solo para parabola):",
                    placeholder="Ej: y = -2 o x = 3",
                    key="elem_directriz"
                )
            
            with col_param_c:
                st.text_input(
                    "Ecuacion Canonica (forma transformada):",
                    placeholder="Ej: (x-h)²/a² + (y-k)²/b² = 1",
                    key="elem_canonica"
                )

        st.markdown("")
        st.divider()
        st.markdown("")

        # =====================================================================
        # SECCION B: LIMITES Y CONTINUIDAD (Fase 6 - Criterios 26 a 32)
        # =====================================================================
        st.markdown("""
        <div style="background:#f0f8ee; border-left:5px solid #4CAF50;
                    padding:14px 16px; border-radius:6px; margin:16px 0;">
        <b style="font-size:1.05rem;"> SECCIÓN B: Límites y Continuidad Funcional</b><br>
        <small style="opacity:0.85;">Analice la función por tramos generada desde d8. Complete los valores durante la defensa.</small>
        </div>""", unsafe_allow_html=True)

        with st.container(border=True):

            row_b1, row_b2 = st.columns([1, 1], gap="large")
            
            with row_b1:
                st.markdown("### Limites Laterales")
                st.text_input(
                    "Limite cuando x → a⁻ (por la izquierda):",
                    placeholder="Valor numerico, ±∞, o No existe",
                    key="limite_izq_valor"
                )
                st.text_input(
                    "Limite cuando x → a⁺ (por la derecha):",
                    placeholder="Valor numerico, ±∞, o No existe",
                    key="limite_der_valor"
                )
                st.text_input(
                    "Valor de f(a) en el punto critico:",
                    placeholder="Indefinido, o valor numerico",
                    key="f_punto_critico"
                )
                st.selectbox(
                    "Existe el limite bilateral:",
                    ["Seleccionar...", "Si existe", "No existe (salto)", "No existe (infinito)"],
                    key="limite_existe"
                )
                st.selectbox(
                    "Conclusión sobre continuidad en x = a:",
                    ["Seleccionar...", "La función ES continua en x = a", "La función NO es continua en x = a"],
                    key="conclusion_continuidad"
                )
            
            with row_b2:
                st.markdown("### Clasificacion de Discontinuidad")
                st.selectbox(
                    "Tipo de discontinuidad detectado:",
                    [
                        "Seleccionar...",
                        "Continua (sin discontinuidad)",
                        "Removible / Evitable",
                        "Salto Finito",
                        "Esencial / Infinita"
                    ],
                    key="discontinuidad_tipo_auditar"
                )
                st.text_area(
                    "Justificacion de la clasificacion:",
                    placeholder="Ej: Removible si lim existe pero f(a) no; Salto si lim⁻≠lim⁺; Infinita si lim=±∞",
                    height=120,
                    key="discontinuidad_justi"
                )
            
            st.markdown("---")
            
            # Procedimiento de comprobacion
            st.markdown("### Evidencia de Comprobacion Numerica")
            col_comp_a, col_comp_b = st.columns(2)
            
            with col_comp_a:
                st.text_area(
                    "Tabla de valores izquierda (x→a⁻):",
                    placeholder="Muestre pasos de aproximacion x = a-0.1, a-0.01, etc.",
                    height=100,
                    key="tabla_izq"
                )
            
            with col_comp_b:
                st.text_area(
                    "Tabla de valores derecha (x→a⁺):",
                    placeholder="Muestre pasos de aproximacion x = a+0.001, a+0.01, etc.",
                    height=100,
                    key="tabla_der"
                )
            
            # Conclusion y propuesta
            st.markdown("---")
            st.text_area(
                "Conclusion final (Comportamiento de la funcion en el punto de analisis):",
                placeholder="Describa el comportamiento de f(x) en el entorno de x=a. ¿Qué tipo de discontinuidad es? ¿Cómo se podría remover o clasificar?",
                height=120,
                key="conclusion_limites"
            )

elif rut_ingresado.strip() and not ejecucion:
    st.info("Estructurando entorno seguro. Por favor ingrese un formato de RUT valido.")
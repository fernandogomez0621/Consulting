"""
Aplicacion Streamlit - Gestion de Costos de Equipos de Construccion
Prueba Tecnica - Cientifico de Datos Senior
Andres Fernando Gomez Rojas
"""

import streamlit as st
import pandas as pd
from modulos.visualizaciones.estilos import aplicar_estilo

aplicar_estilo()

st.set_page_config(
    page_title="Costos Equipos - Prueba Tecnica",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {font-size: 1.8rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0.5rem;}
    .sub-header {font-size: 1rem; color: #666; margin-bottom: 2rem;}
    .pred-result {background: #f0f7ff; border-radius: 10px; padding: 1.5rem; border-left: 5px solid #4A90D9; margin: 1rem 0;}
    .pred-value {font-size: 2.2rem; font-weight: 700; color: #1a1a2e;}
    .pred-ic {font-size: 1rem; color: #666; margin-top: 0.3rem;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Navegacion")
    pagina = st.radio(
        "",
        ["Resumen", "EDA", "Modelos", "Proyecciones", "Prediccion", "Agente"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**Prueba Tecnica**")
    st.markdown("Cientifico de Datos Senior")
    st.markdown("Andres Fernando Gomez Rojas")
    st.markdown("---")
    st.caption("Datos: 2010-01 a 2023-08")
    st.caption("Modelos: Lasso, Prophet")
    st.caption("Horizonte: 6 meses")


if pagina == "Resumen":
    st.markdown('<p class="main-header">Gestion de Costos Operativos en Construccion</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analisis de la relacion entre materias primas y costos de equipos</p>', unsafe_allow_html=True)

    from modulos.datos.carga_s3 import cargar_json_eda
    resumen = cargar_json_eda('resumen_eda')
    info_modelos = cargar_json_eda('info_modelos_completa')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Registros", "3,530")
    with col2:
        st.metric("R2 Equipo 1", "0.9913")
    with col3:
        st.metric("R2 Equipo 2", "0.9852")
    with col4:
        st.metric("Horizonte", "6 meses")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Hallazgos principales")
        st.markdown(f"**Equipo 1:** {resumen.get('hallazgo_principal_equipo1', '')}")
        st.markdown(f"**Equipo 2:** {resumen.get('hallazgo_principal_equipo2', '')}")
        st.markdown(f"**Estacionariedad:** {resumen.get('estacionariedad', '')}")
        st.markdown(f"**COVID:** {resumen.get('covid_impacto', '')}")

    with col_b:
        st.markdown("#### Modelos seleccionados")
        for target in ['Price_Equipo1', 'Price_Equipo2']:
            ml = info_modelos.get(target, {}).get('mejor_modelo_ml', {})
            st.markdown(f"**{target}:** {ml.get('nombre', '')} (R2={ml.get('metricas_test', {}).get('r2', 0):.4f})")
        st.markdown("---")
        st.markdown("**Observaciones clave:**")
        for o in info_modelos.get('Price_Equipo1', {}).get('observaciones', [])[:3]:
            st.markdown(f"- {o}")


elif pagina == "EDA":
    st.markdown('<p class="main-header">Analisis Exploratorio de Datos</p>', unsafe_allow_html=True)

    from modulos.datos.carga_s3 import cargar_equipos, cargar_json_eda
    from modulos.eda.estadisticas import formatear_descriptivas, formatear_normalidad, formatear_estacionariedad
    from modulos.eda.correlaciones import graficar_correlaciones, formatear_vif, formatear_granger, formatear_mutual_info
    from modulos.eda.anomalias import formatear_anomalias
    from modulos.eda.segmentacion import formatear_segmentacion
    from modulos.visualizaciones.graficas_series import graficar_series_historicas, graficar_series_con_covid

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Series", "Estadisticas", "Correlaciones", "Anomalias", "COVID", "Volatilidad"])

    with tab1:
        df = cargar_equipos()
        fig = graficar_series_historicas(df, ['Price_X', 'Price_Y', 'Price_Z', 'Price_Equipo1', 'Price_Equipo2'])
        st.pyplot(fig)
        fig2 = graficar_series_con_covid(df, ['Price_X', 'Price_Y', 'Price_Z', 'Price_Equipo1', 'Price_Equipo2'])
        st.pyplot(fig2)

    with tab2:
        st.markdown("#### Estadisticas descriptivas")
        st.dataframe(formatear_descriptivas(cargar_json_eda('estadisticas_descriptivas')), use_container_width=True)
        st.markdown("#### Test de normalidad")
        st.dataframe(formatear_normalidad(cargar_json_eda('test_normalidad')), use_container_width=True)
        st.markdown("#### Estacionariedad (Dickey-Fuller)")
        st.dataframe(formatear_estacionariedad(cargar_json_eda('test_estacionariedad')), use_container_width=True)

    with tab3:
        corr = cargar_json_eda('correlaciones')
        metodo = st.selectbox("Metodo", ["pearson", "spearman"])
        st.pyplot(graficar_correlaciones(corr, metodo))
        st.markdown("#### VIF (Multicolinealidad)")
        st.dataframe(formatear_vif(cargar_json_eda('vif')), use_container_width=True)
        st.markdown("#### Causalidad de Granger")
        st.dataframe(formatear_granger(cargar_json_eda('causalidad_granger')), use_container_width=True)
        st.markdown("#### Mutual Information")
        st.dataframe(formatear_mutual_info(cargar_json_eda('mutual_information')), use_container_width=True)

    with tab4:
        st.dataframe(formatear_anomalias(cargar_json_eda('anomalias')), use_container_width=True)

    with tab5:
        st.dataframe(formatear_segmentacion(cargar_json_eda('segmentacion_covid')), use_container_width=True)

    with tab6:
        st.json(cargar_json_eda('volatilidad'))


elif pagina == "Modelos":
    st.markdown('<p class="main-header">Modelamiento</p>', unsafe_allow_html=True)

    from modulos.datos.carga_s3 import cargar_json_eda
    from modulos.modelamiento.comparacion import formatear_comparacion, resumen_mejor_modelo
    from modulos.modelamiento.prophet import formatear_prophet
    from modulos.visualizaciones.graficas_modelos import graficar_comparacion_modelos, graficar_residuos, graficar_feature_importance

    tab1, tab2, tab3, tab4 = st.tabs(["Comparacion", "Residuos", "Features", "Prophet"])
    comparacion = cargar_json_eda('comparacion_modelos')
    info_modelos = cargar_json_eda('info_modelos_completa')
    residuos_data = cargar_json_eda('analisis_residuos')
    fi = cargar_json_eda('feature_importance')
    prophet_res = cargar_json_eda('prophet_resultados')

    with tab1:
        target = st.selectbox("Equipo", ['Price_Equipo1', 'Price_Equipo2'], key='comp')
        r = resumen_mejor_modelo(info_modelos, target)
        c1, c2, c3 = st.columns(3)
        c1.metric("Mejor modelo", r['Mejor ML'])
        c2.metric("R2 Test", f"{r['R2 ML']:.4f}")
        c3.metric("MAPE", f"{r['MAPE ML']:.2f}%")
        st.dataframe(formatear_comparacion(comparacion, target), use_container_width=True)
        fig = graficar_comparacion_modelos(comparacion, target)
        if fig:
            st.pyplot(fig)

    with tab2:
        target_r = st.selectbox("Equipo", ['Price_Equipo1', 'Price_Equipo2'], key='res')
        st.markdown(f"**Modelo:** {residuos_data.get(target_r, {}).get('modelo', '')}")
        st.pyplot(graficar_residuos(residuos_data.get(target_r, {}), target_r))
        pi = info_modelos.get(target_r, {}).get('prophet', {}).get('residuos', {})
        if pi:
            st.markdown("#### Residuos Prophet")
            st.pyplot(graficar_residuos(pi, f"{target_r} (Prophet)"))

    with tab3:
        target_f = st.selectbox("Equipo", ['Price_Equipo1', 'Price_Equipo2'], key='feat')
        fig_fi = graficar_feature_importance(fi, target_f)
        if fig_fi:
            st.pyplot(fig_fi)

    with tab4:
        target_p = st.selectbox("Equipo", ['Price_Equipo1', 'Price_Equipo2'], key='proph')
        pd_data = formatear_prophet(prophet_res, target_p)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Metricas Prophet")
            for k, v in pd_data.items():
                st.markdown(f"**{k}:** {v}")
        with c2:
            pic = info_modelos.get(target_p, {}).get('prophet', {}).get('intervalo_confianza', {})
            if pic:
                st.markdown("#### Intervalos de Confianza")
                st.markdown(f"**Nivel:** {pic.get('nivel', '')}")
                st.markdown(f"**Ancho promedio:** {pic.get('ancho_promedio_test', '')}")
                st.markdown(f"**Cobertura:** {pic.get('cobertura_test', '')}%")


elif pagina == "Proyecciones":
    st.markdown('<p class="main-header">Proyeccion de Costos</p>', unsafe_allow_html=True)

    from modulos.datos.carga_s3 import cargar_equipos, cargar_json_predicciones
    from modulos.predicciones.proyeccion import resumen_horizonte, resumen_incertidumbre
    from modulos.visualizaciones.graficas_proyeccion import graficar_proyeccion_equipo, graficar_incertidumbre, tabla_proyeccion_mensual

    proy = cargar_json_predicciones('proyecciones_resumen')
    df_hist = cargar_equipos()
    h = resumen_horizonte(proy)
    c1, c2, c3 = st.columns(3)
    c1.metric("Inicio", h['Inicio'])
    c2.metric("Fin", h['Fin'])
    c3.metric("Meses", h['Meses'])
    st.info(h['Justificacion'])
    st.markdown("---")

    tab1, tab2 = st.tabs(["Equipo 1", "Equipo 2"])
    for tab, target in [(tab1, 'Price_Equipo1'), (tab2, 'Price_Equipo2')]:
        with tab:
            mensual = proy.get('resumen_mensual', {}).get(target, {})
            st.dataframe(tabla_proyeccion_mensual(mensual), use_container_width=True)
            st.pyplot(graficar_proyeccion_equipo(df_hist, mensual, target))
            inc = resumen_incertidumbre(proy, target)
            for k, v in inc.items():
                st.markdown(f"**{k}:** {v}")

    st.markdown("---")
    st.pyplot(graficar_incertidumbre(proy))


elif pagina == "Prediccion":
    st.markdown('<p class="main-header">Prediccion de Costos</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ingresa los precios de las materias primas para estimar el costo de los equipos</p>', unsafe_allow_html=True)

    from modulos.datos.carga_s3 import cargar_modelo, cargar_json_eda
    from modulos.predicciones.predictor import predecir_prophet
    import matplotlib.pyplot as plt
    from modulos.visualizaciones.estilos import COLOR_PRINCIPAL, COLOR_SECUNDARIO

    stats = cargar_json_eda('estadisticas_descriptivas')
    st.markdown("---")

    col_form, col_ref = st.columns([2, 1])

    with col_ref:
        st.markdown("#### Rangos de referencia")
        st.markdown(f"**Price X:** {stats['min']['Price_X']:.2f} - {stats['max']['Price_X']:.2f} (media: {stats['mean']['Price_X']:.2f})")
        st.markdown(f"**Price Y:** {stats['min']['Price_Y']:.2f} - {stats['max']['Price_Y']:.2f} (media: {stats['mean']['Price_Y']:.2f})")
        st.markdown(f"**Price Z:** {stats['min']['Price_Z']:.2f} - {stats['max']['Price_Z']:.2f} (media: {stats['mean']['Price_Z']:.2f})")
        st.markdown("---")
        st.caption("Modelo: Prophet con regressors (Price_X, Price_Y, Price_Z). Intervalos de confianza al 95%.")

    with col_form:
        st.markdown("#### Datos de entrada")
        fecha = st.date_input("Fecha", value=pd.Timestamp('2024-03-01'),
                              min_value=pd.Timestamp('2023-09-01'), max_value=pd.Timestamp('2025-12-31'))
        cx, cy, cz = st.columns(3)
        with cx:
            precio_x = st.number_input("Price X", min_value=0.0, max_value=500.0,
                                       value=float(stats['mean']['Price_X']), step=1.0, format="%.2f")
        with cy:
            precio_y = st.number_input("Price Y", min_value=0.0, max_value=2000.0,
                                       value=float(stats['mean']['Price_Y']), step=5.0, format="%.2f")
        with cz:
            precio_z = st.number_input("Price Z", min_value=0.0, max_value=6000.0,
                                       value=float(stats['mean']['Price_Z']), step=10.0, format="%.2f")

        predecir = st.button("Predecir costos", type="primary", use_container_width=True)

    if predecir:
        st.markdown("---")
        st.markdown("### Resultados")

        with st.spinner("Cargando modelos y calculando..."):
            resultados = {}
            for target in ['Price_Equipo1', 'Price_Equipo2']:
                _, _, prophet = cargar_modelo(target)
                resultados[target] = predecir_prophet(prophet, fecha, precio_x, precio_y, precio_z)

        ce1, ce2 = st.columns(2)
        with ce1:
            r1 = resultados['Price_Equipo1']
            st.markdown(f"""<div class="pred-result">
                <div style="color: #666; font-size: 0.9rem;">Equipo 1</div>
                <div class="pred-value">${r1['prediccion']:,.2f}</div>
                <div class="pred-ic">IC 95%: ${r1['ic_inferior']:,.2f} - ${r1['ic_superior']:,.2f}</div>
                <div class="pred-ic">Tendencia: ${r1['tendencia']:,.2f}</div>
            </div>""", unsafe_allow_html=True)

        with ce2:
            r2 = resultados['Price_Equipo2']
            st.markdown(f"""<div class="pred-result" style="border-left-color: #E8743B;">
                <div style="color: #666; font-size: 0.9rem;">Equipo 2</div>
                <div class="pred-value">${r2['prediccion']:,.2f}</div>
                <div class="pred-ic">IC 95%: ${r2['ic_inferior']:,.2f} - ${r2['ic_superior']:,.2f}</div>
                <div class="pred-ic">Tendencia: ${r2['tendencia']:,.2f}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        for i, (target, label) in enumerate([('Price_Equipo1', 'Equipo 1'), ('Price_Equipo2', 'Equipo 2')]):
            r = resultados[target]
            color = COLOR_PRINCIPAL if i == 0 else COLOR_SECUNDARIO
            axes[i].barh(['Prediccion'], [r['prediccion']], color=color, alpha=0.8, height=0.4)
            axes[i].errorbar(r['prediccion'], 0,
                             xerr=[[r['prediccion'] - r['ic_inferior']], [r['ic_superior'] - r['prediccion']]],
                             fmt='o', color='black', capsize=8, capthick=2, markersize=8)
            axes[i].set_title(label, fontweight='bold', fontsize=13)
            axes[i].set_xlabel('Precio')
            axes[i].annotate(f"${r['prediccion']:,.2f}\n[${r['ic_inferior']:,.2f} - ${r['ic_superior']:,.2f}]",
                             xy=(r['prediccion'], 0), xytext=(r['prediccion'], 0.3),
                             ha='center', fontsize=10,
                             bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.5))
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("---")
        detalle = pd.DataFrame({
            'Concepto': ['Fecha', 'Price X', 'Price Y', 'Price Z',
                         'Equipo 1 - Prediccion', 'Equipo 1 - IC Inferior', 'Equipo 1 - IC Superior',
                         'Equipo 2 - Prediccion', 'Equipo 2 - IC Inferior', 'Equipo 2 - IC Superior'],
            'Valor': [str(fecha), f"{precio_x:.2f}", f"{precio_y:.2f}", f"{precio_z:.2f}",
                      f"{resultados['Price_Equipo1']['prediccion']:.2f}",
                      f"{resultados['Price_Equipo1']['ic_inferior']:.2f}",
                      f"{resultados['Price_Equipo1']['ic_superior']:.2f}",
                      f"{resultados['Price_Equipo2']['prediccion']:.2f}",
                      f"{resultados['Price_Equipo2']['ic_inferior']:.2f}",
                      f"{resultados['Price_Equipo2']['ic_superior']:.2f}"]
        })
        st.dataframe(detalle, use_container_width=True, hide_index=True)


elif pagina == "Agente":
    st.markdown('<p class="main-header">Agente de IA</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Pregunta sobre los resultados del analisis, modelos o proyecciones</p>', unsafe_allow_html=True)

    from agente import Agente

    if 'agente' not in st.session_state:
        st.session_state.agente = Agente()
    if 'mensajes_chat' not in st.session_state:
        st.session_state.mensajes_chat = []

    with st.sidebar:
        if st.button("Reiniciar conversacion"):
            st.session_state.agente.reiniciar()
            st.session_state.mensajes_chat = []
            st.rerun()
        st.markdown("**Preguntas sugeridas:**")
        for s in ["Cual es el mejor modelo?", "Que relacion hay entre Y y Equipo 1?",
                   "Cuanto costaria el Equipo 2 en enero 2024?", "Como impacto el COVID?",
                   "Que features son mas importantes?", "Que es un agente de IA vs IA convencional?"]:
            if st.button(s, key=f"sug_{s}"):
                st.session_state.pregunta_sugerida = s

    for msg in st.session_state.mensajes_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    pregunta = st.chat_input("Escribe tu pregunta...")
    if 'pregunta_sugerida' in st.session_state:
        pregunta = st.session_state.pregunta_sugerida
        del st.session_state.pregunta_sugerida

    if pregunta:
        st.session_state.mensajes_chat.append({"role": "user", "content": pregunta})
        with st.chat_message("user"):
            st.markdown(pregunta)
        with st.chat_message("assistant"):
            with st.spinner("Consultando..."):
                try:
                    respuesta = st.session_state.agente.consultar(pregunta)
                    st.markdown(respuesta)
                    st.session_state.mensajes_chat.append({"role": "assistant", "content": respuesta})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

"""
Aplicacion Streamlit - Gestion de Costos de Equipos de Construccion
Prueba Tecnica - Cientifico de Datos Senior
Andres Fernando Gomez Rojas
"""

import streamlit as st
import pandas as pd

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
    col1.metric("Registros", "3,530")
    col2.metric("R2 Equipo 1", "0.9913")
    col3.metric("R2 Equipo 2", "0.9852")
    col4.metric("Horizonte", "6 meses")

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
        cols = ['Price_X', 'Price_Y', 'Price_Z', 'Price_Equipo1', 'Price_Equipo2']
        st.plotly_chart(graficar_series_historicas(df, cols), use_container_width=True)
        st.plotly_chart(graficar_series_con_covid(df, cols), use_container_width=True)

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
        st.plotly_chart(graficar_correlaciones(corr, metodo), use_container_width=True)
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
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        target_r = st.selectbox("Equipo", ['Price_Equipo1', 'Price_Equipo2'], key='res')
        st.markdown(f"**Modelo:** {residuos_data.get(target_r, {}).get('modelo', '')}")
        st.plotly_chart(graficar_residuos(residuos_data.get(target_r, {}), target_r), use_container_width=True)
        pi = info_modelos.get(target_r, {}).get('prophet', {}).get('residuos', {})
        if pi:
            st.markdown("#### Residuos Prophet")
            st.plotly_chart(graficar_residuos(pi, f"{target_r} (Prophet)"), use_container_width=True)

    with tab3:
        target_f = st.selectbox("Equipo", ['Price_Equipo1', 'Price_Equipo2'], key='feat')
        fig_fi = graficar_feature_importance(fi, target_f)
        if fig_fi:
            st.plotly_chart(fig_fi, use_container_width=True)

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
            st.plotly_chart(graficar_proyeccion_equipo(df_hist, mensual, target), use_container_width=True)
            inc = resumen_incertidumbre(proy, target)
            for k, v in inc.items():
                st.markdown(f"**{k}:** {v}")

    st.markdown("---")
    st.plotly_chart(graficar_incertidumbre(proy), use_container_width=True)


elif pagina == "Prediccion":
    st.markdown('<p class="main-header">Prediccion de Costos</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ingresa los precios de las materias primas para estimar el costo de los equipos</p>', unsafe_allow_html=True)

    from modulos.datos.carga_s3 import cargar_modelo, cargar_json_eda
    from modulos.predicciones.predictor import predecir_prophet
    import plotly.graph_objects as go
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

        # Grafica interactiva con Plotly
        fig = go.Figure()

        equipos = ['Equipo 1', 'Equipo 2']
        preds = [resultados['Price_Equipo1']['prediccion'], resultados['Price_Equipo2']['prediccion']]
        lowers = [resultados['Price_Equipo1']['ic_inferior'], resultados['Price_Equipo2']['ic_inferior']]
        uppers = [resultados['Price_Equipo1']['ic_superior'], resultados['Price_Equipo2']['ic_superior']]
        colores = [COLOR_PRINCIPAL, COLOR_SECUNDARIO]

        for i in range(2):
            fig.add_trace(go.Bar(
                name=equipos[i], x=[equipos[i]], y=[preds[i]],
                marker_color=colores[i],
                error_y=dict(type='data',
                             symmetric=False,
                             array=[uppers[i] - preds[i]],
                             arrayminus=[preds[i] - lowers[i]],
                             thickness=2, width=8),
                text=[f'${preds[i]:,.2f}'], textposition='outside',
                hovertemplate=(f'{equipos[i]}<br>'
                               f'Prediccion: ${preds[i]:,.2f}<br>'
                               f'IC: [${lowers[i]:,.2f} - ${uppers[i]:,.2f}]<extra></extra>')
            ))

        fig.update_layout(
            height=400,
            title='Prediccion con Intervalos de Confianza (95%)',
            yaxis_title='Precio',
            showlegend=False,
            template='plotly_white',
            font=dict(family='Segoe UI, sans-serif', size=12)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Gauge charts
        st.markdown("---")
        cg1, cg2 = st.columns(2)

        for col_g, target, label, color in [
            (cg1, 'Price_Equipo1', 'Equipo 1', COLOR_PRINCIPAL),
            (cg2, 'Price_Equipo2', 'Equipo 2', COLOR_SECUNDARIO)
        ]:
            with col_g:
                r = resultados[target]
                rango_min = r['ic_inferior'] * 0.9
                rango_max = r['ic_superior'] * 1.1

                fig_gauge = go.Figure(go.Indicator(
                    mode='gauge+number',
                    value=r['prediccion'],
                    number=dict(prefix='$', valueformat=',.2f'),
                    title=dict(text=label),
                    gauge=dict(
                        axis=dict(range=[rango_min, rango_max]),
                        bar=dict(color=color),
                        steps=[
                            dict(range=[rango_min, r['ic_inferior']], color='#f0f0f0'),
                            dict(range=[r['ic_inferior'], r['ic_superior']], color='rgba(74, 144, 217, 0.15)'),
                            dict(range=[r['ic_superior'], rango_max], color='#f0f0f0')
                        ],
                        threshold=dict(line=dict(color=color, width=3), thickness=0.8, value=r['prediccion'])
                    )
                ))
                fig_gauge.update_layout(height=280, margin=dict(l=30, r=30, t=50, b=20))
                st.plotly_chart(fig_gauge, use_container_width=True)

        # Tabla detalle
        st.markdown("---")
        detalle = pd.DataFrame({
            'Concepto': ['Fecha', 'Price X', 'Price Y', 'Price Z',
                         'Equipo 1 - Prediccion', 'Equipo 1 - IC 95%',
                         'Equipo 2 - Prediccion', 'Equipo 2 - IC 95%'],
            'Valor': [str(fecha), f"${precio_x:.2f}", f"${precio_y:.2f}", f"${precio_z:.2f}",
                      f"${resultados['Price_Equipo1']['prediccion']:,.2f}",
                      f"[${resultados['Price_Equipo1']['ic_inferior']:,.2f} - ${resultados['Price_Equipo1']['ic_superior']:,.2f}]",
                      f"${resultados['Price_Equipo2']['prediccion']:,.2f}",
                      f"[${resultados['Price_Equipo2']['ic_inferior']:,.2f} - ${resultados['Price_Equipo2']['ic_superior']:,.2f}]"]
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

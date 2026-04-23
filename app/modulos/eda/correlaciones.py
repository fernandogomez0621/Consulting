"""Funciones para mostrar correlaciones con graficas Plotly."""

import pandas as pd
import plotly.graph_objects as go
from modulos.visualizaciones.estilos import *


def graficar_correlaciones(corr_json, metodo='pearson'):
    data = corr_json.get(metodo, {})
    df_corr = pd.DataFrame(data)

    fig = go.Figure(data=go.Heatmap(
        z=df_corr.values,
        x=df_corr.columns,
        y=df_corr.index,
        colorscale='RdBu_r',
        zmid=0, zmin=-1, zmax=1,
        text=df_corr.round(3).values,
        texttemplate='%{text}',
        textfont=dict(size=11),
        hovertemplate='%{x} vs %{y}<br>Correlacion: %{z:.4f}<extra></extra>'
    ))

    fig.update_layout(
        height=500, width=600,
        title=f'Correlacion {metodo.capitalize()}',
        **LAYOUT_BASE
    )
    return fig


def formatear_vif(vif_json):
    rows = []
    for var, valor in vif_json.items():
        nivel = 'OK' if valor < 5 else ('Moderada' if valor < 10 else 'Severa')
        rows.append({'Variable': var, 'VIF': f"{valor:.2f}", 'Nivel': nivel})
    return pd.DataFrame(rows)


def formatear_granger(granger_json):
    rows = []
    for par, info in granger_json.items():
        rows.append({
            'Par': par,
            'Mejor Lag': info['mejor_lag'],
            'p-value': f"{info['mejor_p_value']:.6f}",
            'Causal': info['es_causal']
        })
    return pd.DataFrame(rows)


def formatear_mutual_info(mi_json):
    rows = []
    for target, valores in mi_json.items():
        for var, mi in sorted(valores.items(), key=lambda x: x[1], reverse=True):
            rows.append({'Target': target, 'Variable': var, 'MI': f"{mi:.4f}"})
    return pd.DataFrame(rows)

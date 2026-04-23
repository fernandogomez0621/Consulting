"""Graficas interactivas de series de tiempo con Plotly."""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from modulos.visualizaciones.estilos import *


def graficar_series_historicas(df, columnas, titulo='Series de Tiempo'):
    fig = make_subplots(
        rows=len(columnas), cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=columnas
    )

    for i, col in enumerate(columnas):
        color = COLORES_VARIABLES.get(col, COLOR_PRINCIPAL)
        fig.add_trace(
            go.Scatter(
                x=df['Date'], y=df[col],
                name=col, line=dict(color=color, width=1),
                hovertemplate='%{x|%Y-%m-%d}<br>%{y:,.2f}<extra></extra>'
            ),
            row=i+1, col=1
        )

    fig.update_layout(
        height=200 * len(columnas),
        title=titulo,
        showlegend=False,
        **LAYOUT_BASE
    )
    return fig


def graficar_series_con_covid(df, columnas):
    fig = make_subplots(
        rows=len(columnas), cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=columnas
    )

    for i, col in enumerate(columnas):
        color = COLORES_VARIABLES.get(col, COLOR_PRINCIPAL)
        fig.add_trace(
            go.Scatter(
                x=df['Date'], y=df[col],
                name=col, line=dict(color=color, width=1),
                hovertemplate='%{x|%Y-%m-%d}<br>%{y:,.2f}<extra></extra>'
            ),
            row=i+1, col=1
        )
        fig.add_vrect(
            x0='2020-03-01', x1='2021-06-01',
            fillcolor='red', opacity=0.08, line_width=0,
            row=i+1, col=1
        )

    fig.update_layout(
        height=200 * len(columnas),
        title='Series con Segmentacion COVID (zona roja)',
        showlegend=False,
        **LAYOUT_BASE
    )
    return fig


def graficar_retornos(df, columnas):
    retornos = df[columnas].pct_change().dropna()
    fechas = df['Date'].iloc[1:].values

    fig = make_subplots(
        rows=len(columnas), cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=[f'Retorno {c}' for c in columnas]
    )

    for i, col in enumerate(columnas):
        color = COLORES_VARIABLES.get(col, COLOR_PRINCIPAL)
        fig.add_trace(
            go.Scatter(
                x=fechas, y=retornos[col],
                name=col, line=dict(color=color, width=0.5),
                hovertemplate='%{x|%Y-%m-%d}<br>%{y:.4%}<extra></extra>'
            ),
            row=i+1, col=1
        )
        fig.add_hline(y=0, line_dash='dash', line_color='black', line_width=0.5, row=i+1, col=1)

    fig.update_layout(
        height=180 * len(columnas),
        title='Retornos Porcentuales Diarios',
        showlegend=False,
        **LAYOUT_BASE
    )
    return fig

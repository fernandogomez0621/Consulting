"""Graficas interactivas de proyeccion con intervalos de confianza - Plotly."""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from modulos.visualizaciones.estilos import *


def graficar_proyeccion_equipo(df_historico, proyeccion_mensual, target):
    meses = sorted(proyeccion_mensual.keys())
    prophet_mean = [proyeccion_mensual[m]['prophet_mean'] for m in meses]
    prophet_lower = [proyeccion_mensual[m]['prophet_lower'] for m in meses]
    prophet_upper = [proyeccion_mensual[m]['prophet_upper'] for m in meses]
    lasso_mean = [proyeccion_mensual[m]['lasso_mean'] for m in meses]
    fechas_pred = [pd.Timestamp(f"{m}-15") for m in meses]

    color = COLORES_VARIABLES.get(target, COLOR_PRINCIPAL)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=False,
                        subplot_titles=[f'{target} - Historico + Proyeccion', f'{target} - Zoom Proyeccion'],
                        vertical_spacing=0.12)

    # Panel 1: historico + proyeccion
    fig.add_trace(
        go.Scatter(x=df_historico['Date'], y=df_historico[target],
                   name='Historico', line=dict(color=color, width=0.8),
                   hovertemplate='%{x|%Y-%m-%d}<br>$%{y:,.2f}<extra></extra>'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=fechas_pred, y=prophet_upper, mode='lines',
                   line=dict(width=0), showlegend=False, hoverinfo='skip'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=fechas_pred, y=prophet_lower, mode='lines',
                   line=dict(width=0), fill='tonexty', fillcolor=COLOR_IC,
                   name='IC 95%', hoverinfo='skip'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=fechas_pred, y=prophet_mean, mode='lines+markers',
                   name='Prophet', line=dict(color=COLOR_SECUNDARIO, width=2.5),
                   marker=dict(size=7),
                   hovertemplate='%{x|%Y-%m}<br>Prophet: $%{y:,.2f}<extra></extra>'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=fechas_pred, y=lasso_mean, mode='lines+markers',
                   name='Lasso', line=dict(color=COLOR_ROJO, width=2, dash='dash'),
                   marker=dict(size=6, symbol='square'),
                   hovertemplate='%{x|%Y-%m}<br>Lasso: $%{y:,.2f}<extra></extra>'),
        row=1, col=1
    )
    fig.add_vline(x=df_historico['Date'].max(), line_dash='dot',
                  line_color=COLOR_GRIS, line_width=1, row=1, col=1)

    # Panel 2: zoom
    fig.add_trace(
        go.Scatter(x=fechas_pred, y=prophet_upper, mode='lines',
                   line=dict(width=0), showlegend=False, hoverinfo='skip'),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=fechas_pred, y=prophet_lower, mode='lines',
                   line=dict(width=0), fill='tonexty', fillcolor=COLOR_IC,
                   showlegend=False, hoverinfo='skip'),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=fechas_pred, y=prophet_mean, mode='lines+markers+text',
                   line=dict(color=COLOR_SECUNDARIO, width=2.5),
                   marker=dict(size=9),
                   text=[f'${v:,.0f}' for v in prophet_mean],
                   textposition='top center', textfont=dict(size=10),
                   showlegend=False,
                   hovertemplate='%{x|%Y-%m}<br>Prophet: $%{y:,.2f}<br>IC: [$' +
                   '<br>'.join([f'{l:,.0f} - ${u:,.0f}' for l, u in zip(prophet_lower, prophet_upper)]) +
                   ']<extra></extra>'),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=fechas_pred, y=lasso_mean, mode='lines+markers',
                   line=dict(color=COLOR_ROJO, width=2, dash='dash'),
                   marker=dict(size=7, symbol='square'),
                   showlegend=False,
                   hovertemplate='%{x|%Y-%m}<br>Lasso: $%{y:,.2f}<extra></extra>'),
        row=2, col=1
    )

    fig.update_layout(height=700, **LAYOUT_BASE)
    fig.update_yaxes(title_text='Precio', row=1, col=1)
    fig.update_yaxes(title_text='Precio', row=2, col=1)
    return fig


def graficar_incertidumbre(proyecciones_resumen):
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=['Ancho IC 95% - Equipo 1', 'Ancho IC 95% - Equipo 2'],
                        horizontal_spacing=0.1)

    for i, target in enumerate(['Price_Equipo1', 'Price_Equipo2']):
        mensual = proyecciones_resumen.get('resumen_mensual', {}).get(target, {})
        meses = sorted(mensual.keys())
        anchos = [mensual[m]['ancho_ic'] for m in meses]
        color = COLOR_PRINCIPAL if i == 0 else COLOR_SECUNDARIO

        fig.add_trace(
            go.Bar(x=meses, y=anchos, name=target,
                   marker_color=color,
                   text=[f'{a:.1f}' for a in anchos], textposition='outside',
                   hovertemplate='%{x}<br>Ancho IC: %{y:.2f}<extra></extra>'),
            row=1, col=i+1
        )

    fig.update_layout(height=350, showlegend=False, **LAYOUT_BASE)
    fig.update_yaxes(title_text='Ancho IC', row=1, col=1)
    return fig


def tabla_proyeccion_mensual(proyeccion_mensual):
    rows = []
    for mes in sorted(proyeccion_mensual.keys()):
        d = proyeccion_mensual[mes]
        rows.append({
            'Mes': mes,
            'Prophet': f"${d['prophet_mean']:,.2f}",
            'IC Inferior': f"${d['prophet_lower']:,.2f}",
            'IC Superior': f"${d['prophet_upper']:,.2f}",
            'Ancho IC': f"{d['ancho_ic']:.2f}",
            'Lasso': f"${d['lasso_mean']:,.2f}"
        })
    return pd.DataFrame(rows)

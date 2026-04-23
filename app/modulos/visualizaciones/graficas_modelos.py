"""Graficas interactivas de comparacion de modelos y residuos con Plotly."""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from modulos.visualizaciones.estilos import *


def graficar_comparacion_modelos(comparacion, target):
    modelos = comparacion.get(target, [])
    if not modelos:
        return None

    top = modelos[:12]
    nombres = [f"{m['ronda']} | {m['modelo']}" for m in top]
    r2_test = [m['test_r2'] for m in top]
    gaps = [m.get('gap', 0) for m in top]
    colores = [COLOR_ROJO if g > 0.1 else COLOR_PRINCIPAL for g in gaps]

    fig = make_subplots(rows=1, cols=2, subplot_titles=['R2 Test', 'Gap Train-Test'],
                        horizontal_spacing=0.15)

    fig.add_trace(
        go.Bar(y=nombres, x=r2_test, orientation='h',
               marker_color=colores, name='R2 Test',
               hovertemplate='%{y}<br>R2: %{x:.6f}<extra></extra>'),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(y=nombres, x=gaps, orientation='h',
               marker_color=colores, name='Gap',
               hovertemplate='%{y}<br>Gap: %{x:.4f}<extra></extra>'),
        row=1, col=2
    )
    fig.add_vline(x=0.1, line_dash='dash', line_color=COLOR_ROJO, line_width=1, row=1, col=2)

    fig.update_layout(
        height=500, showlegend=False,
        title=f'Comparacion de Modelos - {target} (rojo = overfit)',
        **LAYOUT_BASE
    )
    fig.update_yaxes(autorange='reversed')
    return fig


def graficar_residuos(residuos_info, target):
    media = residuos_info.get('media', 0)
    std = residuos_info.get('std', 1)
    shapiro_p = residuos_info.get('shapiro_p', 0)
    jb_p = residuos_info.get('jarque_bera_p', 0)
    lb_p = residuos_info.get('ljung_box_p', 0)

    fig = make_subplots(rows=1, cols=2, subplot_titles=['Distribucion Estimada', 'Tests Estadisticos'],
                        horizontal_spacing=0.12)

    x = np.linspace(media - 4*std, media + 4*std, 200)
    from scipy.stats import norm
    y = norm.pdf(x, media, std)

    fig.add_trace(
        go.Scatter(x=x, y=y, fill='tozeroy', name='Distribucion',
                   line=dict(color=COLOR_SECUNDARIO, width=2),
                   fillcolor='rgba(232, 116, 59, 0.2)',
                   hovertemplate='Residuo: %{x:.2f}<br>Densidad: %{y:.4f}<extra></extra>'),
        row=1, col=1
    )
    fig.add_vline(x=media, line_dash='dash', line_color=COLOR_ROJO, line_width=1, row=1, col=1,
                  annotation_text=f'Media: {media:.4f}')

    tests = ['Shapiro-Wilk', 'Jarque-Bera', 'Ljung-Box']
    pvals = [shapiro_p, jb_p, lb_p]
    colores_bar = [COLOR_TERCERO if p > 0.05 else COLOR_ROJO for p in pvals]

    fig.add_trace(
        go.Bar(y=tests, x=pvals, orientation='h',
               marker_color=colores_bar, name='p-value',
               text=[f'{p:.6f}' for p in pvals], textposition='outside',
               hovertemplate='%{y}<br>p-value: %{x:.6f}<extra></extra>'),
        row=1, col=2
    )
    fig.add_vline(x=0.05, line_dash='dash', line_color=COLOR_ROJO, line_width=1, row=1, col=2,
                  annotation_text='alpha=0.05')

    fig.update_layout(
        height=350, showlegend=False,
        title=f'Analisis de Residuos - {target} (Media: {media:.4f}, Std: {std:.4f})',
        **LAYOUT_BASE
    )
    return fig


def graficar_feature_importance(fi_data, target):
    info = fi_data.get(target, {})
    importancias = info.get('importancias', {})
    if not importancias:
        return None

    sorted_items = sorted(importancias.items(), key=lambda x: x[1], reverse=True)[:15]
    nombres = [item[0] for item in sorted_items][::-1]
    valores = [item[1] for item in sorted_items][::-1]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(y=nombres, x=valores, orientation='h',
               marker_color=COLOR_PRINCIPAL,
               text=[f'{v:.4f}' for v in valores], textposition='outside',
               hovertemplate='%{y}<br>Importancia: %{x:.6f}<extra></extra>')
    )

    fig.update_layout(
        height=500,
        title=f'Top 15 Features - {target} ({info.get("modelo", "")})',
        xaxis_title='Importancia (coeficiente absoluto)',
        **LAYOUT_BASE
    )
    return fig

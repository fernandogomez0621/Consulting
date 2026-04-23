"""Configuracion global de estilos para graficas Plotly."""

COLOR_PRINCIPAL = '#4A90D9'
COLOR_SECUNDARIO = '#E8743B'
COLOR_TERCERO = '#2CA02C'
COLOR_ROJO = '#D93025'
COLOR_GRIS = '#888888'
COLOR_IC = 'rgba(232, 116, 59, 0.15)'
COLOR_IC_LINEA = 'rgba(232, 116, 59, 0.4)'

COLORES_VARIABLES = {
    'Price_X': '#4A90D9',
    'Price_Y': '#E8743B',
    'Price_Z': '#2CA02C',
    'Price_Equipo1': '#8E44AD',
    'Price_Equipo2': '#E74C3C'
}

LAYOUT_BASE = dict(
    template='plotly_white',
    font=dict(family='Segoe UI, sans-serif', size=12),
    hovermode='x unified',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    margin=dict(l=60, r=30, t=50, b=50)
)

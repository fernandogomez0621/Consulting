"""Graficas de series de tiempo."""

import matplotlib.pyplot as plt
from modulos.visualizaciones.estilos import *


def graficar_series_historicas(df, columnas, titulo='Series de Tiempo'):
    fig, axes = crear_figura(len(columnas), 1)
    if len(columnas) == 1:
        axes = [axes]
    for i, col in enumerate(columnas):
        axes[i].plot(df['Date'], df[col], linewidth=0.6, color=COLOR_PRINCIPAL)
        axes[i].set_ylabel(col)
    axes[0].set_title(titulo, fontweight='bold')
    axes[-1].set_xlabel('Fecha')
    plt.tight_layout()
    return fig


def graficar_series_con_covid(df, columnas):
    import pandas as pd
    fig, axes = crear_figura(len(columnas), 1)
    if len(columnas) == 1:
        axes = [axes]
    for i, col in enumerate(columnas):
        axes[i].plot(df['Date'], df[col], linewidth=0.6, color=COLOR_PRINCIPAL)
        axes[i].axvspan(pd.Timestamp('2020-03-01'), pd.Timestamp('2021-06-01'),
                        alpha=0.15, color=COLOR_ROJO, label='COVID' if i == 0 else '')
        axes[i].set_ylabel(col)
    axes[0].set_title('Series con Segmentacion COVID', fontweight='bold')
    axes[0].legend(loc='upper left', fontsize=8)
    plt.tight_layout()
    return fig


def graficar_retornos(df, columnas):
    retornos = df[columnas].pct_change().dropna()
    fig, axes = crear_figura(len(columnas), 1)
    if len(columnas) == 1:
        axes = [axes]
    fechas = df['Date'].iloc[1:].values
    for i, col in enumerate(columnas):
        axes[i].plot(fechas, retornos[col], linewidth=0.3, color=COLOR_PRINCIPAL)
        axes[i].axhline(y=0, color='black', linewidth=0.5)
        axes[i].set_ylabel(col)
    axes[0].set_title('Retornos Porcentuales Diarios', fontweight='bold')
    plt.tight_layout()
    return fig

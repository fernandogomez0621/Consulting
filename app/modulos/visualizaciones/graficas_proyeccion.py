"""Graficas de proyeccion con intervalos de confianza."""

import matplotlib.pyplot as plt
import pandas as pd
from modulos.visualizaciones.estilos import *


def graficar_proyeccion_equipo(df_historico, proyeccion_mensual, target):
    meses = sorted(proyeccion_mensual.keys())
    prophet_mean = [proyeccion_mensual[m]['prophet_mean'] for m in meses]
    prophet_lower = [proyeccion_mensual[m]['prophet_lower'] for m in meses]
    prophet_upper = [proyeccion_mensual[m]['prophet_upper'] for m in meses]
    lasso_mean = [proyeccion_mensual[m]['lasso_mean'] for m in meses]

    fig, axes = crear_figura(2, 1, figsize=(14, 10))

    # Panel 1: historico + proyeccion
    axes[0].plot(df_historico['Date'], df_historico[target],
                 linewidth=0.5, color=COLOR_PRINCIPAL, label='Historico')

    fechas_pred = [pd.Timestamp(f"{m}-15") for m in meses]
    axes[0].plot(fechas_pred, prophet_mean, 'o-', color=COLOR_SECUNDARIO,
                 linewidth=2, markersize=5, label='Prophet')
    axes[0].fill_between(fechas_pred, prophet_lower, prophet_upper,
                          alpha=0.2, color=COLOR_IC, label='IC 95%')
    axes[0].plot(fechas_pred, lasso_mean, 's--', color=COLOR_ROJO,
                 linewidth=1.5, markersize=4, label='Lasso')
    axes[0].axvline(x=df_historico['Date'].max(), color=COLOR_GRIS,
                     linestyle='--', linewidth=1)
    axes[0].set_title(f'Proyeccion de Costos - {target}', fontweight='bold', fontsize=13)
    axes[0].set_ylabel('Precio')
    axes[0].legend(fontsize=9)

    # Panel 2: zoom
    axes[1].plot(fechas_pred, prophet_mean, 'o-', color=COLOR_SECUNDARIO,
                 linewidth=2, markersize=6, label='Prophet')
    axes[1].fill_between(fechas_pred, prophet_lower, prophet_upper,
                          alpha=0.2, color=COLOR_IC, label='IC 95%')
    axes[1].plot(fechas_pred, lasso_mean, 's--', color=COLOR_ROJO,
                 linewidth=2, markersize=5, label='Lasso')

    for i, m in enumerate(meses):
        axes[1].annotate(f'{prophet_mean[i]:.0f}',
                         (fechas_pred[i], prophet_mean[i]),
                         textcoords="offset points", xytext=(0, 12),
                         ha='center', fontsize=8, color=COLOR_SECUNDARIO)

    axes[1].set_title(f'Zoom Proyeccion - {target}', fontweight='bold', fontsize=13)
    axes[1].set_ylabel('Precio')
    axes[1].set_xlabel('Mes')
    axes[1].legend(fontsize=9)

    plt.tight_layout()
    return fig


def graficar_incertidumbre(proyecciones_resumen):
    fig, axes = crear_figura(1, 2, figsize=(14, 5))

    for i, target in enumerate(['Price_Equipo1', 'Price_Equipo2']):
        mensual = proyecciones_resumen.get('resumen_mensual', {}).get(target, {})
        meses = sorted(mensual.keys())
        anchos = [mensual[m]['ancho_ic'] for m in meses]
        fechas = [pd.Timestamp(f"{m}-15") for m in meses]

        axes[i].bar(fechas, anchos, width=20, color=COLOR_SECUNDARIO, alpha=0.7)
        axes[i].set_title(f'Ancho IC 95% - {target}', fontweight='bold')
        axes[i].set_ylabel('Ancho IC')
        axes[i].set_xlabel('Mes')
        axes[i].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    return fig


def tabla_proyeccion_mensual(proyeccion_mensual):
    rows = []
    for mes in sorted(proyeccion_mensual.keys()):
        d = proyeccion_mensual[mes]
        rows.append({
            'Mes': mes,
            'Prophet': f"{d['prophet_mean']:.2f}",
            'IC Inferior': f"{d['prophet_lower']:.2f}",
            'IC Superior': f"{d['prophet_upper']:.2f}",
            'Ancho IC': f"{d['ancho_ic']:.2f}",
            'Lasso': f"{d['lasso_mean']:.2f}"
        })
    return pd.DataFrame(rows)

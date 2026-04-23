"""Funciones para mostrar correlaciones."""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from modulos.visualizaciones.estilos import *


def graficar_correlaciones(corr_json, metodo='pearson'):
    data = corr_json.get(metodo, {})
    df_corr = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(df_corr, annot=True, fmt='.3f', cmap='RdBu_r', center=0,
                vmin=-1, vmax=1, ax=ax, square=True)
    ax.set_title(f'Correlacion {metodo.capitalize()}', fontweight='bold')
    plt.tight_layout()
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

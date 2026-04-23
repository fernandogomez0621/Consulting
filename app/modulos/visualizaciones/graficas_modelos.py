"""Graficas de comparacion de modelos y residuos."""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from modulos.visualizaciones.estilos import *


def graficar_comparacion_modelos(comparacion, target):
    modelos = comparacion.get(target, [])
    if not modelos:
        return None

    nombres = [f"{m['ronda']} - {m['modelo']}" for m in modelos[:12]]
    r2_test = [m['test_r2'] for m in modelos[:12]]
    gaps = [m.get('gap', 0) for m in modelos[:12]]

    fig, axes = crear_figura(1, 2, figsize=(14, 6))

    colores = [COLOR_ROJO if g > 0.1 else COLOR_PRINCIPAL for g in gaps]
    axes[0].barh(range(len(nombres)), r2_test, color=colores, alpha=0.8)
    axes[0].set_yticks(range(len(nombres)))
    axes[0].set_yticklabels(nombres, fontsize=8)
    axes[0].invert_yaxis()
    axes[0].set_xlabel('R2 Test')
    axes[0].set_title(f'R2 Test - {target}', fontweight='bold')

    axes[1].barh(range(len(nombres)), gaps, color=colores, alpha=0.8)
    axes[1].set_yticks(range(len(nombres)))
    axes[1].set_yticklabels(nombres, fontsize=8)
    axes[1].invert_yaxis()
    axes[1].set_xlabel('Gap (Train - Test)')
    axes[1].set_title('Gap Train-Test (rojo = overfit)', fontweight='bold')
    axes[1].axvline(x=0.1, color=COLOR_ROJO, linestyle='--', linewidth=1, alpha=0.5)

    plt.tight_layout()
    return fig


def graficar_residuos(residuos_info, target):
    fig, axes = crear_figura(1, 3, figsize=(15, 4))

    media = residuos_info.get('media', 0)
    std = residuos_info.get('std', 1)

    x = np.linspace(media - 4*std, media + 4*std, 100)
    axes[0].plot(x, stats.norm.pdf(x, media, std), color=COLOR_SECUNDARIO, linewidth=2)
    axes[0].axvline(x=media, color=COLOR_ROJO, linestyle='--', linewidth=1)
    axes[0].set_title('Distribucion de Residuos', fontweight='bold')
    axes[0].set_xlabel('Residuo')

    info_text = (f"Media: {media:.4f}\n"
                 f"Std: {std:.4f}\n"
                 f"Ljung-Box p: {residuos_info.get('ljung_box_p', 0):.4f}")
    axes[1].text(0.5, 0.5, info_text, transform=axes[1].transAxes,
                 fontsize=12, verticalalignment='center', horizontalalignment='center',
                 fontfamily='monospace',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    axes[1].set_title(f'Estadisticas - {target}', fontweight='bold')
    axes[1].axis('off')

    shapiro_p = residuos_info.get('shapiro_p', 0)
    jb_p = residuos_info.get('jarque_bera_p', 0)
    lb_p = residuos_info.get('ljung_box_p', 0)

    tests = ['Shapiro-Wilk', 'Jarque-Bera', 'Ljung-Box']
    pvals = [shapiro_p, jb_p, lb_p]
    colores_bar = [COLOR_TERCERO if p > 0.05 else COLOR_ROJO for p in pvals]

    axes[2].barh(tests, pvals, color=colores_bar, alpha=0.8)
    axes[2].axvline(x=0.05, color=COLOR_ROJO, linestyle='--', linewidth=1)
    axes[2].set_xlabel('p-value')
    axes[2].set_title('Tests sobre Residuos', fontweight='bold')

    plt.tight_layout()
    return fig


def graficar_feature_importance(fi_data, target):
    info = fi_data.get(target, {})
    importancias = info.get('importancias', {})
    if not importancias:
        return None

    sorted_items = sorted(importancias.items(), key=lambda x: x[1], reverse=True)[:15]
    nombres = [item[0] for item in sorted_items]
    valores = [item[1] for item in sorted_items]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(range(len(nombres)), valores, color=COLOR_PRINCIPAL, alpha=0.8)
    ax.set_yticks(range(len(nombres)))
    ax.set_yticklabels(nombres)
    ax.invert_yaxis()
    ax.set_xlabel('Importancia (coeficiente absoluto)')
    ax.set_title(f'Top 15 Features - {target} ({info.get("modelo", "")})', fontweight='bold')
    plt.tight_layout()
    return fig

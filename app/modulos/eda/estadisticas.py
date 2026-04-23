"""Funciones para mostrar estadisticas del EDA."""

import pandas as pd


def formatear_descriptivas(stats_json):
    df = pd.DataFrame(stats_json)
    df = df.round(4)
    return df


def formatear_normalidad(norm_json):
    rows = []
    for var, info in norm_json.items():
        rows.append({
            'Variable': var,
            'Shapiro-Wilk': f"{info['shapiro_stat']:.4f}",
            'p-value SW': f"{info['shapiro_p']:.6f}",
            'Jarque-Bera': f"{info['jarque_bera_stat']:.4f}",
            'p-value JB': f"{info['jarque_bera_p']:.6f}",
            'Normal': info['es_normal']
        })
    return pd.DataFrame(rows)


def formatear_estacionariedad(est_json):
    rows = []
    for var, info in est_json.items():
        rows.append({
            'Variable': var,
            'ADF Stat': f"{info['adf_stat']:.4f}",
            'p-value': f"{info['p_value']:.6f}",
            'Estacionaria': info['es_estacionaria']
        })
    return pd.DataFrame(rows)

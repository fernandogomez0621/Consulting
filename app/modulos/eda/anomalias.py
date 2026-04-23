"""Funciones para mostrar anomalias."""

import pandas as pd


def formatear_anomalias(anomalias_json):
    rows = []
    for var, info in anomalias_json.items():
        rows.append({
            'Variable': var,
            'IQR': info['iqr_anomalias'],
            'Z-score > 3': info['zscore_anomalias'],
            'Isolation Forest': info['isolation_forest_anomalias'],
            'Total registros': info['total_registros']
        })
    return pd.DataFrame(rows)

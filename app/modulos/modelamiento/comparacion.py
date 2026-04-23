"""Funciones para comparacion de modelos."""

import pandas as pd


def formatear_comparacion(comp_json, target):
    modelos = comp_json.get(target, [])
    rows = []
    for m in modelos:
        rows.append({
            'Ronda': m['ronda'],
            'Modelo': m['modelo'],
            'R2 Test': f"{m['test_r2']:.6f}",
            'RMSE Test': f"{m['test_rmse']:.4f}",
            'MAE Test': f"{m.get('test_mae', 0):.4f}",
            'MAPE %': f"{m['test_mape']:.4f}",
            'Gap': f"{m.get('gap', 0):.4f}",
            'Overfit': 'SI' if m.get('gap', 0) > 0.1 else ''
        })
    return pd.DataFrame(rows)


def resumen_mejor_modelo(info_modelos, target):
    info = info_modelos.get(target, {})
    ml = info.get('mejor_modelo_ml', {})
    prophet = info.get('prophet', {})
    return {
        'Mejor ML': ml.get('nombre', ''),
        'R2 ML': ml.get('metricas_test', {}).get('r2', 0),
        'RMSE ML': ml.get('metricas_test', {}).get('rmse', 0),
        'MAPE ML': ml.get('metricas_test', {}).get('mape', 0),
        'R2 Prophet': prophet.get('metricas_test', {}).get('r2', 0),
        'RMSE Prophet': prophet.get('metricas_test', {}).get('rmse', 0),
        'Params': ml.get('best_params', {})
    }

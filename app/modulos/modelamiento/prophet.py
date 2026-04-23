"""Funciones para resultados de Prophet."""

import pandas as pd


def formatear_prophet(prophet_json, target):
    info = prophet_json.get(target, {})
    return {
        'R2 Train': info.get('train', {}).get('r2', 0),
        'R2 Test': info.get('test', {}).get('r2', 0),
        'RMSE Test': info.get('test', {}).get('rmse', 0),
        'MAPE Test': info.get('test', {}).get('mape', 0),
        'Changepoints': info.get('n_changepoints', 0),
        'Regressors': ', '.join(info.get('regressors', [])),
        'Changepoint Prior': info.get('params', {}).get('changepoint_prior_scale', ''),
        'Seasonality Prior': info.get('params', {}).get('seasonality_prior_scale', '')
    }

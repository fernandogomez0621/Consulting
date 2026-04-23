"""Funciones para predecir con Prophet."""

import pandas as pd


def predecir_prophet(modelo_prophet, fecha, precio_x, precio_y, precio_z):
    """
    Predice el costo del equipo con Prophet.
    Retorna prediccion puntual e intervalo de confianza.
    """
    df_input = pd.DataFrame({
        'ds': [pd.Timestamp(fecha)],
        'Price_X': [precio_x],
        'Price_Y': [precio_y],
        'Price_Z': [precio_z]
    })

    forecast = modelo_prophet.predict(df_input)

    return {
        'prediccion': round(forecast['yhat'].values[0], 2),
        'ic_inferior': round(forecast['yhat_lower'].values[0], 2),
        'ic_superior': round(forecast['yhat_upper'].values[0], 2),
        'tendencia': round(forecast['trend'].values[0], 2)
    }


def predecir_prophet_rango(modelo_prophet, df_inputs):
    """
    Predice para multiples fechas.
    df_inputs debe tener columnas: ds, Price_X, Price_Y, Price_Z
    """
    forecast = modelo_prophet.predict(df_inputs)

    resultado = pd.DataFrame({
        'Fecha': forecast['ds'],
        'Prediccion': forecast['yhat'].round(2),
        'IC Inferior': forecast['yhat_lower'].round(2),
        'IC Superior': forecast['yhat_upper'].round(2),
        'Tendencia': forecast['trend'].round(2)
    })

    return resultado

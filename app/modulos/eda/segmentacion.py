"""Funciones para mostrar segmentacion COVID."""

import pandas as pd


def formatear_segmentacion(seg_json):
    rows = []
    for periodo, info in seg_json.items():
        rows.append({
            'Periodo': periodo,
            'Registros': info['n_registros'],
            'Inicio': info['fecha_inicio'],
            'Fin': info['fecha_fin'],
            'Corr Y-Eq1': info['correlaciones_equipo1']['Price_Y'],
            'Corr Z-Eq2': info['correlaciones_equipo2']['Price_Z'],
            'Corr X-Eq1': info['correlaciones_equipo1']['Price_X']
        })
    return pd.DataFrame(rows)

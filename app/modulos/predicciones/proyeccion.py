"""Funciones para proyecciones de costos."""

import pandas as pd


def resumen_horizonte(proy_json):
    h = proy_json.get('horizonte', {})
    return {
        'Inicio': h.get('inicio', ''),
        'Fin': h.get('fin', ''),
        'Meses': h.get('meses', 0),
        'Justificacion': h.get('justificacion', '')
    }


def resumen_incertidumbre(proy_json, target):
    inc = proy_json.get('incertidumbre', {}).get(target, {})
    return {
        'Ancho IC promedio': inc.get('ancho_ic_promedio', 0),
        'Ancho IC relativo': f"{inc.get('ancho_ic_relativo_pct', 0):.1f}%",
        'Ancho IC mes 1': inc.get('ancho_ic_mes1', 0),
        'Ancho IC mes 6': inc.get('ancho_ic_mes6', 0)
    }

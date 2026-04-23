"""Configuracion global de estilos para graficas."""

import matplotlib.pyplot as plt
import seaborn as sns

COLOR_PRINCIPAL = '#4A90D9'
COLOR_SECUNDARIO = '#E8743B'
COLOR_TERCERO = '#2CA02C'
COLOR_ROJO = '#D93025'
COLOR_GRIS = '#888888'
COLOR_IC = '#E8743B'

COLORES_MATERIAS = {
    'Price_X': '#4A90D9',
    'Price_Y': '#E8743B',
    'Price_Z': '#2CA02C'
}

COLORES_EQUIPOS = {
    'Price_Equipo1': '#4A90D9',
    'Price_Equipo2': '#E8743B'
}


def aplicar_estilo():
    plt.rcParams['figure.figsize'] = (12, 5)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    sns.set_style('whitegrid')


def crear_figura(filas=1, columnas=1, figsize=None):
    if figsize is None:
        figsize = (12, 4 * filas)
    fig, axes = plt.subplots(filas, columnas, figsize=figsize)
    return fig, axes

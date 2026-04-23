"""Funciones de carga de datos desde S3."""

import boto3
import pandas as pd
import json
import pickle
from io import StringIO
import streamlit as st

BUCKET = 'consulting-dataknow-prueba-tecnica'
REGION = 'us-east-2'

_s3 = boto3.client('s3', region_name=REGION)


@st.cache_data(ttl=3600)
def leer_csv(key, **kwargs):
    obj = _s3.get_object(Bucket=BUCKET, Key=key)
    contenido = obj['Body'].read().decode('utf-8-sig')
    return pd.read_csv(StringIO(contenido), **kwargs)


@st.cache_data(ttl=3600)
def leer_json(key):
    try:
        obj = _s3.get_object(Bucket=BUCKET, Key=key)
        return json.loads(obj['Body'].read())
    except Exception as e:
        return {"error": str(e)}


@st.cache_resource(ttl=3600)
def leer_pickle(key):
    obj = _s3.get_object(Bucket=BUCKET, Key=key)
    return pickle.loads(obj['Body'].read())


def cargar_equipos():
    return leer_csv('datos_procesados/historico_equipos_limpio.csv', parse_dates=['Date'])


def cargar_materias():
    x = leer_csv('datos_procesados/X_limpio.csv', parse_dates=['Date'])
    y = leer_csv('datos_procesados/Y_limpio.csv', parse_dates=['Date'])
    z = leer_csv('datos_procesados/Z_limpio.csv', parse_dates=['Date'])
    return x, y, z


def cargar_dataset_features():
    return leer_csv('datos_procesados/dataset_con_features.csv', parse_dates=['Date'])


def cargar_json_eda(nombre):
    return leer_json(f'eda_resultados/{nombre}.json')


def cargar_json_predicciones(nombre):
    return leer_json(f'predicciones/{nombre}.json')


def cargar_modelo(equipo):
    nombre = equipo.replace('Price_', '').lower()
    modelo = leer_pickle(f'modelos/mejor_modelo_{nombre}.pkl')
    scaler = leer_pickle(f'modelos/scaler_{nombre}.pkl')
    prophet = leer_pickle(f'modelos/prophet_{nombre}.pkl')
    return modelo, scaler, prophet

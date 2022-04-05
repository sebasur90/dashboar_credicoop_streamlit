import datetime as dt
import pathlib
import urllib
import urllib.request

import pandas as pd
import streamlit as st
from pandas_datareader import data as pdr
#import xlrd

PATH = pathlib.Path(__file__).parent

DATA_PATH = PATH.joinpath("../datasets").resolve()


def proceso(fecha_inicio_dataset_credicoop):


    start = fecha_inicio_dataset_credicoop

    now = dt.datetime.now()
    
    df_peso = pdr.get_data_yahoo("ggal.ba", start, now)

    df_dolar = pdr.get_data_yahoo("ggal", start, now)

    df_peso = df_peso.reset_index()

    df_dolar = df_dolar.reset_index()
    

    datos_ccl = pd.merge(df_peso, df_dolar, on='Date', how='outer')

    datos_ccl.columns = datos_ccl.columns.str.lower()
    #datos_ccl = datos_ccl.fillna(method='bfill')
    datos_ccl = datos_ccl.sort_values(by='date', ascending=True)
    datos_ccl = datos_ccl.fillna(method='ffill')    
    datos_ccl = datos_ccl.fillna(method='bfill')    

    datos_ccl['ccl'] = datos_ccl['adj close_x']*10 / datos_ccl['adj close_y']

    datos_ccl.rename(columns={'date': 'fecha'}, inplace=True)

    datos_ccl = datos_ccl.drop(datos_ccl.columns[1: 13], axis=1)

    datos_ccl_mensual = datos_ccl.copy()

    datos_ccl_mensual = datos_ccl_mensual.set_index('fecha')

    datos_ccl_mensual['ano'] = datos_ccl_mensual.index.year
    datos_ccl_mensual['mes'] = datos_ccl_mensual.index.month

    datos_ccl_mensual = datos_ccl_mensual.groupby(
        ['ano', 'mes'], as_index=False)['ccl'].mean()

    st.session_state['datos_ccl'] = datos_ccl
    st.session_state['datos_ccl_mensual'] = datos_ccl_mensual
    

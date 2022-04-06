import funciones_para_datasets.procesa_cotizacion
import pandas as pd
import datetime as dt
from datetime import date
import numpy as np
import pathlib
import streamlit as st


def proceso():

    PATH = pathlib.Path(__file__).parent

    DATA_PATH = PATH.joinpath("../datasets").resolve()

    datos_sin_procesar = st.session_state['dataframe_original']
    #datos_sin_procesar = pd.read_csv(        (DATA_PATH.joinpath("./mov.csv").resolve()), sep=';')

    st.session_state['meses_del_ano'] = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
                                         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

    st.session_state['meses_del_ano_numeros']=[1,2,3,4,5,6,7,8,9,10,11,12]

    st.session_state['anos']=[2018,2019,2020,2021,2022]

    datos = datos_sin_procesar.copy()

    # paso a minuscula las columnas y la info la descripcion
    datos.columns = datos.columns.str.lower()
    datos['descripcion'] = datos['descripcion'].str.lower()

    # le doy formato a la fecha
    datos['fecha'] = pd.to_datetime(datos['fecha'], format='%Y%m%d')

    # saca comas y puntos y convierte a numeros las columnas

    columnas = ['debito', 'credito', 'saldo']
    for columna in columnas:
        datos[columna] = datos[columna].str.replace('.', '', regex=True)
        datos[columna] = datos[columna].str.replace(',', '.', regex=True)
        datos[columna] = datos[columna].astype(float)

    anos = range(datos.fecha.iloc[-1].year, datos.fecha.iloc[0].year)

    # procesa_cotizacion.proceso(datos.fecha.iloc[-1])

    ''' dol = pd.read_excel((DATA_PATH.joinpath("./dolar.xlsx")
                         ).resolve(), sheet_name="cotizacion") '''

    #st.session_state['datos_ccl'] = datos_ccl
    #st.session_state['datos_ccl_mensual'] = datos_ccl_mensual

    ''' datos_ccl = pd.read_excel(
        (DATA_PATH.joinpath("./dolar.xlsx")).resolve(), sheet_name="datos_ccl")
    datos_ccl_mensual = pd.read_excel(
        (DATA_PATH.joinpath("./dolar.xlsx")).resolve(), sheet_name="datos_ccl_mensual") '''

    # datasets_adicionales.descarga_datasets(datos.fecha.iloc[-1])

    conceptos = []

    datos['concepto'] = np.where(datos.descripcion.str.contains("pago de servicios ente: "),
                                 datos.descripcion.map(
                                     lambda x: x[len("pago de servicios ente: "):]),
                                 np.where(datos.descripcion.str.contains("compra con tarjeta cabal debito"),
                                          datos.descripcion.map(
                                              lambda x: x[len("compra con tarjeta cabal debito tarj:xxxx comercio:"):]),
                                          np.where(
                                              datos.descripcion.str.contains(
                                                  "debito/credito automatico-tarjeta cabal"),
                                              "cabal",
                                              np.where(datos.descripcion.str.contains(
                                                  "debito/credito automatico-tarjeta visa"), "visa",
                                                  np.where(datos.descripcion.str.contains("cajero automatico"),
                                                           "retiro de cajero automatico",                                                               
                                                                        np.where(
                                                                            datos.descripcion.str.contains(
                                                                                "compra/venta de moneda extranjera"),
                                                                            "compra/venta de moneda extranjera", datos.descripcion
                                                                        ))))))

    ''' dolares = dol.copy()

    datos_final = pd.merge(datos, dolares, on='fecha', how='inner')

    datos_final['debito_usd'] = datos_final['debito'] / \
        datos_final['cotizacion']
    datos_final['credito_usd'] = datos_final['credito'] / \
        datos_final['cotizacion']

    datos_final = datos_final.fillna(0)

    datos_final['val_abs'] = datos_final['credito'] + datos_final['debito']
    datos_final['val_abs_usd'] = datos_final['credito_usd'] + \
        datos_final['debito_usd']

    conceptos = datos_final['concepto'].unique()
    conceptos.sort()

    anos = datos_final['fecha'].dt.year.unique()
    anos = anos.tolist()
    anos.sort()

    meses = datos_final['fecha'].dt.month.unique()
    meses.sort()
    meses = meses.tolist()

    dias = datos_final['fecha'].dt.day.unique()
    dias.sort()
    dias = dias.tolist() '''
    
    datos_final = pd.merge(
        datos, st.session_state['datos_ccl'], on='fecha', how='inner')

    
    datos_final['ccl'] = datos_final['ccl'].fillna(method='bfill')
    datos_final = datos_final.fillna(0)
    datos_final = datos_final.dropna()

    datos_final['debito_usd_ccl'] = round(
        datos_final['debito'] / datos_final['ccl'], 2)
    datos_final['credito_usd_ccl'] = round(
        datos_final['credito'] / datos_final['ccl'], 2)

    datos_final['val_abs_usd_ccl'] = datos_final['credito_usd_ccl'] + \
        datos_final['debito_usd_ccl']

    #datos_final = datos_final.set_index('fecha')

    datos_final['ano'] = pd.DatetimeIndex(datos_final['fecha']).year
    datos_final['mes'] = pd.DatetimeIndex(datos_final['fecha']).month
    datos_final = datos_final.set_index('fecha')
    datos_final = datos_final.sort_values(by='fecha')    
    datos_final['val_abs']=abs(datos_final['credito'] + datos_final['debito'] )
    st.session_state['datos_procesados']=datos_final
    st.dataframe(st.session_state['datos_procesados'])
    
    st.session_state['sueldos']=st.session_state['datos_procesados'][st.session_state['datos_procesados'].concepto =='acreditacion de sueldos ' ]
    st.session_state['sueldos_agrupados_mes_ano']=st.session_state['sueldos'].groupby(['ano','mes'])['val_abs','val_abs_usd_ccl'].sum().reset_index()
   
    datos_final.to_csv("datos_2.csv")
    st.session_state['sueldos'].to_csv("sueldos.csv")
    st.session_state['sueldos_agrupados_mes_ano'].to_csv("sueldos_agrupados_mes_ano.csv")
    st.session_state['sueldos_agrupados_mes_ano']['media_12']=st.session_state['sueldos_agrupados_mes_ano'].val_abs_usd_ccl.rolling(12).mean()
    st.session_state['sueldos_agrupados_mes_ano']['media_6']=st.session_state['sueldos_agrupados_mes_ano'].val_abs_usd_ccl.rolling(12).mean()
    st.session_state['sueldos_agrupados_mes_ano']['media_3']=st.session_state['sueldos_agrupados_mes_ano'].val_abs_usd_ccl.rolling(12).mean()
    st.session_state['sueldos_agrupados_mes_ano']['media_12']=st.session_state['sueldos_agrupados_mes_ano'].val_abs.rolling(12).mean()
    st.session_state['sueldos_agrupados_mes_ano']['media_6']=st.session_state['sueldos_agrupados_mes_ano'].val_abs.rolling(12).mean()
    st.session_state['sueldos_agrupados_mes_ano']['media_3']=st.session_state['sueldos_agrupados_mes_ano'].val_abs.rolling(12).mean()
    
    
    
    st.session_state['mejor_ano']=st.session_state['sueldos_agrupados_mes_ano'].groupby('ano')['val_abs_usd_ccl','val_abs'].sum()
    
    st.session_state['mejor_ano']=st.session_state['mejor_ano'].reset_index()
    st.session_state['mejor_ano'].columns=['ano','val_abs_usd_ccl','val_abs']
    
    st.session_state['mejor_mes']=st.session_state['sueldos_agrupados_mes_ano'].groupby('mes')['val_abs_usd_ccl','val_abs'].sum()
    st.session_state['mejor_mes']=st.session_state['mejor_mes'].reset_index()
    st.session_state['mejor_mes'].columns=['mes','val_abs_usd_ccl','val_abs']
    
    
    st.session_state['pivot'] = st.session_state['sueldos'].groupby(['ano', 'mes'], as_index=False)[
                'val_abs_usd_ccl'].sum()
    st.session_state['pivot']['val_abs_usd_ccl'] = st.session_state['pivot']['val_abs_usd_ccl'].round()
    st.session_state['pivot'] = st.session_state['pivot'].pivot(index='mes', columns='ano',
                        values='val_abs_usd_ccl')
    
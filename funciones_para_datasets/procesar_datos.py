import pandas as pd
import numpy as np

import streamlit as st


def proceso():

    datos_sin_procesar = st.session_state['dataframe_original']
    st.session_state['meses_del_ano'] = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
                                         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    st.session_state['meses_del_ano_numeros']=[1,2,3,4,5,6,7,8,9,10,11,12]
    st.session_state['anos']=[2018,2019,2020,2021,2022]
    datos = datos_sin_procesar.copy()
    datos.columns = datos.columns.str.lower()
    datos['descripcion'] = datos['descripcion'].str.lower()
    datos['fecha'] = pd.to_datetime(datos['fecha'], format='%Y%m%d')
    columnas = ['debito', 'credito', 'saldo']
    for columna in columnas:
        datos[columna] = datos[columna].str.replace('.', '', regex=True)
        datos[columna] = datos[columna].str.replace(',', '.', regex=True)
        datos[columna] = datos[columna].astype(float)

    anos = range(datos.fecha.iloc[-1].year, datos.fecha.iloc[0].year)

    
    conceptos = []

    datos['concepto'] = np.where(datos.descripcion.str.contains("pago de servicios ente: "),
                                 datos.descripcion.map(
                                     lambda x: x[len("pago de servicios ente: "):]),
                                 np.where(datos.descripcion.str.contains("compra con tarjeta cabal debito"),
                                          datos.descripcion.map(
                                              lambda x: x[len("compra con tarjeta cabal debito tarj:xxxx comercio:"):]),
                                          np.where(datos.descripcion.str.contains("transf."),"transferencias", 
                                            np.where(datos.descripcion.str.contains(
                                                                    "debito/cred aut-segurcoop seg"),
                                                                    "debito/cred aut-segurcoop seg",
                                                                    np.where(datos.descripcion.str.contains("constitucion de plazo fijo"),"constitucion de plazo fijo", 
                                                                             np.where(datos.descripcion.str.contains("mercado libre") | datos.descripcion.str.contains("mercadolibre"),"mercadolibre", 
                                                                                      
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
                                                                        ))))))))))

    
    
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

    

    datos_final['ano'] = pd.DatetimeIndex(datos_final['fecha']).year
    
    st.session_state['anos']=datos_final['ano'].sort_values(ascending=True).unique()
    st.session_state['ultimo_ano']=st.session_state['anos'][-1]
    
    datos_final['mes'] = pd.DatetimeIndex(datos_final['fecha']).month
    datos_final = datos_final.set_index('fecha')
    datos_final = datos_final.sort_values(by='fecha')    
    datos_final['val_abs']=abs(datos_final['credito'] + datos_final['debito'] )
    st.session_state['datos_procesados']=datos_final
    st.session_state['datos_procesados'].to_csv("datos_proc.csv")
    
    
    st.session_state['sueldos']=st.session_state['datos_procesados'][st.session_state['datos_procesados'].concepto =='acreditacion de sueldos ' ]
    st.session_state['sueldos_agrupados_mes_ano']=st.session_state['sueldos'].groupby(['ano','mes'])['val_abs','val_abs_usd_ccl'].sum().reset_index()
   
    
    
    
    st.session_state['sueldos_agrupados_mes_ano']['media_12_usd']=st.session_state['sueldos_agrupados_mes_ano'].val_abs_usd_ccl.rolling(12).mean()
    st.session_state['sueldos_agrupados_mes_ano']['media_6_usd']=st.session_state['sueldos_agrupados_mes_ano'].val_abs_usd_ccl.rolling(12).mean()
    st.session_state['sueldos_agrupados_mes_ano']['media_3_usd']=st.session_state['sueldos_agrupados_mes_ano'].val_abs_usd_ccl.rolling(12).mean()
    st.session_state['sueldos_agrupados_mes_ano']['media_12']=st.session_state['sueldos_agrupados_mes_ano'].val_abs.rolling(12).mean()
    st.session_state['sueldos_agrupados_mes_ano']['media_6']=st.session_state['sueldos_agrupados_mes_ano'].val_abs.rolling(12).mean()
    st.session_state['sueldos_agrupados_mes_ano']['media_3']=st.session_state['sueldos_agrupados_mes_ano'].val_abs.rolling(12).mean()
    
    st.session_state['sueldos_agrupados_ano']=st.session_state['sueldos_agrupados_mes_ano'].groupby('ano')['val_abs_usd_ccl','val_abs'].sum().reset_index()

    
    st.session_state['mejor_ano']=st.session_state['sueldos_agrupados_mes_ano'].groupby('ano')['val_abs_usd_ccl','val_abs'].sum()
    
    st.session_state['mejor_ano']=st.session_state['mejor_ano'].reset_index()
    st.session_state['mejor_ano'].columns=['ano','val_abs_usd_ccl','val_abs']
    
    if len(st.session_state['sueldos_agrupados_mes_ano'][st.session_state['sueldos_agrupados_mes_ano'].ano == st.session_state['sueldos_agrupados_mes_ano'].ano.sort_values().iloc[0]]) <12:
        st.session_state['mejor_ano']=st.session_state['mejor_ano'][st.session_state['mejor_ano'].ano >st.session_state['sueldos_agrupados_mes_ano'].ano.sort_values().iloc[0]]
    
     
    
    st.session_state['mejor_mes']=st.session_state['sueldos_agrupados_mes_ano'].groupby('mes')['val_abs_usd_ccl','val_abs'].sum()
    st.session_state['mejor_mes']=st.session_state['mejor_mes'].reset_index()
    st.session_state['mejor_mes'].columns=['mes','val_abs_usd_ccl','val_abs'] 
    st.session_state['pivot'] = st.session_state['sueldos'].groupby(['ano', 'mes'], as_index=False)[
                'val_abs_usd_ccl'].sum()
    st.session_state['pivot']['val_abs_usd_ccl'] = st.session_state['pivot']['val_abs_usd_ccl'].round()
    st.session_state['pivot'] = st.session_state['pivot'].pivot(index='mes', columns='ano',
                        values='val_abs_usd_ccl')
    
   
    st.session_state['gastos'] = st.session_state['datos_procesados'][(st.session_state['datos_procesados']['debito'] > 0) &
                              (st.session_state['datos_procesados']['concepto'] != "suscripcion a fondo comun de inversion ") &
                              (st.session_state['datos_procesados']['concepto'] != "constitucion de plazo fijo") &
                              (st.session_state['datos_procesados']['concepto'] != "compra/venta de moneda extranjera")&
                              (st.session_state['datos_procesados']['concepto'] != "transferencias")]
    
    
    
    st.session_state['gastos_tarjetas'] = st.session_state['gastos'][(st.session_state['gastos']['debito'] > 0) &
                                        (st.session_state['gastos']['concepto'] == "cabal") |
                                        (st.session_state['gastos']['concepto'] == "visa")]
    
    st.session_state['gastos_agrupados_mes_ano']=st.session_state['gastos'].groupby(['ano','mes'])['val_abs','val_abs_usd_ccl'].sum().reset_index()
    st.session_state['gastos_agrupados_ano']=st.session_state['gastos'].groupby('ano')['val_abs_usd_ccl','val_abs'].sum().reset_index()
    
    st.session_state['gastos_agrupados_mes_ano']['media_12_usd']=st.session_state['gastos_agrupados_mes_ano'].val_abs_usd_ccl.rolling(12).mean()
    st.session_state['gastos_agrupados_mes_ano']['media_6_usd']=st.session_state['gastos_agrupados_mes_ano'].val_abs_usd_ccl.rolling(12).mean()
    st.session_state['gastos_agrupados_mes_ano']['media_3_usd']=st.session_state['gastos_agrupados_mes_ano'].val_abs_usd_ccl.rolling(12).mean()
    st.session_state['gastos_agrupados_mes_ano']['media_12']=st.session_state['gastos_agrupados_mes_ano'].val_abs.rolling(12).mean()
    st.session_state['gastos_agrupados_mes_ano']['media_6']=st.session_state['gastos_agrupados_mes_ano'].val_abs.rolling(12).mean()
    st.session_state['gastos_agrupados_mes_ano']['media_3']=st.session_state['gastos_agrupados_mes_ano'].val_abs.rolling(12).mean()
    
    st.session_state['gastos_agrupados_mes_ano_tarjetas']=st.session_state['gastos_tarjetas'].groupby(['ano','mes'])['val_abs','val_abs_usd_ccl'].sum().reset_index()
    st.session_state['gasto_agrupados_ano_tarjetas']=st.session_state['gastos_tarjetas'].groupby('ano')['val_abs_usd_ccl','val_abs'].sum().reset_index()
    
    st.session_state['peor_ano']=st.session_state['gastos_agrupados_mes_ano'].groupby('ano')['val_abs_usd_ccl','val_abs'].sum()
    
    st.session_state['peor_ano']=st.session_state['peor_ano'].reset_index()
    st.session_state['peor_ano'].columns=['ano','val_abs_usd_ccl','val_abs']
    
    if len(st.session_state['gastos_agrupados_mes_ano'][st.session_state['gastos_agrupados_mes_ano'].ano == st.session_state['gastos_agrupados_mes_ano'].ano.sort_values().iloc[0]]) <12:
        st.session_state['peor_ano']=st.session_state['peor_ano'][st.session_state['peor_ano'].ano >st.session_state['gastos_agrupados_mes_ano'].ano.sort_values().iloc[0]]
    
    
    st.session_state['peor_mes']=st.session_state['gastos_agrupados_mes_ano'].groupby('mes')['val_abs_usd_ccl','val_abs'].sum()
    st.session_state['peor_mes']=st.session_state['peor_mes'].reset_index()
    st.session_state['peor_mes'].columns=['mes','val_abs_usd_ccl','val_abs']     
   
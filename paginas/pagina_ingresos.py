import streamlit as st

def pagina_ingresos_funcion():
    if "sueldos" not in st.session_state:        
        st.warning("primero debe cargar dataset")
    else:            
        st.title("pagina_ingresos")
        
        
        
        with st.sidebar:
            genre = st.radio(
            "Seleccionar tipo de moneda",
            ('Dolar', 'Peso'))

            if genre == 'Dolar':
                st.session_state['moneda']='val_abs_usd_ccl'
                st.write('Seleccionaste Dolar')                
            else:
                st.session_state['moneda']='val_abs'
                st.write('Seleccionaste Peso')
            
           
                        
            st.session_state['ano_inicio'], st.session_state['ano_fin'] = st.select_slider(
            'Seleccionar años ',
            options=st.session_state['anos'],
            value=(st.session_state['anos'][0], st.session_state['anos'][-1]))
            st.write('Seleccionaste los años entre ', st.session_state['ano_inicio'], 'y', st.session_state['ano_fin'])
            
        datos_importantes(st.session_state['moneda'])    
        ing_media()
        grafico_sueldos_agrupados()
        graf_mejor_ano()
        graf_mejor_mes()
        graf_mapacalor()
        graf_cuadro_ingreso()           
        ing_repetidos()
        sueldos_ordenados()
        



def datos_importantes(mon):   
    dataframe_datos=st.session_state['datos_procesados'][st.session_state['datos_procesados'].ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]
    filtro_sueldo = st.session_state['sueldos_agrupados_mes_ano'][st.session_state['sueldos_agrupados_mes_ano'].ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]
    st.session_state['datos_imp_sueltos_historicos_totales']=int(filtro_sueldo[mon].sum())
    st.session_state['datos_imp_ultimo_sueldo']=int(filtro_sueldo[mon].iloc[-1] )    
    st.session_state['datos_imp_anteultimo_sueldo']=int(filtro_sueldo[mon].iloc[-2] )      
    variacion_ultimo_sueldo=st.session_state['datos_imp_ultimo_sueldo']/st.session_state['datos_imp_anteultimo_sueldo']-1
    
    st.session_state['datos_imp_sueldos_totales_ultimo_ano']=st.session_state['sueldos_agrupados_ano'][st.session_state['sueldos_agrupados_ano'].ano==st.session_state['sueldos_agrupados_ano'].ano.iloc[-1]][mon].iloc[0]
    
    st.session_state['datos_imp_sueldos_totales_anteultimo_ano']=st.session_state['sueldos_agrupados_ano'][st.session_state['sueldos_agrupados_ano'].ano==st.session_state['sueldos_agrupados_ano'].ano.iloc[-2]][mon].iloc[0]
    variacion_sueldo_ultimo_ano=st.session_state['datos_imp_sueldos_totales_ultimo_ano']/st.session_state['datos_imp_sueldos_totales_anteultimo_ano']-1
   
    
    
    col1, col2  = st.columns(2)
    col1.metric(label="Total datos", value=len(dataframe_datos))    
    col2.metric(label=f"Total ingresos ({filtro_sueldo.ano.iloc[0]}-{filtro_sueldo.ano.iloc[-1]} )" ,value=f"{st.session_state['datos_imp_sueltos_historicos_totales']:,.0f}")
    
    col3, col4  = st.columns(2)
    col3.metric(label="Total datos", value=len(dataframe_datos))    
    col4.metric(label=f"Ultimo sueldo ({filtro_sueldo.mes.iloc[-1]}/{filtro_sueldo.ano.iloc[-1]}) " ,value=f"{st.session_state['datos_imp_ultimo_sueldo']:,.0f}",delta=f"{round(variacion_ultimo_sueldo,1)*100}%")
    
    
    col5, col6  = st.columns(2)
    col5.metric(label="Total datos", value=len(dataframe_datos))        
    col6.metric(label=f"Ultimo sueldo anual ( {st.session_state['ultimo_ano']})" ,value=f"{st.session_state['datos_imp_sueldos_totales_ultimo_ano']:,.0f}",delta=f"{round(variacion_sueldo_ultimo_ano,1)*100}%")
    
     
            
        
def grafico_sueldos_agrupados():          
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
        #filtro_sueldo = mov.prepara_ingresos()
        #datos.reset_index(inplace=True)
        filtro_sueldo = st.session_state['sueldos_agrupados_mes_ano'][st.session_state['sueldos_agrupados_mes_ano'].ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]
        filtro_sueldo = filtro_sueldo[filtro_sueldo.mes.isin([1,2,3,4,5,6,7,8,9,10,11,12])]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        nombres = ['Peso', 'Dolar']
        columnas = ['val_abs','val_abs_usd_ccl']
        secundario = [False, True, True]
        fff = []
        for x in range(len(filtro_sueldo)):
            fff.append(f"{filtro_sueldo.ano.iloc[x]} - { filtro_sueldo.mes.iloc[x]}")

        for nom, secu, col in zip(nombres, secundario, columnas):
            dato = filtro_sueldo[col].to_numpy()
            fig.add_trace(
                go.Scatter(x=fff, y=dato, name=nom), secondary_y=secu)

        st.plotly_chart(fig)
        
        
def graf_mejor_ano():
    import plotly.express as px
    filtro = st.session_state['mejor_ano']
    filtro = filtro[filtro.ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]  
    fig = px.bar(filtro, x='ano', y=st.session_state['moneda'], color=st.session_state['moneda'],
                 labels={st.session_state['moneda']: 'Ingresos anuales', 'ano': 'Año'})
    st.plotly_chart(fig)      
    
def graf_mejor_mes():
    import plotly.express as px
    filtro = st.session_state['mejor_mes']
    fig = px.bar(filtro, x='mes', y=st.session_state['moneda'], color=st.session_state['moneda'],
                 labels={st.session_state['moneda']: 'Ingresos anuales', 'mes': 'Mes'})

    st.plotly_chart(fig)    
    
    
def graf_mapacalor():
    import plotly.graph_objects as go
    filtro = st.session_state['pivot']     
    datos = filtro.to_numpy()
    trace = go.Heatmap(
        x=st.session_state['anos'],
        y=[1,2,3,4,5,6,7,8,9,10,11,12],
        z=datos,
        type='heatmap',
        colorscale='Viridis'
    )

    data = [trace]
    fig = go.Figure(data=data)
    fig.update_xaxes(title_text="Años")
    fig.update_yaxes(title_text="Meses")
    fig.update_layout(title_text='Mapa de calor : INGRESOS'
                      )

    st.plotly_chart(fig)   
    
def graf_cuadro_ingreso():
    filtro = st.session_state['sueldos_agrupados_mes_ano']
    filtro = filtro[filtro.ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]  
    import plotly.express as px
    fig = px.treemap(filtro, path=[px.Constant('Ingresos'), 'ano', 'mes'], values=st.session_state['moneda'],
                     color=st.session_state['moneda'], labels={st.session_state['moneda']: 'Ingresos'})  
    fig.update_layout(title_text='Cuadro : Ingresos'
                      )
    st.plotly_chart(fig)
 
 
def ing_repetidos():
    
    import plotly.express as px
    filtro = st.session_state['sueldos_agrupados_mes_ano']
    filtro = filtro[filtro.ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]
    if st.session_state['moneda']=="val_abs_usd_ccl":
        fig = px.histogram(filtro, x="val_abs_usd_ccl", labels={'val_abs_usd_ccl': 'Ingresos'},nbins=10)
        fig.update_layout(title_text='Histograma de sueldos en dolares')  
    else:
        fig = px.histogram(filtro, x="val_abs", labels={'val_abs': 'Ingresos'},nbins=10)
        fig.update_layout(title_text='Histograma de sueldos en pesos')              
            
    st.plotly_chart(fig)

    
    

def ing_media():
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    filtro = st.session_state['sueldos_agrupados_mes_ano']
    filtro = filtro[filtro.ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]    
    ano_mes=[str(x)+"-"+str(y) for x,y in zip (filtro.ano,filtro.mes)]    
    fig = make_subplots(rows=1)   
    fig.add_trace(go.Bar(x=ano_mes,
                  y=filtro[st.session_state['moneda']], name="Sueldos"))
    
    
    if st.session_state['moneda']=="val_abs_usd_ccl":
        fig.add_trace(
        go.Scatter(x=ano_mes, y=filtro.media_12_usd),
        row=1, col=1
)   
    else:
       fig.add_trace(
        go.Scatter(x=ano_mes, y=filtro.media_12),
        row=1, col=1
)    

    
    fig.update_layout(hovermode="x")
    st.plotly_chart(fig)


def sueldos_ordenados():
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    filtro = st.session_state['sueldos_agrupados_mes_ano']
    colores=['rgb(158,202,225)'for x in range(len(filtro.index))]
    
    filtro["ranking_dolar"]=filtro.val_abs_usd_ccl.rank(ascending=False)
    filtro["ranking_peso"]=filtro.val_abs.rank(ascending=False)
    filtro['colores']=colores
    filtro.colores.iloc[-1]="crimson"
    
    ranking=filtro.sort_values(by='ranking_dolar')
    lista_fechas_str=[f"{x[0]}/{x[1]}" for x in  zip(ranking.mes,ranking.ano)]
    ranking['orden']=lista_fechas_str
    
    if st.session_state['moneda']=="val_abs_usd_ccl":  
        fig=px.bar(ranking, x='ranking_dolar', y=st.session_state['moneda'], text="orden", color=ranking.colores)
        fig.update_yaxes(title="Dolares")
    
    else:    
        fig=px.bar(ranking, x='ranking_peso', y=st.session_state['moneda'], text="orden", color=ranking.colores)
        fig.update_yaxes(title="Dolares")
    fig.update_xaxes(showticklabels=False ,title="Sueldos ordenados por importancia")
    fig.update_layout(showlegend=False) 
    fig.update_layout(width=1100)
    st.plotly_chart(fig)
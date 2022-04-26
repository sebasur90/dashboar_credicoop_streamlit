import streamlit as st

def pagina_egresos_funcion():
    if "sueldos" not in st.session_state:        
        st.warning("primero debe cargar dataset")
    else:            
        st.title("Egresos")       
        st.caption("(No incluye transferencias)" )
        
        
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
        gastos_media()
        grafico_sueldos_agrupados()
        graf_peor_ano()
        graf_peor_mes()
        graf_mapacalor()
        graf_cuadro_gastos()           
        ing_repetidos()
        gastos_ordenados()
        gastos_donut_anuales()
        gastos_donut_concepto()



def datos_importantes(mon):   
    dataframe_datos=st.session_state['datos_procesados'][st.session_state['datos_procesados'].ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]
    filtro_gasto = st.session_state['gastos_agrupados_mes_ano'][st.session_state['gastos_agrupados_mes_ano'].ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]
    st.session_state['datos_imp_gastos_historicos_totales']=int(filtro_gasto[mon].sum())
    st.session_state['datos_imp_ultimo_gasto']=int(filtro_gasto[mon].iloc[-1] )    
    st.session_state['datos_imp_anteultimo_gasto']=int(filtro_gasto[mon].iloc[-2] )      
    variacion_ultimo_gasto=st.session_state['datos_imp_ultimo_gasto']/st.session_state['datos_imp_anteultimo_gasto']-1
    
    st.session_state['datos_imp_gastos_totales_ultimo_ano']=st.session_state['gastos_agrupados_ano'][st.session_state['gastos_agrupados_ano'].ano==st.session_state['sueldos_agrupados_ano'].ano.iloc[-1]][mon].iloc[0]
    
    st.session_state['datos_imp_gastos_totales_anteultimo_ano']=st.session_state['gastos_agrupados_ano'][st.session_state['gastos_agrupados_ano'].ano==st.session_state['sueldos_agrupados_ano'].ano.iloc[-2]][mon].iloc[0]
    variacion_gasto_ultimo_ano=st.session_state['datos_imp_gastos_totales_ultimo_ano']/st.session_state['datos_imp_gastos_totales_anteultimo_ano']-1
   
    
    
    col1, col2,col3  = st.columns(3)   
    col1.metric(label=f"Total gastos ({filtro_gasto.ano.iloc[0]}-{filtro_gasto.ano.iloc[-1]} )" ,value=f"{st.session_state['datos_imp_gastos_historicos_totales']:,.0f}")
        
    col2.metric(label=f"Ultimo gasto ({filtro_gasto.mes.iloc[-1]}/{filtro_gasto.ano.iloc[-1]}) " ,value=f"{st.session_state['datos_imp_ultimo_gasto']:,.0f}",delta=f"{round(variacion_ultimo_gasto,1)*100}%")
        
    col3.metric(label=f"Ultimo gasto anual ( {st.session_state['ultimo_ano']})" ,value=f"{st.session_state['datos_imp_gastos_totales_anteultimo_ano']:,.0f}",delta=f"{round(variacion_gasto_ultimo_ano,1)*100}%")
    
     
            
        
def grafico_sueldos_agrupados():          
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
        #filtro_sueldo = mov.prepara_Egresos()
        #datos.reset_index(inplace=True)
        filtro_sueldo = st.session_state['sueldos_agrupados_mes_ano'][st.session_state['gastos_agrupados_mes_ano'].ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]
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
        
        
def graf_peor_ano():
    import plotly.express as px
    filtro = st.session_state['peor_ano']
    filtro = filtro[filtro.ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]  
    fig = px.bar(filtro, x='ano', y=st.session_state['moneda'], color=st.session_state['moneda'],
                 labels={st.session_state['moneda']: 'Egresos anuales', 'ano': 'Año'})
    st.plotly_chart(fig)      
    
def graf_peor_mes():
    import plotly.express as px
    filtro = st.session_state['peor_mes']
    fig = px.bar(filtro, x='mes', y=st.session_state['moneda'], color=st.session_state['moneda'],
                 labels={st.session_state['moneda']: 'Egresos mensuales', 'mes': 'Mes'})

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
    fig.update_layout(title_text='Mapa de calor : Egresos'
                      )

    st.plotly_chart(fig)   
    
def graf_cuadro_gastos():
    filtro = st.session_state['gastos_agrupados_mes_ano']
    filtro = filtro[filtro.ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]  
    import plotly.express as px
    fig = px.treemap(filtro, path=[px.Constant('Egresos'), 'ano', 'mes'], values=st.session_state['moneda'],
                     color=st.session_state['moneda'], labels={st.session_state['moneda']: 'Egresos'})  
    fig.update_layout(title_text='Cuadro : Egresos'
                      )
    st.plotly_chart(fig)
 
 
def ing_repetidos():
    
    import plotly.express as px
    filtro = st.session_state['gastos_agrupados_mes_ano']
    filtro = filtro[filtro.ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]
    if st.session_state['moneda']=="val_abs_usd_ccl":
        fig = px.histogram(filtro, x="val_abs_usd_ccl", labels={'val_abs_usd_ccl': 'Egresos'},nbins=10)
        fig.update_layout(title_text='Histograma de gastos en dolares')  
    else:
        fig = px.histogram(filtro, x="val_abs", labels={'val_abs': 'Egresos'},nbins=10)
        fig.update_layout(title_text='Histograma de gastos en pesos')              
            
    st.plotly_chart(fig)

    
    

def gastos_media():
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    filtro = st.session_state['gastos_agrupados_mes_ano']
    filtro = filtro[filtro.ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]    
    ano_mes=[str(x)+"-"+str(y) for x,y in zip (filtro.ano,filtro.mes)]    
    fig = make_subplots(rows=1)   
    fig.add_trace(go.Bar(x=ano_mes,
                  y=filtro[st.session_state['moneda']], name="Gastos"))    
    
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


def gastos_ordenados():
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    filtro = st.session_state['gastos_agrupados_mes_ano']
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
    fig.update_xaxes(showticklabels=False ,title="gastos ordenados por importancia")
    fig.update_layout(showlegend=False) 
    fig.update_layout(width=1100)
    st.plotly_chart(fig)
    
def gastos_donut_anuales():
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    filtro = st.session_state['gastos']
    filtro = filtro[filtro.ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]    
    ano_mes=[str(x)+"-"+str(y) for x,y in zip (filtro.ano,filtro.mes)]         
    
    filtro=filtro.groupby(['concepto'], as_index=False)[st.session_state['moneda']].sum()
    filtro_ordenado=filtro.sort_values(st.session_state['moneda'],ascending=False)
    filtro_ordenado['cum_percent'] = 100*(filtro_ordenado[st.session_state['moneda']].cumsum() / filtro_ordenado[st.session_state['moneda']].sum())
    
    filtro_ordenado=filtro_ordenado[filtro_ordenado.cum_percent <=95]

    if st.session_state['moneda']=="val_abs_usd_ccl": 
        fig=px.pie(filtro_ordenado, values=st.session_state['moneda'], names='concepto',
                 title="Gastos totales por año", hole=.5, labels={'val_abs_usd_ccl': 'Importe'}) 
    else:
        fig=px.pie(filtro_ordenado, values=st.session_state['moneda'], names='concepto',
                 title="Gastos totales por año", hole=.5, labels={st.session_state['moneda']: 'Importe'})
    
  
    st.plotly_chart(fig)    
    
def gastos_donut_concepto():
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    
    
    filtro = st.session_state['gastos']
    filtro = filtro[filtro.ano.isin(range(st.session_state['ano_inicio'],st.session_state['ano_fin']+1))]    
    filtro=filtro.groupby(['concepto',"ano"], as_index=False)[st.session_state['moneda']].sum()
    filtro_ordenado=filtro.sort_values(st.session_state['moneda'],ascending=False)
    conceptos=sorted(list(filtro_ordenado.concepto.unique()))
    option = st.selectbox(
     'Ver gastos por concepto',
     conceptos)
    filtro_ordenado=filtro_ordenado[filtro_ordenado.concepto==option]
    
    if st.session_state['moneda']=="val_abs_usd_ccl": 
        fig=px.pie(filtro_ordenado, values=st.session_state['moneda'], names='ano',
                 title="Gastos totales por año en dolares", hole=.5, labels={st.session_state['moneda']: 'Importe'}) 
    else:
        fig=px.pie(filtro_ordenado, values=st.session_state['moneda'], names='ano',
                 title="Gastos totales por año en pesos", hole=.5, labels={st.session_state['moneda']: 'Importe'})
    
  
    st.plotly_chart(fig)      
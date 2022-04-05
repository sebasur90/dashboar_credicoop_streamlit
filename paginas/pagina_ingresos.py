import streamlit as st

def pagina_ingresos_funcion():
    if "sueldos" not in st.session_state:
        st.write("primero debe cargar dataset")
        
    else:            
        st.title("pagina_ingresos")
        grafico_sueldos_agrupados()
        graf_mejor_ano()
        graf_mejor_mes()
        graf_mapacalor()
        graf_cuadro_ingreso()           
        ing_repetidos_pesos()
        ing_repetidos_usd()
        ing_media()
        
        
def grafico_sueldos_agrupados():          
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
        #filtro_sueldo = mov.prepara_ingresos()
        #datos.reset_index(inplace=True)
        filtro_sueldo = st.session_state['sueldos_agrupados_mes_ano'][st.session_state['sueldos_agrupados_mes_ano'].ano.isin([2018,2019,2020,2021,2022])]
        filtro_sueldo = filtro_sueldo[filtro_sueldo.mes.isin([1,2,3,4,5,6,7,8,9,10,11,12])]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        nombres = ['Peso', 'Dolar CCL']
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
    fig = px.bar(filtro, x='ano', y='val_abs_usd_ccl', color='val_abs_usd_ccl',
                 labels={'val_abs_usd_ccl': 'Ingresos anuales', 'ano': 'Año'})

    st.plotly_chart(fig)      
    
def graf_mejor_mes():
    import plotly.express as px
    filtro = st.session_state['mejor_mes']
    fig = px.bar(filtro, x='mes', y='val_abs_usd_ccl', color='val_abs_usd_ccl',
                 labels={'val_abs_usd_ccl': 'Ingresos anuales', 'mes': 'Mes'})

    st.plotly_chart(fig)    
    
    
def graf_mapacalor():
    import plotly.graph_objects as go
    filtro = st.session_state['pivot']     
    datos = filtro.to_numpy()
    trace = go.Heatmap(
        x=[2018,2019,2020,2021,2022],
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
    import plotly.express as px
    fig = px.treemap(filtro, path=[px.Constant('Ingresos'), 'ano', 'mes'], values='val_abs_usd_ccl',
                     color='val_abs_usd_ccl', labels={'val_abs_usd_ccl': 'Ingresos'})  
    fig.update_layout(title_text='Mapa de calor : Ingresos'
                      )
    st.plotly_chart(fig)
 
 
def ing_repetidos_pesos():
    
    import plotly.express as px
    filtro = st.session_state['sueldos_agrupados_mes_ano']
    #filtro = filtro[filtro.ano.isin(ano_elegido)]
    fig = px.histogram(filtro, x="val_abs", labels={'val_abs': 'Ingresos'},nbins=10)
    fig.update_layout(title_text='Histograma de sueldos en pesos')   
    st.plotly_chart(fig)

def ing_repetidos_usd():
    import plotly.express as px
    filtro = st.session_state['sueldos_agrupados_mes_ano']
    #filtro = filtro[filtro.ano.isin(ano_elegido)]
    fig = px.histogram(filtro, x="val_abs_usd_ccl", labels={'val_abs_usd_ccl': 'Ingresos'},nbins=10)
    fig.update_layout(title_text='Histograma de sueldos en pesos')   
    st.plotly_chart(fig)
    
    

def ing_media():
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    filtro = st.session_state['sueldos_agrupados_mes_ano']
    #filtro = mov.agrupado("ano", "mes", mov.prepara_ingresos(), "dolar")
    #filtro = filtro[filtro.ano.isin(ano_elegido)]
    #print(filtro.ano, filtro.mes)
    ano_mes=[str(x)+"-"+str(y) for x,y in zip (filtro.ano,filtro.mes)]
    #fig = go.Figure() 
    fig = make_subplots(rows=1, cols=2)   
    fig.add_trace(go.Bar(x=ano_mes,
                  y=filtro.val_abs_usd_ccl, name="Sueldos en Dolares"))
    
    fig.add_trace(
    go.Scatter(x=ano_mes, y=filtro.media_12),
    row=1, col=1
)

    
    fig.update_layout(hovermode="x")
    st.plotly_chart(fig)



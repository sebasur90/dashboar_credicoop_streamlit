import streamlit as st
#import pandas as pd
#from paginas.pag_prepro import prepro
#from paginas.pag_random_forest import random_forest
#from paginas.pag_pca import page_pca
#from paginas.pag_knn import page_knn
#from paginas.pag_principal_datos import principal_datos
import streamlit.components.v1 as components
import pandas as pd
from funciones_para_datasets import procesa_cotizacion
from funciones_para_datasets import procesar_datos
from paginas.pagina_ingresos import pagina_ingresos_funcion
from paginas.pagina_movimientos import pagina_movimientos_funcion

def main():
    pages = {
        "Home": page_home,
        "pagina_ingresos":pagina_ingresos_funcion,
        "Movimientos": pagina_movimientos_funcion,
        # "PCA":page_pca,
        # "Random forest":random_forest,
        # "KNN: vecinos mas cercanos":page_knn

    }

    # If 'page' is present, update session_state with itself to preserve
    # values when navigating from Home to Settings.
    if "page" in st.session_state:
        st.session_state.update(st.session_state)

    # If 'page' is not present, setup default values for settings widgets.
    else:
        st.session_state.update({
            # Default page
            "page": "Home",
        })

    with st.sidebar:
        page = st.radio("Select your page", tuple(pages.keys()))

    pages[page]()


def page_home():
    st.title("Dashboard Credicoop")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:        
        with st.spinner('Por favor esperar el procesamiento...'):               

            st.session_state['dataframe_original'] = pd.read_csv(uploaded_file,sep =';')        
            procesa_cotizacion.proceso(str(st.session_state['dataframe_original']['FECHA'].iloc[-1]))       
            procesar_datos.proceso()
            st.success('Listo')
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Total datos", value=len(st.session_state['dataframe_original']))
            #col1.metric("Temperature", "70 °F", "1.2 °F")
            col2.metric("Wind", "9 mph", "-8%")
            col3.metric("Humidity", "86%", "4%")


    


if __name__ == "__main__":
    main()

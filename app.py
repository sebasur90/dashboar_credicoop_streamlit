import streamlit as st
#import pandas as pd
#from paginas.pag_prepro import prepro
#from paginas.pag_random_forest import random_forest
#from paginas.pag_pca import page_pca
#from paginas.pag_knn import page_knn
#from paginas.pag_principal_datos import principal_datos
import streamlit.components.v1 as components



def main():
    pages = {
        "Home": page_home,
       
        #"Carga datos":principal_datos,
        #"Preprocesamiento": prepro,
        #"PCA":page_pca,
        #"Random forest":random_forest,
        #"KNN: vecinos mas cercanos":page_knn
        
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
    st.title("Modelos de machine learning")
    
    col1, col2 = st.columns(2)

    with col1:
        st.session_state['nombre_dataset'] = st.selectbox(
     'Seleccionar dataset',
     ('Iris', 'Insurance'))

        st.write('Dataset seleccionado :', st.session_state['nombre_dataset'])

    with col2:
        st.session_state['nombre_variable_objetivo'] = str(st.selectbox(
     'Seleccionar variable objetivo',
     ('Species', 'smoker')))

        st.write('Objetivo seleccionado:', st.session_state['nombre_variable_objetivo'])

    
 

if __name__ == "__main__":
    main()
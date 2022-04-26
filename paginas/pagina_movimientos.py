import streamlit as st

def pagina_movimientos_funcion():
    
    if "sueldos" not in st.session_state:
        st.warning("primero debe cargar dataset")
        
    else:            
        st.title("Movimientos")        
        st.dataframe(st.session_state['datos_procesados'],width=900, height=768 )
        
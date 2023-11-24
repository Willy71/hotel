import streamlit as st
import pandas as pd
import webbrowser
import datetime
from datetime import datetime

# Colocar nome na pagina, icone e ampliar a tela
st.set_page_config(
    page_title="Reservations",
    page_icon=":house",
    layout="wide"
)

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://i.postimg.cc/jdtSsJ9t/jr-korpa-H-BJWTh-ZRok-unsplash.jpg");
background-size: 180%;
background-position: top left;
background-repeat: repeat;
background-attachment: local;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}

[data-testid="stSidebar"] {{
background: rgba(28,28,56,1);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


def centrar_imagen(imagen, ancho):
    # Aplicar estilo CSS para centrar la imagen con Markdown
    st.markdown(
        f'<div style="display: flex; justify-content: center;">'
        f'<img src="{imagen}" width="{ancho}">'
        f'</div>',
        unsafe_allow_html=True
    )


def centrar_texto(texto, tamanho, color):
    st.markdown(f"<h{tamanho} style='text-align: center; color: {color}'>{texto}</h{tamanho}>",
                unsafe_allow_html=True)

st.write("#")

with st.container():    
    col01, col02, col03, col04 = st.columns(4)
    with col02:
        opciones_numericas = list(range(31))
        option = st.selectbox("Room", opciones_numericas, index=None, placeholder="Select a room...")
    with col03:
        opciones_numericas = list(range(11))
        option = st.selectbox("Number of guests", opciones_numericas, index=None, placeholder="Guests...")


with st.container():    
    col11, col12, col13, col14 = st.columns(4)
    with col12:
        t = st.time_input('Check in time', value=None)
    with col13:
        d = st.date_input("Date of admission", format="DD.MM.YYYY")

with st.container():    
    col21, col22, col23, col24 = st.columns(4)
    with col22:
        t = st.time_input('Check out time', value=None)
    with col23:
        d = st.date_input("Departure date", format="DD.MM.YYYY")

with st.container():    
    col31, col32, col33, col34 = st.columns(4)
    with col32:
        first_name = st.text_input('First name')
    with col33:
        last_name = st.text_input('Last name')
        
        







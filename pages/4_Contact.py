import streamlit as st
import pandas as pd
import webbrowser
from datetime import datetime

# Colocar nome na pagina, icone e ampliar a tela
st.set_page_config(
    page_title="Contact",
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
    col60, col61, col62, col63, col64, col65, col66, cl67 = st.columns(8)
    with col61:
        centrar_texto("[Kaggle](https://www.kaggle.com/willycerato)", 7, "blue")
    with col62:
        centrar_texto("[Github](https://github.com/Willy71)", 7, "blue")
    with col63:
        centrar_texto("[Instagram](https://www.instagram.com/willycerato)", 7, "blue")
    with col64:
        centrar_texto("[Facebook](https://www.facebook.com/guillermo.cerato)", 7, "blue")
    with col65:
        centrar_texto("[Whatsapp](https://wa.me/5542991657847)", 7, "blue")

st.title("")

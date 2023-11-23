import streamlit as st
import pandas as pd
import webbrowser
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

centrar_texto("Free application for temporary rental management. If you want customization of this project, consult with our developer.", 7, "white")

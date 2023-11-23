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
    col50, col51, col52, col53, col54 = st.columns(5)
    with col51:
        centrar_imagen("https://e7.pngegg.com/pngimages/399/47/png-clipart-kaggle-predictive-modelling-data-science-business-predictive-analytics-%E6%95%B0%E6%8D%AE-blue-text.png", 50)
    with col52:
        centrar_imagen("https://cdn-icons-png.flaticon.com/512/25/25231.png", 50)
    with col53:
        centrar_imagen("https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Instagram_logo_2022.svg/150px-Instagram_logo_2022.svg.png", 50)
            
with st.container():    
    col60, col61, col62, col63, col64 = st.columns(5)
    with col61:
        centrar_texto("[Kaggle](https://www.kaggle.com/willycerato)", 7, "blue")
    with col62:
        centrar_texto("[Github](https://github.com/Willy71)", 7, "blue")
    with col63:
        centrar_texto("[Instagram](https://www.instagram.com/willycerato)", 7, "blue")
    
st.title("")
st.title("")

with st.container():    
    col55, col56, col57, col58, col59 = st.columns(5)
    with col56:
        centrar_imagen("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/2023_Facebook_icon.svg/50px-2023_Facebook_icon.svg.png", 50)
    with col57:
        centrar_imagen("https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/LinkedIn_2021.svg/200px-LinkedIn_2021.svg.png", 50)        
    with col58:
        centrar_imagen("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/120px-WhatsApp.svg.png", 50)

with st.container():    
    col65, col66, col67, col68, col69 = st.columns(5)
    with col66:
        centrar_texto("[Facebook](https://www.facebook.com/guillermo.cerato)", 7, "blue")
    with col67:
        centrar_texto("[Linkedin](https://www.linkedin.com/in/willycerato/)", 7, "blue")
    with col68:
        centrar_texto("[Whatsapp](https://wa.me/5542991657847)", 7, "blue")


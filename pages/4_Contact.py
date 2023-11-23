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

def photo_link(nombre, imagen, link):
    st.markdown(f"[![{nombre}]({imagen} =80x80)]({link})"{:width="100px"})

st.write("#")

with st.container():    
    col50, col51, col52, col53, col54 = st.columns(5)
    with col51:
        photo_link("Kaggle", "https://e7.pngegg.com/pngimages/399/47/png-clipart-kaggle-predictive-modelling-data-science-business-predictive-analytics-%E6%95%B0%E6%8D%AE-blue-text.png", "https://www.kaggle.com/willycerato")
    with col52:
        photo_link("Github", "https://static.vecteezy.com/system/resources/previews/016/833/880/non_2x/github-logo-git-hub-icon-with-text-on-white-background-free-vector.jpg", "https://github.com/Willy71")
    with col53:
        photo_link("Instagram", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Instagram_logo_2022.svg/150px-Instagram_logo_2022.svg.png", "https://www.instagram.com/willycerato")
            
st.title("")
st.title("")

with st.container():    
    col55, col56, col57, col58, col59 = st.columns(5)
    with col56:
        photo_link("Facebook", "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/2023_Facebook_icon.svg/50px-2023_Facebook_icon.svg.png", "https://www.facebook.com/guillermo.cerato")
    with col57:
        photo_link("Linkedin", "https://img.freepik.com/vetores-premium/logotipo-quadrado-do-linkedin-isolado-no-fundo-branco_469489-892.jpg", "https://www.linkedin.com/in/willycerato")        
    with col58:
        photo_link("Whatsapp", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/120px-WhatsApp.svg.png", "Whatsapp](https://wa.me/5542991657847")

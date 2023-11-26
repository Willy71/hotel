import streamlit as st
import pandas as pd
import webbrowser
from datetime import datetime

# Colocar nome na pagina, icone e ampliar a tela
st.set_page_config(
    page_title="Hotels Service",
    page_icon=":house",
    layout="wide",
    initial_sidebar_state="collapsed",  # Opciones: 'auto', 'expanded', 'collapsed'
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

from gsheetsdb import connect

# Share the connector across all users connected to the app
@st.experimental_singleton()
def get_connector():
    return connect()

# Time to live: the maximum number of seconds to keep an entry in the cache
TTL = 24 * 60 * 60

# Using `experimental_memo()` to memoize function executions
@st.experimental_memo(ttl=TTL)
def query_to_dataframe(_connector, query: str) -> pd.DataFrame:
    rows = _connector.execute(query, headers=1)
    df = pd.DataFrame(list(rows))
    return df

@st.experimental_memo(ttl=600)
def get_data(_connector, gsheets_url) -> pd.DataFrame:
    return query_to_dataframe(_connector, f'SELECT * FROM "{gsheets_url}"')

st.markdown(f"## 📝 Connecting to a public Google Sheet")

gsheet_connector = get_connector()
gsheets_url = st.secrets["gsheets"]["public_gsheets_url"]

data = get_data(gsheet_connector, gsheets_url)
st.write("👇 Find below the data in the Google Sheet you provided in the secrets:")
st.dataframe(data)


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

def photo_link(alt_text, img_url, link_url, img_width):
    markdown_code = f'<a href="{link_url}" target="_blank"><img src="{img_url}" alt="{alt_text}" width="{img_width}"></a>'
    st.markdown(markdown_code, unsafe_allow_html=True)

st.write("#")

centrar_imagen("https://i.postimg.cc/kg86jt2S/Your-Company-removebg-preview.png", 300)
st.markdown("")

st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

centrar_imagen("https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Flag_of_the_United_Kingdom_%283-5%29.svg/255px-Flag_of_the_United_Kingdom_%283-5%29.svg.png", 50)
st.markdown("")
centrar_texto("Application for temporary rental management.", 5, "white")
centrar_texto("If you want customization of this project, consult with our developer.", 5, "white")

col1, col2, col3 = st.columns([5, 3.7, 2])  # Establecer anchos personalizados (en este caso, la columna central es el doble de ancha)
with col2:
    photo_link("Whatsapp", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/120px-WhatsApp.svg.png", "https://wa.me/5542991657847", "50px")



st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

centrar_imagen("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Flag_of_Spain.svg/255px-Flag_of_Spain.svg.png", 50)
st.markdown("")
centrar_texto("Aplicacion para la administración de alquileres temporarios.", 5, "white")
centrar_texto("Si desea una personalizacion de este proyecto consulte con nuestro desarrollador.", 5, "white")

col4, col5, col6 = st.columns([5, 3.7, 2])
with col5:
    photo_link("Whatsapp", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/120px-WhatsApp.svg.png", "https://wa.me/5542991657847", "50px")

st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

centrar_imagen("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Flag_of_Portugal.svg/260px-Flag_of_Portugal.svg.png", 50)
st.markdown("")
centrar_texto("Aplicativo para gerenciamento de aluguel temporário.", 5, "white")
centrar_texto("Caso queira customização deste projeto consulte nosso desenvolvedor.", 5, "white")

col7, col8, col9 = st.columns([5, 3.7, 2])
with col8:
    photo_link("Whatsapp", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/120px-WhatsApp.svg.png", "https://wa.me/5542991657847", "50px")

st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)



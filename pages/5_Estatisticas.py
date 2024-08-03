import streamlit as st
import pandas as pd
import webbrowser
from datetime import datetime
import re
import gspread
from google.oauth2.service_account import Credentials

# Colocar nome na pagina, icone e ampliar a tela
st.set_page_config(
    page_title="Rooms",
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
background: rgba(0,0,0,0);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

#=============================================================================================================================
# Conexion via gspread a traves de https://console.cloud.google.com/ y Google sheets

# Ruta al archivo de credenciales
SERVICE_ACCOUNT_INFO = st.secrets["gsheets"]

# Scopes necesarios
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Cargar credenciales y autorizar
credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
gc = gspread.authorize(credentials)

# Clave de la hoja de cálculo (la parte de la URL después de "/d/" y antes de "/edit")
SPREADSHEET_KEY =  st.secrets["gsheets"]["SPREADSHEET_KEY"]  # Reemplaza con la clave de tu documento
SHEET_NAME = 'Hoja1'  # Nombre de la hoja dentro del documento

try:
    worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet(SHEET_NAME)
    existing_data = pd.DataFrame(worksheet.get_all_records())
except gspread.exceptions.SpreadsheetNotFound:
    st.error(f"No se encontró la hoja de cálculo con la clave '{SPREADSHEET_KEY}'. Asegúrate de que la clave es correcta y que has compartido la hoja con el correo electrónico del cliente de servicio.")
#=============================================================================================================================

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

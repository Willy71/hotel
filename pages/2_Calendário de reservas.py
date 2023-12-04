import streamlit as st
from datetime import datetime
from streamlit_calendar import calendar
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g

# Colocar nome na pagina, icone e ampliar a tela
st.set_page_config(
    page_title="Calendar",
    page_icon=":house",
    layout="wide"
)

# ----------------------------------------------------------------------------------------------------------------------------
# Colocar el background y definir los colores del sidebar
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
# ----------------------------------------------------------------------------------------------------------------------------
# Establishing a Google Sheets connection
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Hoja1", usecols=list(range(22)), ttl=5)
existing_data = existing_data.dropna(how="all")

# ----------------------------------------------------------------------------------------------------------------------------

# Función para obtener los datos de ocupación desde Google Sheets
def obtener_datos_ocupacion():
    # Configurar las credenciales para acceder a Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/your/credentials.json", scope)
    client = gspread.authorize(creds)

    # Obtener la hoja de cálculo
    sheet = client.open("Nombre de tu hoja de cálculo").sheet1

    # Leer los datos en un DataFrame de pandas
    df = pd.DataFrame(sheet.get_all_records())

    return df

# Función para marcar días de ocupación en el calendario
def marcar_dias_ocupados(months, datos_ocupacion):
    marked_dates = []

    for _, row in datos_ocupacion.iterrows():
        fecha_ocupacion = datetime.strptime(row["Fecha"], "%Y-%m-%d").date()
        if fecha_ocupacion.month in months:
            marked_dates.append(fecha_ocupacion)

    return marked_dates

# Cargar datos de ocupación
datos_ocupacion = obtener_datos_ocupacion()

# Configuración de la aplicación Streamlit
st.title("Calendario de Ocupación")

# Calendario multimonth
months = st.multiselect("Seleccione los meses:", list(range(1, 13)), [1, 2, 3])
marked_dates = marcar_dias_ocupados(months, datos_ocupacion)

# Mostrar el calendario con días de ocupación marcados en rojo
selected_dates = st.calendar(marked_dates=marked_dates, key="cal")

# Mostrar los días seleccionados
st.write("Días seleccionados:", selected_dates)



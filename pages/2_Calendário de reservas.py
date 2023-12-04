import streamlit as st
from datetime import datetime
from streamlit_calendar import calendar
import pandas as pd
from streamlit_gsheets import GSheetsConnection

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

# Function to mark occupied dates in the calendar
def mark_occupied_dates(months, occupancy_data):
    marked_dates = []

    for _, row in occupancy_data.iterrows():
        fecha_ocupacion = datetime.strptime(row["Data de entrada"], "%Y-%m-%d").date()
        if fecha_ocupacion.month in months:
            marked_dates.append(fecha_ocupacion)

    return marked_dates

# Streamlit app setup
st.title("Calendario de Ocupación")

# Multiselect for selecting months
months = st.multiselect("Selecione os meses:", list(range(1, 13)), [1, 2, 3])

# Mark occupied dates based on the selected months
marked_dates = mark_occupied_dates(months, existing_data)

# Calendar display with marked occupied dates in red
selected_dates = st.calendar(marked_dates=marked_dates, key="cal")

# Display the selected dates
st.write("Días selecionados:", selected_dates)

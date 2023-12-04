import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components
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
# Obtener las fechas ocupadas

def get_occupied_dates(selected_room, occupancy_data):
    marked_dates = []

    for _, row in occupancy_data[occupancy_data["Quarto"] == selected_room].iterrows():
        fecha_entrada = datetime.strptime(row["Data de entrada"], "%d/%m/%Y")

        # Verificar si la columna "Data de saida" existe en el DataFrame
        if "Data de saida" in row.index:
            fecha_saida = datetime.strptime(row["Data de saida"], "%d/%m/%Y")
        else:
            # En caso de que no exista, asumir una salida para evitar errores
            fecha_saida = fecha_entrada

        # Añadir días al rango de fechas
        current_date = fecha_entrada
        while current_date <= fecha_saida:
            marked_dates.append({
                'title': 'Ocupado',
                'start': current_date.strftime("%Y-%m-%d")
            })
            current_date += timedelta(days=1)

    return marked_dates

# ----------------------------------------------------------------------------------------------------------------------------

# Configuración inicial
st.title("Calendario de Ocupação")

# Widget para seleccionar el "Quarto" (Room)
room_options = sorted(existing_data["Quarto"].astype(int).unique())
selected_room = st.selectbox("Selecione o Quarto:", room_options)

# Obtener las fechas ocupadas para la habitación seleccionada
marked_dates = get_occupied_dates(selected_room, existing_data)

# Crear el código JavaScript para inicializar FullCalendar
calendar_code = f"""
    <link rel="stylesheet" href="https://unpkg.com/@fullcalendar/core/main.css" />
    <script src="https://unpkg.com/@fullcalendar/core/main.js"></script>
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {{
            initialView: 'dayGridMonth',
            events: {marked_dates},
            dateClick: function(info) {{
                alert('Date clicked: ' + info.dateStr);
            }}
        }});
        calendar.render();
    }});
    </script>
"""

# Mostrar el calendario
st.markdown(calendar_code, unsafe_allow_html=True)
components.html("<div id='calendar'></div>", height=600)

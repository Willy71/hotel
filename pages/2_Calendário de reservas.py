import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# ----------------------------------------------------------------------------------------------------------------------------
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

# ----------------------------------------------------------------------------------------------------------------------------
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
# Función para marcar fechas ocupadas
def mark_occupied_dates(selected_room, occupancy_data):
    marked_dates = []

    for _, row in occupancy_data[occupancy_data["Quarto"] == selected_room].iterrows():
        fecha_entrada = datetime.strptime(row["Data de entrada"], "%d/%m/%Y")

        # Verificar si la columna "Data de saida" existe en el DataFrame
        if "Data de saída" in row.index:
            fecha_saida = datetime.strptime(row["Data de saída"], "%d/%m/%Y")
        else:
            # En caso de que no exista, asumir una salida para evitar errores
            fecha_saida = fecha_entrada

        # Añadir días al rango de fechas
        current_date = fecha_entrada
        while current_date <= fecha_saida:
            marked_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)

    return marked_dates

# ----------------------------------------------------------------------------------------------------------------------------
# Streamlit app setup
st.title("Calendario de Ocupação")

# Widget para seleccionar el "Quarto" (Room)
room_options = sorted(existing_data["Quarto"].astype(int).unique())
selected_room = st.selectbox("Selecione o Quarto:", room_options)

# Filtrar los datos según la habitación seleccionada
filtered_data = existing_data[existing_data["Quarto"] == selected_room]

# Marcar las fechas ocupadas según el cuarto seleccionado
marked_dates = mark_occupied_dates(selected_room, filtered_data)

# Crear un DataFrame para usar con Plotly Express
df_calendar = pd.DataFrame({"Date": marked_dates})

# Crear un gráfico de calendario con Plotly Express
fig = px.timeline(df_calendar, x_start="Date", x_end="Date", title="Calendario de Ocupação")

# Configuración adicional del diseño
fig.update_yaxes(showticklabels=False, visible=False)
fig.update_xaxes(showticklabels=False)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

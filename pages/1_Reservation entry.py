import streamlit as st
import pandas as pd
import webbrowser
import datetime
import re
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

with st.container():    
    col01, col02, col03, col04 = st.columns(4)
    with col02:
        opciones_numericas = list(range(31))
        option = st.selectbox("Room", opciones_numericas, index=None, placeholder="Select a room...")
    with col03:
        opciones_numericas = list(range(11))
        option = st.selectbox("Number of guests", opciones_numericas, index=None, placeholder="Guests...")


with st.container():    
    col11, col12, col13, col14 = st.columns(4)
    with col12:
        t = st.time_input('Check in time', value=None)
    with col13:
        d = st.date_input("Date of admission", format="DD.MM.YYYY")

with st.container():    
    col21, col22, col23, col24 = st.columns(4)
    with col22:
        t = st.time_input('Check out time', value=None)
    with col23:
        d = st.date_input("Departure date", format="DD.MM.YYYY")

with st.container():    
    col31, col32, col33, col34 = st.columns(4)
    with col32:
        first_name = st.text_input('First name')
    with col33:
        last_name = st.text_input('Last name')

def validar_email(email):
    # Expresión regular para validar direcciones de correo electrónico
    patron_email = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    if re.match(patron_email, email):
        return True
    else:
        return False

def validar_numero_telefono(numero):
    # Define una expresión regular para un número de teléfono
    patron = re.compile(r'^\d{11}$')  # Asumiendo un formato de 10 dígitos, ajusta según tus necesidades
    # Comprueba si el número coincide con el patrón
    if patron.match(numero):
        return True
    else:
        return False

with st.container():    
    col41, col42, col43, col44 = st.columns(4)
    with col42:
        email_input = st.text_input("Enter a valid email:")
    with col43:
        if validar_email(email_input):
            st.success("¡The email address is valid!")
        else:
            st.error("The email address is not valid. Please enter a valid address.")

# Lista de prefijos telefónicos internacionales
prefijos = {'Estados Unidos': '+1',
            'Canadá': '+1',
            'Brasil': '+55',
            'Argentina': '+54',
            'Reino Unido': '+44',
            'Australia': '+61',
            'India': '+91',
            # Agrega más países según sea necesario
           }

# Función para obtener el prefijo seleccionado
def obtener_prefijo(pais):
    return prefijos.get(pais, '')

with st.container():    
    col51, col52, col53, col54 = st.columns(4)
    with col52:
        # Selecciona el país desde el selectbox
        pais_seleccionado = st.selectbox('Select a country', list(prefijos.keys()))
    with col53:
        numero_telefono = st.text_input("Enter your phone number:")
    with col54:
        st.text("")
        # Validar el número de teléfono continuamente
        if validar_numero_telefono(numero_telefono):
            st.success("Valid phone number!")
        else:
            st.error("Invalid phone number. Enter a 10-digit number.")

with st.container():    
    col61, col62, col63, col64 = st.columns(4)
    with col62:
        street = st.text_input('Street')
    with col63:
        street_number = st.text_input('Street number')

with st.container():    
    col71, col72, col73, col74 = st.columns(4)
    with col72:
        city = st.text_input('City')
    with col73:
        state = st.text_input('State')
    with col74:
        zip_code = st.text_input('Zip code')

with st.container():    
    col81, col82, col83, col84 = st.columns(4)
    with col82:
        opciones_pago = ["Credit card", "Cash", "Debit"]
        option = st.selectbox("Payment", opciones_pago, index=None, placeholder="Payment option...")
    with col83:
        opciones_saldo = ["Full payment", "Partial payment", "No reservation payment"]
        option = st.selectbox("Pay", opciones_saldo, index=None, placeholder="Pay...")
    with col84:
        pay = st.number_input('Insert a pay')


        
        







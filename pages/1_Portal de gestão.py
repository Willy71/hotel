import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import re

# ----------------------------------------------------------------------------------------------------------------------------------
# Colocar nome na pagina, icone e ampliar a tela
st.set_page_config(
    page_title="Reservations",
    page_icon=":house",
    layout="wide"
)

# ----------------------------------------------------------------------------------------------------------------------------------
# Colocar background
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
# ----------------------------------------------------------------------------------------------------------------------------------
# Titulo de la pagina
st.title("Portal de gestão")

# ----------------------------------------------------------------------------------------------------------------------------------
# Establecer conexion con Google Sheets
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Hoja1", usecols=list(range(22)), ttl=5)
existing_data = existing_data.dropna(how="all")

df = st.dataframe(existing_data)

# ----------------------------------------------------------------------------------------------------------------------------------
# Definir funciones a ser usadas:

# Función para obtener el próximo ID disponible
def obtener_proximo_id(df):
    if df.empty:
        return 1
    else:
        return df['ID_usuario'].max() + 1
        

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
        
# ----------------------------------------------------------------------------------------------------------------------------------
# Constantes

# Lista de prefijos telefónicos internacionales
import phonenumbers as pn
import pycountry

prefijos = {c.alpha_2: pn.country_code_for_region(c.alpha_2) for c in pycountry.countries}

# prefijos = {'Estados Unidos': '+1',
#            'Canadá': '+1',
#            'Brasil': '+55',
#            'Argentina': '+54',
#            'Reino Unido': '+44',
#            'Australia': '+61',
#            'India': '+91',
#            Agrega más países según sea necesario
#           }

# Función para obtener el prefijo seleccionado
def obtener_prefijo(pais):
    return prefijos.get(pais, '')

st.write("#")

# ----------------------------------------------------------------------------------------------------------------------------------
# Seleccion de la opcion de CRUD
action = st.selectbox(
    "Escolha uma ação",
    [
        "Adicionar nova reserva", # Insert
        "Atualizar reserva existente", # Update
        "Ver todos as reservas", # View
        "Apagar reserva", # Delete
    ],
)
# ----------------------------------------------------------------------------------------------------------------------------------
# Formulario

if action == "Adicionar nova reserva":
    st.markdown("Insira os detalhes da nova reserva")
    with st.form(key="reservation"):
        with st.container():    
            col00, col01, col02, col03, col04 = st.columns([2, 2, 2, 1, 3])
            with col00:
                opciones_numericas = list(range(31))
                room = st.selectbox("Quarto", opciones_numericas, index=None, placeholder="Selecione um quarto...")
            with col01:
                opciones_numericas_2 = list(range(11))
                guests = st.selectbox("Quantidade de hospedes", opciones_numericas_2, index=None, placeholder="Hospedes...")
        
        with st.container():    
            col10, col11, col12, col13, col14, col15, col16 = st.columns([1, 2, 2, 0.5, 2, 2, 1])
            with col11:
                checkin_time = st.time_input('Hora de entrada', value=None)
            with col12:
                admission_date = st.date_input("Data de entrada", format="DD.MM.YYYY")
            with col14:
                checkout_time = st.time_input('Hora de saida', value=None)
            with col15:
                departure_date = st.date_input("Data de saida", format="DD.MM.YYYY")
        
        with st.container():    
            col30, col31, col32, col33, col34 = st.columns([2, 2, 2, 0.2, 3.8])
            with col30:
                first_name = st.text_input('Primeiro nome')
            with col31:
                last_name = st.text_input('Sobrenome')
            with col32:
                email = st.text_input("Entre um email válido:")
            with col34:
                st.text("")
                if validar_email(email):
                    st.success("¡El email é valido!")
                else:
                    st.error("O endereço de e-mail não é válido.")
             
        
        with st.container():    
            col40, col41, col42, col43, col44 = st.columns([2, 2, 0.2, 0.2, 5.6])
            with col40:
                # Selecciona el país desde el selectbox
                country = st.selectbox('Selecione um pais', list(prefijos.keys()))
            with col41:
                phone_number = st.text_input("Número de telefone:")
            with col44:
                st.text("")
                # Validar el número de teléfono continuamente
                if validar_numero_telefono(phone_number):
                    st.success("Número de telefone valido!")
                else:
                    st.error("Não valido. Insira um número de 11 dígitos.")
        
        with st.container():    
            col50, col51, col52, col53, col54 = st.columns([4, 2, 2, 1, 1])
            with col50:
                street = st.text_input('Rua')
            with col51:
                street_number = st.text_input('Número da rua')
            with col52:
                department_number = st.text_input("Número de apartamento")
        
        with st.container():    
            col60, col61, col62, col63, col64 = st.columns([2, 2, 2, 1, 3])
            with col60:
                city = st.text_input('Cidade')
            with col61:
                state = st.text_input('Estado')
            with col62:
                zip_code = st.text_input('CEP')
        
        with st.container():    
            col70, col71, col72, col73, col74, col75 = st.columns([1, 2, 2, 2, 2, 1])
            with col71:
                total_cost = st.number_input(label="Costo total")       
            with col72:
                opciones_pago = ["Nenhum", "Cartão de crédito", "A vista", "Débito"]
                payment_option = st.selectbox("Pagamento", opciones_pago, index=None, placeholder="Opções de pagamento...")
            with col73:
                opciones_saldo = ["Nenhum", "Pago integral", "Pago parcial"]
                pay_option = st.selectbox("Pagamento", opciones_saldo, index=None, placeholder="Pagamento...")
            with col74:
                pay_amount = st.number_input(label='Inserir pagamento')
    
        with st.container():    
            col81, col82, col83, col84, col85 = st.columns([1.2, 1.2, 1, 1, 1])
            with col83:
                submit_button = st.form_submit_button("Enviar")
                if submit_button:
                    nuevo_id = obtener_proximo_id(df)
                    # Obtener los datos ingresados
                    data = pd.DataFrame(
                        [
                            {
                                'user_id': nuevo_id,
                                'Quarto': room,
                                'Hospedes': guests,
                                'Hora de entrada': checkin_time.isoformat() if checkin_time else None,
                                'Data de entrada': admission_date.isoformat() if admission_date else None,
                                'Hora de saida': checkout_time.isoformat() if checkout_time else None,
                                'Data de saida': departure_date.isoformat() if departure_date else None,
                                'Primeiro nome': first_name,
                                'Sobrenome': last_name,
                                'Email': email,
                                'Pais': country,
                                'Celular': phone_number,
                                'Rua': street,
                                'Numero': street_number,
                                'Apartamento': department_number,
                                'Cidade': city,
                                'Estado': state,
                                'CEP': zip_code,
                                'Costo total': total_cost,
                                'Forma de pagamento': payment_option,
                                'Opção de pagamento': pay_option,
                                'Quantia paga': pay_amount
                            }
                        ]
                    )
                    updated_df = pd.concat([existing_data, data], ignore_index=True)
                    conn.update(worksheet="Hoja1", data=updated_df)
                    st.success("Detalhes da reserva enviados com sucesso!")

# View All Vendors
elif action == "Ver todos as reservas":
    st.dataframe(existing_data)

# Delete Vendor
elif action == "Apagar reserva":
    vendor_to_delete = st.selectbox(
        "Selecione uma reserva para apagar", options=existing_data["Sobrenome"].tolist()
    )

    if st.button("Delete"):
        existing_data.drop(
            existing_data[existing_data["Sobrenome"] == vendor_to_delete].index,
            inplace=True,
        )
        conn.update(worksheet="Hoja1", data=existing_data)
        st.success("Reserva apagada com sucesso!")


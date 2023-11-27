import streamlit as st
import pandas as pd
import datetime
import re
import os
import boto3

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

# ----------------------------------------------------------------------------------------------------------------------------------
# Configura las credenciales de AWS S3
st.secrets['aws_s3'] = {
    'ACCESS_KEY_ID': 'AKIARV3P4L55RFKT7N7E',
    'SECRET_ACCESS_KEY': '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',
}

@st.experimental_singleton()
def get_connector():
    """Create a connector to AWS S3"""
    connector = boto3.Session(
        aws_access_key_id=st.secrets.aws_s3.ACCESS_KEY_ID,
        aws_secret_access_key=st.secrets.aws_s3.SECRET_ACCESS_KEY,
    ).resource("s3")
    return connector

# Time to live: the maximum number of seconds to keep an entry in the cache
TTL = 24 * 60 * 60

@st.experimental_memo(ttl=TTL)
def get_buckets(_connector) -> list:
    return [bucket.name for bucket in list(_connector.buckets.all())]

def to_tuple(s3_object):
    return (
        s3_object.key,
        s3_object.last_modified,
        s3_object.size,
        s3_object.storage_class,
    )

@st.experimental_memo(ttl=TTL)
def get_files(_connector, bucket) -> pd.DataFrame:
    files = list(s3.Bucket(name=bucket).objects.all())
    if files:
        df = pd.DataFrame(
            pd.Series(files).apply(to_tuple).tolist(),
            columns=["key", "last_modified", "size", "storage_class"],
        )
        return df

# st.markdown(f"## 📦 Connecting to AWS S3")

s3 = get_connector()
buckets = get_buckets(s3)
bucket = 'st-hotel-reservas'
# bucket = st.selectbox("Choose a bucket", buckets) if buckets else None

# Nombre del archivo CSV en el bucket de S3
csv_filename = 'reservations.csv'

# Ruta del archivo en S3
s3_path = f's3://{bucket}/{csv_filename}' if bucket else None


# if buckets:
#      st.write(f"🎉 Found {len(buckets)} bucket(s)!")
#     bucket = st.selectbox("Choose a bucket", buckets)
#     files = get_files(s3, bucket)
#     if isinstance(files, pd.DataFrame):
#         st.write(f"📁 Found {len(files)} file(s) in this bucket:")
#         st.dataframe(files)
#     else:
#         st.write(f"This bucket is empty!")
# else:
#     st.write(f"Couldn't find any bucket. Make sure to create one!")

# ----------------------------------------------------------------------------------------------------------------------------------

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

st.write("#")

with st.form(key="reservation"):
    with st.container():    
        col00, col01, col02, col03, col04 = st.columns([1, 2, 2, 2, 3])
        with col01:
            opciones_numericas = list(range(31))
            room = st.selectbox("Room", opciones_numericas, index=None, placeholder="Select a room...")
        with col02:
            opciones_numericas_2 = list(range(11))
            guests = st.selectbox("Number of guests", opciones_numericas_2, index=None, placeholder="Guests...")
    
    with st.container():    
        col10, col11, col12, col13, col14 = st.columns([1, 2, 2, 2, 3])
        with col11:
            checkin_time = st.time_input('Check in time', value=None)
        with col12:
            admission_date = st.date_input("Date of admission", format="DD.MM.YYYY")
    
    with st.container():    
        col20, col21, col22, col23, col24 = st.columns([1, 2, 2, 2, 3])
        with col21:
            checkout_time = st.time_input('Check out time', value=None)
        with col22:
            departure_date = st.date_input("Departure date", format="DD.MM.YYYY")
    
    with st.container():    
        col30, col31, col32, col33, col34 = st.columns([1, 2, 2, 2, 3])
        with col31:
            first_name = st.text_input('First name')
        with col32:
            last_name = st.text_input('Last name')
        with col33:
            email = st.text_input("Enter a valid email:")
        with col34:
            st.text("")
            if validar_email(email):
                st.success("¡The email address is valid!")
            else:
                st.error("The email address is not valid. Please enter a valid address.")
         
    
    with st.container():    
        col40, col41, col42, col43, col44 = st.columns([1, 2, 2, 2, 3])
        with col41:
            # Selecciona el país desde el selectbox
            country = st.selectbox('Select a country', list(prefijos.keys()))
        with col42:
            phone_number = st.text_input("Phone number:")
        with col44:
            st.text("")
            # Validar el número de teléfono continuamente
            if validar_numero_telefono(phone_number):
                st.success("Valid phone number!")
            else:
                st.error("Invalid phone number. Enter a 11-digit number.")
    
    with st.container():    
        col50, col51, col52, col53, col54 = st.columns([1, 2, 2, 2, 3])
        with col51:
            street = st.text_input('Street')
        with col52:
            street_number = st.text_input('Street number')
        with col53:
            department_number = st.text_input("Department number")
    
    with st.container():    
        col60, col61, col62, col63, col64 = st.columns([1, 2, 2, 2, 3])
        with col61:
            city = st.text_input('City')
        with col62:
            state = st.text_input('State')
        with col63:
            zip_code = st.text_input('Zip code')
    
    with st.container():    
        col70, col71, col72, col73, col74, col75 = st.columns(6)
        with col71:
            total_cost = st.number_input(label="Total cost")       
        with col72:
            opciones_pago = ["None", "Credit card", "Cash", "Debit"]
            payment_option = st.selectbox("Payment", opciones_pago, index=None, placeholder="Payment option...")
        with col73:
            opciones_saldo = ["None", "Full payment", "Partial payment"]
            pay_option = st.selectbox("Pay", opciones_saldo, index=None, placeholder="Pay...")
        with col74:
            pay_amount = st.number_input(label='Insert a pay')

    with st.container():    
        col81, col82, col83, col84, col85 = st.columns([1.2, 1.2, 1, 1, 1])
        with col83:
            input_submit = st.form_submit_button("submit")


if input_submit:
    # Obtener los datos ingresados
    data = {
        'Room': room,
        'Guests': guests,
        'Checkin Time': checkin_time.isoformat() if checkin_time else None,
        'Admission Date': admission_date.isoformat() if admission_date else None,
        'Checkout Time': checkout_time.isoformat() if checkout_time else None,
        'Departure Date': departure_date.isoformat() if departure_date else None,
        'First Name': first_name,
        'Last Name': last_name,
        'Email': email,
        'Country': country,
        'Phone Number': phone_number,
        'Street': street,
        'Street Number': street_number,
        'Department Number': department_number,
        'City': city,
        'State': state,
        'Zip Code': zip_code,
        'Total Cost': total_cost,
        'Payment Option': payment_option,
        'Pay Option': pay_option,
        'Pay Amount': pay_amount
    }
    # Convertir los datos a un DataFrame
    new_data_df = pd.DataFrame([data])

    # Descargar el archivo CSV existente desde S3 (si existe)
    import io

    # Descargar el archivo CSV existente desde S3 (si existe)
    try:
        s3_object = s3.Object(bucket, csv_filename)
        existing_data_df = pd.read_csv(io.BytesIO(s3_object.get()['Body'].read()))
    except FileNotFoundError:
        existing_data_df = pd.DataFrame()


    # Concatenar los nuevos datos con los existentes
    merged_data_df = pd.concat([existing_data_df, new_data_df], ignore_index=True)
    
    # Guardar el DataFrame combinado en un nuevo archivo CSV en S3
    merged_data_df.to_csv(csv_filename, index=False)
    if bucket:
        s3.meta.client.upload_file(csv_filename, bucket, csv_filename)
    
    # Eliminar el archivo local después de cargarlo en S3
    os.remove(csv_filename)

    # Mensaje de éxito
    centrar_texto("Reservation added successfully!!", 5, "green")
    centrar_texto("Sent", 5, "green")
else:
    centrar_texto("I haven't added this reservation yet.", 5, "red")


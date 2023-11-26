import streamlit as st
import pandas as pd
import boto3

# Obtener las credenciales de AWS S3 desde los secrets
access_key_id = st.secrets["aws_s3"]["ACCESS_KEY_ID"]
secret_access_key = st.secrets["aws_s3"]["SECRET_ACCESS_KEY"]

@st.experimental_singleton()
def get_connector():
    """Create a connector to AWS S3"""
    connector = boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    ).resource("s3")
    return connector
  
# Nombre del archivo CSV en el bucket de S3
csv_filename = 'reservations.csv'
bucket = 'connect-acc'  # Reemplaza con el nombre de tu bucket

# Descargar el archivo CSV desde S3
response = s3.get_object(Bucket=bucket, Key=csv_filename)
data = response['Body'].read().decode('utf-8')

# Convierte los datos a DataFrame
df = pd.read_csv(io.StringIO(data))

# Mostrar el DataFrame en una tabla de Streamlit
st.dataframe(df)

# Seleccionar una fila para eliminar
index_to_delete = st.number_input("Ingrese el índice de la reserva que desea eliminar:", min_value=0, max_value=len(df)-1)

# Botón para eliminar con confirmación
if st.button("Eliminar Reserva"):
    # Verificar si el índice es válido
    if 0 <= index_to_delete < len(df):
        # Mostrar ventana emergente de confirmación
        if st.confirm(f"¿Estás seguro de eliminar la reserva con índice {index_to_delete}?"):
            # Eliminar la reserva y actualizar el DataFrame
            df = df.drop(index_to_delete).reset_index(drop=True)

            # Guardar el DataFrame actualizado en S3
            df.to_csv(io.BytesIO(df.to_csv(index=False).encode()), index=False)
            s3.upload_fileobj(io.BytesIO(df.to_csv(index=False).encode()), bucket, csv_filename)

            # Mostrar mensaje de éxito
            st.success(f"Reserva con índice {index_to_delete} eliminada exitosamente.")
    else:
        st.error("Índice no válido. Por favor, ingrese un índice válido.")


import streamlit as st
import pandas as pd
import boto3
import io

# Intenta obtener las credenciales de AWS S3 desde los secrets
try:
    access_key_id = st.secrets["aws_s3"]["ACCESS_KEY_ID"]
    secret_access_key = st.secrets["aws_s3"]["SECRET_ACCESS_KEY"]
except KeyError:
    st.error("No se pudieron encontrar las credenciales en los secrets.")
    st.stop()

# Intenta crear el cliente de S3
try:
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )
except Exception as e:
    st.error(f"Error al crear el cliente de S3: {str(e)}")
    st.stop()

# Nombre del archivo CSV en el bucket de S3
csv_filename = 'reservations.csv'
bucket = 'connect-acc'  # Reemplaza con el nombre de tu bucket

# Intenta descargar el archivo CSV desde S3
try:
    response = s3.get_object(Bucket=bucket, Key=csv_filename)
    data = response['Body'].read().decode('utf-8')
except Exception as e:
    st.error(f"Error al descargar el archivo CSV desde S3: {str(e)}")
    st.stop()

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
        if st.checkbox(f"¿Estás seguro de eliminar la reserva con índice {index_to_delete}?"):
            # Eliminar la reserva y actualizar el DataFrame
            df = df.drop(index_to_delete).reset_index(drop=True)

            # Guardar el DataFrame actualizado en S3
            df.to_csv(io.BytesIO(df.to_csv(index=False).encode()), index=False)
            s3.upload_fileobj(io.BytesIO(df.to_csv(index=False).encode()), bucket, csv_filename)

            # Mostrar mensaje de éxito
            st.success(f"Reserva con índice {index_to_delete} eliminada exitosamente.")
    else:
        st.error("Índice no válido. Por favor, ingrese un índice válido.")

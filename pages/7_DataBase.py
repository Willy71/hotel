import streamlit as st
import pandas as pd
import boto3
import io

# Configura el cliente de S3
s3 = boto3.client(
    's3',
    aws_access_key_id='AKIARV3P4L557EZTCJ7A',
    aws_secret_access_key='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',
    region_name='sa-east-1'
)

# Nombre del archivo CSV en el bucket de S3
csv_filename = 'reservations_data.csv'
bucket = 'TU_BUCKET'  # Reemplaza con el nombre de tu bucket

# Descargar el archivo CSV desde S3
response = s3.get_object(Bucket=bucket, Key=csv_filename)
data = response['Body'].read().decode('utf-8')

# Convierte los datos a DataFrame
df = pd.read_csv(io.StringIO(data))

# Mostrar el DataFrame en una tabla de Streamlit
st.dataframe(df)


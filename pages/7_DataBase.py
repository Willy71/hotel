import streamlit as st
import pandas as pd
import boto3
import io

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
bucket = 'connect-acc'
# bucket = st.selectbox("Choose a bucket", buckets) if buckets else None

# Nombre del archivo CSV en el bucket de S3
csv_filename = 'reservations.csv'

# Ruta del archivo en S3
s3_path = f's3://{bucket}/{csv_filename}' if bucket else None
bucket = 'connect-acc'  # Reemplaza con el nombre de tu bucket

# Descargar el archivo CSV desde S3
response = s3.get_object(Bucket=bucket, Key=csv_filename)
data = response['Body'].read().decode('utf-8')

# Convierte los datos a DataFrame
df = pd.read_csv(io.StringIO(data))

# Mostrar el DataFrame en una tabla de Streamlit
st.dataframe(df)


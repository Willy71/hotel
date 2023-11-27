import streamlit as st
import pandas as pd
import webbrowser
from datetime import datetime

# Colocar nome na pagina, icone e ampliar a tela
st.set_page_config(
    page_title="Rooms",
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

import streamlit as st
import pandas as pd
import boto3

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

st.markdown(f"## 📦 Connecting to AWS S3")

s3 = get_connector()

buckets = get_buckets(s3)
if buckets:
    st.write(f"🎉 Found {len(buckets)} bucket(s)!")
    bucket = st.selectbox("Choose a bucket", buckets)
    files = get_files(s3, bucket)
    if isinstance(files, pd.DataFrame):
        st.write(f"📁 Found {len(files)} file(s) in this bucket:")
        st.dataframe(files)
    else:
        st.write(f"This bucket is empty!")
else:
    st.write(f"Couldn't find any bucket. Make sure to create one!")

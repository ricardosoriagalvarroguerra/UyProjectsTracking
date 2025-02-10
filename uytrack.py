import streamlit as st
import requests
import pandas as pd

# ------------------------------------------------------------------------------
# CONFIGURACIÓN DE STREAMLIT
# ------------------------------------------------------------------------------
st.set_page_config(page_title="Prueba de Conexión con IATI", layout="wide")
st.title("Prueba de Conexión al Endpoint de Transacciones IATI")

# ------------------------------------------------------------------------------
# CLAVE DE SUSCRIPCIÓN (API Key)
# ------------------------------------------------------------------------------
# Para la prueba, la clave se coloca directamente.
# En producción es mejor usar variables de entorno o st.secrets.
api_key = "3ed3705bd91943b7ad8583f88836ea51"

if not api_key:
    st.error("No se ha proporcionado la API Key de IATI.")
    st.stop()

# ------------------------------------------------------------------------------
# PETICIÓN AL ENDPOINT DE TRANSACCIONES
# ------------------------------------------------------------------------------
url = "https://api.iatistandard.org/datastore/transaction/select"

# Búsqueda únicamente por 'recipient_country_code:UR'
query = "recipient_country_code:UY"

params = {
    "q": query,
    "rows": 50,           # Trae hasta 50 transacciones para esta prueba
    "wt": "json",         # Formato JSON
    "fl": "*"             # Todos los campos disponibles
}

headers = {
    "Ocp-Apim-Subscription-Key": api_key
}

# ------------------------------------------------------------------------------
# REALIZAMOS LA SOLICITUD A LA API
# ------------------------------------------------------------------------------
response = requests.get(url, params=params, headers=headers)

st.write(f"**Query enviado**: `{query}`")
st.write("**Status code**:", response.status_code)

if response.status_code != 200:
    st.error(f"Ocurrió un error al consultar la API. "
             f"Código de estado: {response.status_code}\n"
             f"Texto de respuesta: {response.text}")
    st.stop()

# ------------------------------------------------------------------------------
# PROCESAMOS LA RESPUESTA
# ------------------------------------------------------------------------------
data = response.json()
docs = data.get("response", {}).get("docs", [])

st.write(f"**Documentos obtenidos**: {len(docs)}")

# Si no hay resultados, avisamos
if not docs:
    st.warning("No se encontraron transacciones con recipient_country_code:UR")
    st.stop()

# Convertimos a DataFrame
df = pd.DataFrame(docs)

# ------------------------------------------------------------------------------
# VISUALIZACIÓN DE RESULTADOS
# ------------------------------------------------------------------------------
st.subheader("Transacciones encontradas")
st.dataframe(df)

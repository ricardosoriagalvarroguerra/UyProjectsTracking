import streamlit as st
import requests
import pandas as pd

# ------------------------------------------------------------------------------
# CONFIGURACIÓN DE STREAMLIT
# ------------------------------------------------------------------------------
st.set_page_config(page_title="Prueba de Conexión con IATI", layout="wide")
st.title("Prueba - Transacciones con reporting_org_ref: XI-IATI-IADB")

# ------------------------------------------------------------------------------
# CLAVE DE SUSCRIPCIÓN (API Key)
# ------------------------------------------------------------------------------
api_key = "3ed3705bd91943b7ad8583f88836ea51"  # Ajusta aquí tu clave real
if not api_key:
    st.error("No se ha proporcionado la API Key de IATI.")
    st.stop()

# ------------------------------------------------------------------------------
# ENDPOINT DE TRANSACCIONES Y PARÁMETROS
# ------------------------------------------------------------------------------
url = "https://api.iatistandard.org/datastore/transaction/select"

# Búsqueda para filtrar por reporting_org_ref:XI-IATI-IADB
query = 'reporting_org_ref:"XI-IATI-IADB"'  # Notar las comillas para coincidencia literal

params = {
    "q": query,
    "rows": 50,        # Máximo de 50 resultados en esta demo
    "wt": "json",      # Formato JSON
    "fl": "*"          # Todos los campos disponibles
}

headers = {
    "Ocp-Apim-Subscription-Key": api_key
}

# Mostramos información básica
st.write(f"**Query enviado**: `{query}`")

# ------------------------------------------------------------------------------
# REALIZAMOS LA SOLICITUD A LA API
# ------------------------------------------------------------------------------
response = requests.get(url, params=params, headers=headers)

st.write("**Status code**:", response.status_code)

if response.status_code != 200:
    st.error(f"Error al consultar la API (código {response.status_code}).\n"
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
    st.warning("No se encontraron transacciones con reporting_org_ref: XI-IATI-IADB.")
    st.stop()

# Convertimos a DataFrame para mostrar
df = pd.DataFrame(docs)

st.subheader("Transacciones encontradas")
st.dataframe(df)

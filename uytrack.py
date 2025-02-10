import streamlit as st
import requests
import pandas as pd

# ------------------------------------------------------------------------------
# CONFIGURACIÓN INICIAL DE STREAMLIT
# ------------------------------------------------------------------------------
st.set_page_config(page_title="Monitoreo de préstamos Uruguay - IATI", layout="wide")
st.title("Monitoreo de préstamos Uruguay - Fuentes Multilaterales (IATI)")

st.write("""
Este panel obtiene datos de **transacciones** registradas en IATI que 
cumplen con:
- País receptor: Uruguay (`UY`)
- Tipo de financiamiento: préstamos (códigos `4xx`)
- Organización reportante: Multilateral (`reporting_org_type_code=40`)
""")

# ------------------------------------------------------------------------------
# CLAVE DE SUSCRIPCIÓN (API Key) - Aquí se coloca explícitamente
# ------------------------------------------------------------------------------
api_key = "3ed3705bd91943b7ad8583f88836ea51"
if not api_key:
    st.error("Se requiere una API Key de IATI para continuar.")
    st.stop()

# ------------------------------------------------------------------------------
# PARÁMETROS DE BÚSQUEDA
# ------------------------------------------------------------------------------
url = "https://api.iatistandard.org/datastore/transaction/select"

# Construimos la query con AND:
#  - recipient_country_code:UY
#  - finance_type_code:4* (préstamos)
#  - reporting_org_type_code:40 (multilateral)
query = "recipient_country_code:UY AND finance_type_code:4* AND reporting_org_type_code:40"

params = {
    "q": query,
    "rows": 100,       # Máximo de 100 resultados en esta demostración
    "wt": "json",      # Formato JSON
    "fl": "*"          # Todos los campos disponibles
}

headers = {
    "Ocp-Apim-Subscription-Key": api_key
}

st.write(f"**Consulta a la API de IATI:** `{query}`")

# ------------------------------------------------------------------------------
# OBTENEMOS LOS DATOS DE LA API
# ------------------------------------------------------------------------------
response = requests.get(url, params=params, headers=headers)
if response.status_code != 200:
    st.error(f"Error en la solicitud (código {response.status_code}). Revisa la API Key o los parámetros.")
    st.stop()

data = response.json()
docs = data.get("response", {}).get("docs", [])

st.write(f"**Transacciones encontradas:** {len(docs)}")

if not docs:
    st.info("No se encontraron transacciones que coincidan con los filtros.")
    st.stop()

# ------------------------------------------------------------------------------
# MOSTRAMOS LA TABLA DE RESULTADOS
# ------------------------------------------------------------------------------
df = pd.DataFrame(docs)
st.subheader("Tabla de transacciones")
st.dataframe(df)

# ------------------------------------------------------------------------------
# EJEMPLO DE ANÁLISIS: SUMA DE MONTOS POR AÑO
# ------------------------------------------------------------------------------
st.subheader("Resumen de montos por año")

if "transaction_date" in df.columns:
    # Convertimos transaction_date a datetime
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df["year"] = df["transaction_date"].dt.year

    if "transaction_value" in df.columns:
        # Convertimos transaction_value a numérico
        df["transaction_value"] = pd.to_numeric(df["transaction_value"], errors="coerce")

        summary = df.groupby("year")["transaction_value"].sum().reset_index()
        summary.rename(columns={"transaction_value": "Monto total (suma)"}, inplace=True)

        st.write("**Suma de montos por año de transacción**")
        st.dataframe(summary)

        # Gráfico de barras
        st.bar_chart(data=summary, x="year", y="Monto total (suma)")
    else:
        st.info("No existe la columna 'transaction_value' en estos datos para agrupar por año.")
else:
    st.info("No existe la columna 'transaction_date' en estos datos para agrupar por año.")

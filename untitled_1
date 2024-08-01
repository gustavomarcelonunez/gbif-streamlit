import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title("Explorador de Datos de GBIF")

country = st.text_input("Código del país (ej. ES)")
limit = st.number_input("Límite de registros", value=100)

if st.button("Buscar"):
    url = "https://api.gbif.org/v1/occurrence/search"
    params = {
        "country": country,
        "limit": limit
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data['results'])

        st.subheader("Mapa de Distribución de Especies")
        fig = px.scatter_geo(df,
                             lat='decimalLatitude',
                             lon='decimalLongitude',
                             hover_name='species',
                             title='Distribución de Especies (GBIF)')
        st.plotly_chart(fig)

        st.subheader("Datos de Especies")
        st.write(df.head(10))  # Mostrar hasta 10 filas
    else:
        st.error("Error en la solicitud")


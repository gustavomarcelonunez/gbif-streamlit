import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Título de la aplicación
st.title("Explorador de Datos de GBIF")

# Entradas para los parámetros de búsqueda
st.sidebar.header("Parámetros de Búsqueda")
country = st.sidebar.text_input("Código del país (ej. ES)")
limit = st.sidebar.number_input("Límite de registros", value=100)
year_range = st.sidebar.slider("Rango de Años", 1900, 2023, (2000, 2023))
#taxon_key = st.sidebar.text_input("Taxón (ID del taxón)")

# Botón para ejecutar la búsqueda
if st.sidebar.button("Buscar"):
    url = "https://api.gbif.org/v1/occurrence/search"
    params = {
        "country": country,
        "limit": limit,
        "year": ",".join(map(str, range(year_range[0], year_range[1] + 1))),
        #"taxonKey": taxon_key
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            df = pd.json_normalize(data['results'])

            st.header("Mapa de Distribución de Especies")
            fig = px.scatter_geo(df,
                                 lat='decimalLatitude',
                                 lon='decimalLongitude',
                                 hover_name='species',
                                 title='Distribución de Especies (GBIF)')
            st.plotly_chart(fig)

            st.header("Datos de Especies")
            st.write(df.head(10))  # Mostrar hasta 10 filas

            st.header("Estadísticas de Ocurrencias")
            st.write(df.describe())
        else:
            st.error("No se encontraron datos para los parámetros seleccionados.")
    else:
        st.error("Error en la solicitud")

# Opción para descargar los datos
if st.sidebar.button("Descargar Datos"):
    if 'df' in locals():
        st.sidebar.download_button(
            label="Descargar CSV",
            data=df.to_csv().encode('utf-8'),
            file_name='datos_gbif.csv',
            mime='text/csv'
        )
    else:
        st.sidebar.warning("Primero realiza una búsqueda para descargar los datos.")

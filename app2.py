import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuración de la página (debe ser la primera llamada de Streamlit en el script)
st.set_page_config(page_title="Explorador de Datos de GBIF", page_icon="🌍", layout="wide")

# Estilos personalizados
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
            color: black;
        }
        .sidebar .sidebar-content h2 {
            color: #003366;
        }
        .stButton>button {
            background-color: #003366;
            color: white;
        }
        .stButton>button:hover {
            background-color: #0055a5;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# Título de la aplicación
st.title("🌍 Explorador de Datos de GBIF")


# Función para obtener la lista de especies desde la API de GBIF
def obtener_especies():
    url = "https://api.gbif.org/v1/species/search"
    params = {"limit": 1000}  # Limitar a 1000 especies para la demo
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        especies = [item['scientificName'] for item in data['results']]
        return especies
    else:
        st.error("Error al obtener la lista de especies")
        return []


# Obtener la lista de especies para el menú desplegable
especies = obtener_especies()

# Entradas para los parámetros de búsqueda en la barra lateral
st.sidebar.header("Parámetros de Búsqueda")
country = st.sidebar.text_input("Código del país (ej. ES)")
species = st.sidebar.selectbox("Especie", options=especies)
limit = st.sidebar.number_input("Límite de registros", value=100, min_value=1, max_value=10000)
year_range = st.sidebar.slider("Rango de Años", 1900, 2023, (2000, 2023))

# Botón para ejecutar la búsqueda
if st.sidebar.button("Buscar"):
    url = "https://api.gbif.org/v1/occurrence/search"
    params = {
        "country": country,
        "limit": limit,
        "scientificName": species,
        "year": f"{year_range[0]},{year_range[1]}"  # Usar un rango de años
    }
    response = requests.get(url, params=params)

    st.write(f"Solicitando datos a: {url}")
    st.write(f"Con los parámetros: {params}")

    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            df = pd.json_normalize(data['results'])

            st.header("Mapa de Distribución de Especies")
            # Usar una columna válida en el parámetro 'hover_name'
            fig = px.scatter_geo(df,
                                 lat='decimalLatitude',
                                 lon='decimalLongitude',
                                 hover_name='scientificName',  # Columna válida
                                 title='Distribución de Especies (GBIF)')
            st.plotly_chart(fig, use_container_width=True)

            st.header("Datos de Especies")
            st.write(df.head(10))  # Mostrar hasta 10 filas

            st.header("Estadísticas de Ocurrencias")
            st.write(df.describe())

            # Graficar estadísticas de ocurrencias
            st.header("Gráficos de Estadísticas de Ocurrencias")

            # Histograma del número de ocurrencias por año
            fig_year = px.histogram(df, x='year', title='Número de Ocurrencias por Año')
            st.plotly_chart(fig_year, use_container_width=True)

            # Histograma del número de ocurrencias por tipo de registro
            fig_basis = px.histogram(df, x='basisOfRecord', title='Número de Ocurrencias por Tipo de Registro')
            st.plotly_chart(fig_basis, use_container_width=True)

            # Histograma del número de ocurrencias por país
            fig_country = px.histogram(df, x='country', title='Número de Ocurrencias por País')
            st.plotly_chart(fig_country, use_container_width=True)

        else:
            st.error("No se encontraron datos para los parámetros seleccionados.")
    else:
        st.error(f"Error en la solicitud: {response.status_code} - {response.text}")

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

# Footer
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        Explorador de Datos de GBIF | Desarrollado por [Tu Nombre]
    </div>
    """, unsafe_allow_html=True)

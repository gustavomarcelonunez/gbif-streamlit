import streamlit as st
import requests
import pandas as pd

from utils import get_openai_response

# Configuración de la página
st.set_page_config(page_title="Explorador de Datasets de GBIF", page_icon="🌍", layout="wide")

# Título de la aplicación
st.title("🧉 Explorador de Datasets de GBIF")

@st.cache
def obtener_paises():
    url = 'https://raw.githubusercontent.com/gustavomarcelonunez/gbif-url/main/countries.csv'
    countries_df = pd.read_csv(url)
    country_codes = countries_df['code'].tolist()
    return country_codes

@st.cache
def buscar_datos(country, text_field, limit, year_range):
    url = "https://api.gbif.org/v1/dataset"
    params = {
        "country": country,
        "limit": limit,
        "q": text_field,
        "type": "OCCURRENCE"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            return data['results']
        else:
            st.error("No se encontraron datos para los parámetros seleccionados.")
            return None
    else:
        st.error(f"Error en la solicitud: {response.status_code} - {response.text}")
        return None

def obtener_ocurrencias(dataset_key):
    url = "https://api.gbif.org/v1/occurrence/search"
    params = {"datasetKey": dataset_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            st.session_state.df = pd.json_normalize(data['results'])
            st.session_state.show_chat = True
        else:
            st.error("No se encontraron datos para los parámetros seleccionados.")
    else:
        st.error(f"Error en la solicitud: {response.status_code} - {response.text}")

# Inicializar st.session_state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False

# Entradas para los parámetros de búsqueda en la barra lateral
paises = obtener_paises()
st.sidebar.header("Parámetros de Búsqueda")
country = st.sidebar.selectbox("Código del país", options=paises)
text_field = st.sidebar.text_input("Texto de búsqueda")
limit = st.sidebar.number_input("Límite de registros", value=50, min_value=1, max_value=10000)
year_range = st.sidebar.slider("Rango de Años", 1900, 2023, (2000, 2023))

# Botón para ejecutar la búsqueda
if st.sidebar.button("Buscar"):
    results = buscar_datos(country, text_field, limit, year_range)
    if results:
        st.session_state.df = pd.json_normalize(results)
        st.session_state.show_chat = False

if st.session_state.df is not None and not st.session_state.show_chat:
    st.header("Datasets recuperados")
    for idx, row in st.session_state.df.iterrows():
        st.write(f"**{row['title']}**")
        st.write(f"Ocurrencias: {row['numConstituents']}")
        st.write(f"Dataset Key: {row['key']}")  # Imprime el valor de la clave

        if st.button("Consultar datos", key=row['key']):
            obtener_ocurrencias(row['key'])

# Selector de página
st.sidebar.markdown("---")
page = st.sidebar.selectbox("Selecciona una vista", ["Explorador de Datos", "Chat"])

# Mostrar la vista adecuada
if page == "Chat" or st.session_state.show_chat:
    st.header("Chat con LLM")

    if st.session_state.df is None:
        st.error("Realice primero una búsqueda.")
    else:
        question = st.text_input("Escribe tu pregunta aquí:")

        if question and st.button("Enviar"):
            # Obtener la respuesta del modelo OpenAI
            answer = get_openai_response(question, st.session_state.df)
            # Mostrar la respuesta del LLM
            st.write(f"Tu pregunta: {question}")
            st.write(answer)

# Footer
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        Explorador de Datos de GBIF | Desarrollado por [Tu Nombre]
    </div>
    """, unsafe_allow_html=True)

import openai
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json
import os

# Configuración de la API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Función para hacer la consulta a OpenAI
def get_openai_response(question, json_data):
    try:
        # Define el contexto del mensaje
        chat_history = [
            {"role": "system", "content": "Eres un bot útil, siempre respondes en español."},
            {"role": "system", "content": "Tienes un archivo JSON con el siguiente contenido: "},
            {"role": "system", "content": f"{json.dumps(json_data)[:3000]}"}  # Limita la longitud del JSON para evitar errores
        ]
        chat_history.append({"role": "user", "content": question})

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=chat_history,
            temperature=0,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        return response.choices[0].message['content'].strip()

    except Exception as e:
        st.error(f"Error al llamar a la API de OpenAI: {e}")
        return "Error en la consulta."

# Configuración de la página
st.set_page_config(page_title="Explorador de Datos de GBIF", page_icon="🌍", layout="wide")

# Título de la aplicación
st.title("🌍 Explorador de Datos de GBIF")

@st.cache
def obtener_paises():
    url = 'https://raw.githubusercontent.com/gustavomarcelonunez/gbif-url/main/countries.csv'
    countries_df = pd.read_csv(url)
    country_codes = countries_df['code'].tolist()
    return country_codes

@st.cache
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

@st.cache
def buscar_datos(country, species, limit, year_range):
    url = "https://api.gbif.org/v1/occurrence/search"
    params = {
        "country": country,
        "limit": limit,
        "scientificName": species,
        "year": f"{year_range[0]},{year_range[1]}"  # Usar un rango de años
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

# Entradas para los parámetros de búsqueda en la barra lateral
paises = obtener_paises()
especies = obtener_especies()

st.sidebar.header("Parámetros de Búsqueda")
country = st.sidebar.selectbox("Código del país", options=paises)
species = st.sidebar.selectbox("Especie", options=especies)
limit = st.sidebar.number_input("Límite de registros", value=100, min_value=1, max_value=10000)
year_range = st.sidebar.slider("Rango de Años", 1900, 2023, (2000, 2023))

# Botón para ejecutar la búsqueda
if st.sidebar.button("Buscar"):
    results = buscar_datos(country, species, limit, year_range)
    if results:
        df = pd.json_normalize(results)
        st.session_state.df = df

        # Guardar los datos en un archivo JSON
        with open('datos_gbif.json', 'w') as f:
            json.dump(results, f)

        st.header("Mapa de Distribución de Especies")
        fig = px.scatter_geo(df,
                             lat='decimalLatitude',
                             lon='decimalLongitude',
                             hover_name='scientificName',
                             title='Distribución de Especies (GBIF)')
        st.plotly_chart(fig, use_container_width=True)

        st.header("Datos de Especies")
        st.write(df.head(10))

        st.header("Estadísticas de Ocurrencias")
        st.write(df.describe())

        st.header("Gráficos de Estadísticas de Ocurrencias")
        fig_year = px.histogram(df, x='year', title='Número de Ocurrencias por Año')
        st.plotly_chart(fig_year, use_container_width=True)

        fig_basis = px.histogram(df, x='basisOfRecord', title='Número de Ocurrencias por Tipo de Registro')
        st.plotly_chart(fig_basis, use_container_width=True)

        fig_country = px.histogram(df, x='country', title='Número de Ocurrencias por País')
        st.plotly_chart(fig_country, use_container_width=True)

        st.sidebar.download_button(
            label="Descargar Datos",
            data=df.to_csv().encode('utf-8'),
            file_name='datos_gbif.csv',
            mime='text/csv'
        )

# Selector de página
st.sidebar.markdown("---")
page = st.sidebar.selectbox("Selecciona una vista", ["Explorador de Datos", "Chat"])

# Mostrar la vista adecuada
if page == "Chat":
    st.header("Chat con LLM")

    if "df" not in st.session_state:
        st.error("Realice primero una búsqueda.")
    else:
        question = st.text_input("Escribe tu pregunta aquí:")

        if question and st.button("Enviar"):
            # Cargar los datos del JSON almacenado en session_state
            if "json_data" not in st.session_state:
                with open('datos_gbif.json', 'r') as f:
                    st.session_state.json_data = json.load(f)

            json_data = st.session_state.json_data
            
            # Obtener la respuesta del modelo OpenAI
            answer = get_openai_response(question, json_data)
            
            # Mostrar la respuesta del LLM
            st.write(f"Tu pregunta: {question}")
            st.write(answer)

# Footer
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        Explorador de Datos de GBIF | Desarrollado por [Tu Nombre]
    </div>
    """, unsafe_allow_html=True)

import streamlit as st
import requests

import json

from utils_open_ai import get_openai_response
from utils_gbif import search_data
from utils_gbif import get_countries

# Configuración de la página
st.set_page_config(page_title="GBIF Data explorer", page_icon="🌍", layout="wide")

# Título de la aplicación
import streamlit as st

st.title("GBIF EcoQuery Bot: A tool for dynamic interaction with GBIF biodiversity data. 🧉")

st.header("Ask to EcoQuery Bot")
st.write("To inquire about datasets, perform a search first and then consult. To ask about a specific dataset, select one from the results and consult here.")


if "json" not in st.session_state:
    st.session_state.json = None

with st.form(key='my_form'):
    question = st.text_input("Ask here:")
    
    submit_button = st.form_submit_button(label="Send")

if submit_button and question:
    # Obtener la respuesta del modelo OpenAI
    answer = get_openai_response(question, st.session_state.json)
    # Mostrar la respuesta del LLM
    st.write(f"Your question: {question}")
    st.write(f"Answer: {answer}")

def get_occurrences(dataset_key):

    url = "https://api.gbif.org/v1/occurrence/search"
    params = {"datasetKey": dataset_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            with open('ocurrencias.json', 'w') as f:
                json.dump(data, f, indent=4)  # Guardar con indentación para mejor legibilidad
            st.session_state.json = data
            st.success("You can now chat with the dataset information!")

        else:
            st.error("No data was found for the selected parameters.")
    else:
        st.error(f"Request error: {response.status_code} - {response.text}")


# Inicializar st.session_state
if 'json' not in st.session_state:
    st.session_state.json = None

# Entradas para los parámetros de búsqueda en la barra lateral
paises = get_countries()
st.sidebar.header("Search parameters")
country = st.sidebar.selectbox("Country code", options=paises)
text_field = st.sidebar.text_input("Search text")

# Botón para ejecutar la búsqueda
if st.sidebar.button("Search"):
    results = search_data(country, text_field)
    if results:
        st.session_state.json = results
        with open("datasets.json", 'w') as f:
            json.dump(results, f, indent=4)

if st.session_state.json is not None:
    st.header("Recovered Datasets")
    st.write("Showing maximum 9 results...")

    with open('datasets.json', 'r') as f:
        datasets = json.load(f)   

    for idx, row in enumerate(datasets):
        if idx % 3 == 0:  # Crear una nueva fila cada 3 elementos
            cols = st.columns(3)
        
        with cols[idx % 3]:
            st.write(f"**Title: {row['title']}**")
            st.markdown(f"[DOI: {row['doi']}](https://doi.org/{row['doi']})")
            
            if st.button("🤖 Ask about this occurrences", key=row['key']):
                get_occurrences(row['key'])

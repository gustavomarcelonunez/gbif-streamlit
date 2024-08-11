import streamlit as st
from datetime import datetime

import json

from utils_open_ai import get_openai_response
from utils_gbif import get_countries
from utils_gbif import get_dataset_types
from utils_gbif import search_data
from utils_gbif import get_occurrences
from disclaimer_popup import show_disclaimer_popup

# Configuración de la página
st.set_page_config(page_title="GBIF Data explorer", page_icon="🌍", layout="wide")

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

# Inicializar st.session_state
if 'json' not in st.session_state:
    st.session_state.json = None

# Entradas para los parámetros de búsqueda en la barra lateral
st.sidebar.header("Search parameters")
country = st.sidebar.selectbox("Country code", options=get_countries())
dataset_type = st.sidebar.selectbox("Dataset type", options=get_dataset_types())
text_field = st.sidebar.text_input("Search text")

# Botón para ejecutar la búsqueda
if st.sidebar.button("Search"):
    results = search_data(country, text_field, dataset_type)
    if results:
        st.session_state.json = results
        with open("datasets.json", 'w') as f:
            json.dump(results, f, indent=4)

if st.sidebar.button('Disclaimer'):
        show_disclaimer_popup()


if st.session_state.json is not None:
    st.header("Recovered Datasets")
    st.write("Showing maximum 9 results...")

    with open('datasets.json', 'r') as f:
        datasets = json.load(f)   

    for idx, row in enumerate(datasets):
        if idx % 3 == 0:  # Crear una nueva fila cada 3 elementos
            if idx != 0:
                st.markdown("<hr>", unsafe_allow_html=True)  # Agrega una línea horizontal entre filas

            cols = st.columns(3)
        
        with cols[idx % 3]:
            created_date = datetime.fromisoformat(row['created']).strftime("%B %d, %Y at %I:%M %p")
            modified_date = datetime.fromisoformat(row['modified']).strftime("%B %d, %Y at %I:%M %p")


            st.write(f"**Title:** *{row['title']}*")
            st.write(f"**Created at:** {created_date}")
            st.write(f"**Last modified:** {modified_date}")

            st.markdown(f"[DOI: {row['doi']}](https://doi.org/{row['doi']})")
            
            if st.button("🤖 Ask about this data", key=row['key']):
                get_occurrences(row['key'])

import streamlit as st
from datetime import datetime
import json
from utils_open_ai import get_openai_response
from utils_gbif import get_countries, get_dataset_types, search_data, get_occurrences
from disclaimer_popup import show_disclaimer_popup

# Configuración de la página
st.set_page_config(page_title="BotGBIF", page_icon="🧉", layout="wide")

st.title("BotGBIF: A tool to query GBIF data in natural language. 🧉")
st.header("Ask to BotGBIF")
st.write("To ask about datasets, perform a search first and then consult. To ask about a specific dataset, select one from the results and chat! 😎")

# Inicializa el estado
if "json" not in st.session_state:
    st.session_state.json = None

# Entradas para los parámetros de búsqueda en la barra lateral
st.sidebar.header("Search parameters")

country_dict = get_countries()
country_name = st.sidebar.selectbox("Country", options=list(country_dict.keys()))
dataset_type = st.sidebar.selectbox("Dataset type", options=get_dataset_types())
text_field = st.sidebar.text_input("Full text search (simple word or a phrase, wildcards are not supported)")

# Botón para ejecutar la búsqueda
if st.sidebar.button("Search"):
    results = search_data(country_dict[country_name], text_field, dataset_type)
    if results:
        st.session_state.selected_dataset_title = None

        st.session_state.json = results
        with open("datasets.json", 'w') as f:
            json.dump(results, f, indent=4)
        st.session_state.prompt_msg = "Ask about recovered Datasets Metadata"
    else:
        st.session_state.json = None

if st.sidebar.button('Disclaimer'):
    show_disclaimer_popup()

st.sidebar.button("Watch demo")

if st.session_state.json:
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
                st.session_state.selected_dataset_title = row['title']
                st.session_state.prompt_msg = f"Ask about selected Dataset: *{row['title']}*"
                # También puedes cargar los datos del dataset seleccionado
                get_occurrences(row['key'])
                st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(st.session_state.prompt_msg)

            

# Muestra el prompt con el mensaje adecuado
question = st.chat_input("Ask here:")

if question:
    # Obtener la respuesta del modelo OpenAI
    answer = get_openai_response(question, st.session_state.json)
    # Mostrar la respuesta del LLM
    st.write(f"Your question: {question}")
    st.write(f"Answer: {answer}")

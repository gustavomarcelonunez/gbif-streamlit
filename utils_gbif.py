import streamlit as st
import pandas as pd
import requests
import json

@st.cache_resource
def get_countries():
    url = 'https://raw.githubusercontent.com/gustavomarcelonunez/gbif-url/main/countries.csv'
    countries_df = pd.read_csv(url)
    country_codes = countries_df['code'].tolist()
    return country_codes

def get_dataset_types():
    return ["OCCURRENCE", "CHECKLIST", "METADATA", "SAMPLING_EVENT", "MATERIAL_ENTITY"]

def search_data(country, text_field, dataset_type):
    url = "https://api.gbif.org/v1/dataset"
    params = {
        "country": country,
        "limit": 9,
        "q": text_field,
        "type": dataset_type
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            return data['results']
        else:
            st.error("No data was found for the selected parameters.")
            return None
    else:
        st.error(f"Request error: {response.status_code} - {response.text}")
        return None
    
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
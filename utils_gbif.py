import streamlit as st
import pandas as pd
import requests
import json

@st.cache_resource
def get_countries():
    url = 'https://raw.githubusercontent.com/gustavomarcelonunez/gbif-url/main/countries.csv'
    countries_df = pd.read_csv(url)
    
    # Diccionario para almacenar nombre del país, código y el emoji
    country_dict = {}
    
    for index, row in countries_df.iterrows():
        country_name = row['country']
        country_code = row['code']
        # Convertir el código de país a la bandera usando emojis
        flag_emoji = row['icon']
        # Almacenar en el diccionario
        country_dict[f"{flag_emoji} - {country_name}"] = country_code
    
    return country_dict

def get_dataset_types():
    return ["OCCURRENCE", "CHECKLIST", "METADATA", "SAMPLING_EVENT", "MATERIAL_ENTITY"]

def search_data(country, text_field, dataset_type):
    url = "https://api.gbif.org/v1/dataset"
    params = {
        "country": country,
        "limit": 15,
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
    elif response.status_code == 500:
        st.error(f"Request error: {response.status_code} - GBIF Internal Server Error")
        return None
    else:
        st.error(f"Request error: {response.status_code} - {response.text}")
        return None
def get_occurrences(dataset_key):

    url = "https://api.gbif.org/v1/occurrence/search"
    params = {"datasetKey": dataset_key,
              "limit": 100}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            with open('ocurrencias.json', 'w') as f:
                json.dump(data, f, indent=4)  # Guardar con indentación para mejor legibilidad
            st.session_state.json = data
    else:
        st.error(f"Request error: {response.status_code} - {response.text}")
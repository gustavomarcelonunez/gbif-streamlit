import streamlit as st
import pandas as pd
import requests

def search_data(country, text_field):
    url = "https://api.gbif.org/v1/dataset"
    params = {
        "country": country,
        "limit": 10,
        "q": text_field,
        "type": "OCCURRENCE"
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
    
@st.cache(suppress_st_warning=True)
def get_countries():
    url = 'https://raw.githubusercontent.com/gustavomarcelonunez/gbif-url/main/countries.csv'
    countries_df = pd.read_csv(url)
    country_codes = countries_df['code'].tolist()
    return country_codes
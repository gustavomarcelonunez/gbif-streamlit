import streamlit as st


@st.dialog("Disclaimer")
def show_disclaimer_popup():

    st.write("This chat application, 🤖 GBIF EcoQuery, was developed for the GBIF Ebbe Nielsen Challenge 2024 and is non-commercial in nature. It uses data retrieved from the GBIF REST API, limited to 9 datasets and the first 20 occurrences per dataset, due to processing constraints of the utilized Large Language Model (LLM). Please note that while we strive for accuracy, the use of LLMs may result in occasional inaccuracies or incomplete information. Users are encouraged to verify critical information independently.")
    if st.button("Close"):
         st.rerun()

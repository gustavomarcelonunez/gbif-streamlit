import streamlit as st

def show_disclaimer():
    st.markdown("### Disclaimer")
    st.write(
        """
        This chat application, 🤖 GBIF EcoQuery Bot, was developed for the GBIF Ebbe Nielsen Challenge 2024 and is non-commercial in nature.
        
        It uses data retrieved from the GBIF REST API, limited to 9 datasets and the first 20 occurrences per dataset, due to processing constraints of the utilized Large Language Model (LLM).
        
        Please note that while we strive for accuracy, the use of LLMs may result in occasional inaccuracies or incomplete information. Users are encouraged to verify critical information independently.
        """
    )

def show_disclaimer_sidebar():
    if 'show_disclaimer' not in st.session_state:
        st.session_state.show_disclaimer = False

    with st.sidebar:
        if st.button("Disclaimer"):
            st.session_state.show_disclaimer = True

    if st.session_state.show_disclaimer:
        show_disclaimer()
        if st.button("Close Disclaimer"):
            st.session_state.show_disclaimer = False
            st.experimental_rerun()  # Fuerza la actualización de la página

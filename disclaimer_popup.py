import streamlit as st

@st.dialog("Disclaimer")
def show_disclaimer_popup():

    st.write(
        """
        This chat application, 🤖 BotGBIF, was developed for the [GBIF Ebbe Nielsen Challenge 2024](https://www.gbif.org/es/ebbe) and is non-commercial in nature. It uses data retrieved from the [GBIF REST API](https://techdocs.gbif.org/en/openapi/), limited to 15 datasets and the first 100 occurrences per dataset, due to processing constraints of the utilized Large Language Model [(LLM)](https://platform.openai.com/docs/guides/rate-limits). Please note that while we strive for accuracy, the use of LLMs may result in occasional inaccuracies or incomplete information. Users are encouraged to verify critical information independently. Repository readme [here](https://github.com/gustavomarcelonunez/gbif-streamlit/blob/main/README.md).
        """
    )
    if st.button("Close"):
         st.rerun()
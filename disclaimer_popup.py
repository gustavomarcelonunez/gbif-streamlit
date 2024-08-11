import streamlit as st

# Función para mostrar el mensaje de advertencia
def show_disclaimer_popup():
    popup_html = """
    <div id="popup" style="display:block; position:fixed; top:0; left:0; width:100%; height:100%; background-color:rgba(0, 0, 0, 0.8); z-index:9999;">
        <div style="position:relative; width:60%; margin:10% auto; padding:20px; background:white; border-radius:10px; text-align:center;">
            <h2>Disclaimer</h2>
            <p>This chat application, 🤖 GBIF EcoQuery Bot, was developed for the GBIF Ebbe Nielsen Challenge 2024 and is non-commercial in nature. It uses data retrieved from the GBIF REST API, limited to 9 datasets and the first 20 occurrences per dataset, due to processing constraints of the utilized Large Language Model (LLM). Please note that while we strive for accuracy, the use of LLMs may result in occasional inaccuracies or incomplete information. Users are encouraged to verify critical information independently.</p>
            <button onclick="document.getElementById('popup').style.display='none';" style="padding:10px 20px; background-color:#007bff; color:white; border:none; border-radius:5px;">Close</button>
        </div>
    </div>
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        document.getElementById("popup").style.display = "block";
    });
    </script>
    """
    st.components.v1.html(popup_html, height=400)

# Llamada a la función para mostrar el popup
show_disclaimer_popup()

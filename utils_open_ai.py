from openai import OpenAI
import streamlit as st

# Cargar la API key desde el entorno
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
)

def get_openai_response(question, json):
    try:

        # Aclarar tema del archivo vacio de entrada
        chat_history = [
            {"role": "system", "content": "You are an assistant bot specialized in interpreting and providing information from a JSON file related to species and biodiversity data from the GBIF portal. Always respond in English. While your primary focus is on providing information related to this data, you are also able to assist with general tasks such as drafting emails or other related activities if requested by the user."},
            {"role": "system", "content": "You have access to a JSON file with the following content: "},
            {"role": "system", "content": f"{json}"},
            {"role": "system", "content": "If the JSON file is empty, respond by saying that a search must be performed first at sidebar."},
        ]

        if "selected_dataset_title" in st.session_state:
            chat_history.append({"role": "system", "content": f"The selected dataset title is: {st.session_state.selected_dataset_title}"})

        chat_history.append({"role": "user", "content": question})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history,
            temperature=0,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        return response.choices[0].message.content

    except Exception as e:
        st.error(f"Error al llamar a la API de OpenAI: {e}")
        return "Error en la consulta."
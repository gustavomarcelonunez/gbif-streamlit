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
            {"role": "system", "content": "You are an assistant bot specialized in interpreting and providing information from a JSON file related to species and biodiversity data from the GBIF portal. Your primary focus is on providing accurate and relevant information based on this data. Always respond in English."},
            {"role": "system", "content": "You have access to a JSON file with the following content: "},
            {"role": "system", "content": f"{json}"},
            {"role": "system", "content": "If the JSON file is empty, respond by informing the user that they must perform a search first using the sidebar before interacting with the chat, withount mentioning JSON file."},
            {"role": "system", "content": "If the JSON file is not empty, assume that any question the user asks is related to the data available in the json file, unless the user explicitly states otherwise. Respond based on the information from the JSON."},
            {"role": "system", "content": "If the user has already performed a search, in addiotion to responding, you can guide them by letting them know they can ask about the metadata of the retrieved datasets or select a specific dataset from the list to inquire further."},
            {"role": "system", "content": "If the user asks questions unrelated to species, biodiversity, or the GBIF data, politely inform them that your function is limited to assisting with biodiversity-related queries and tasks."},
            {"role": "system", "content": "You can also assist with related tasks, such as drafting emails to contacts found within the dataset, but you should not engage in tasks unrelated to the application."}
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
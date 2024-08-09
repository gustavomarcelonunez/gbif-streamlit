from openai import OpenAI
import streamlit as st

# Cargar la API key desde el entorno
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
)

def get_openai_response(question, df):
    try:
        json_data = df.to_json(orient='records')

        # Define el contexto del mensaje
        chat_history = [
            {"role": "system", "content": "Eres un bot útil, siempre respondes en español."},
            {"role": "system", "content": "Tienes un archivo JSON con el siguiente contenido: "},
            {"role": "system", "content": f"{json_data[:100000]}"}  # Limita la longitud del JSON para evitar errores
        ]
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
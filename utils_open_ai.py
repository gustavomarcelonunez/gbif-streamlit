from openai import OpenAI
import streamlit as st
import json

OCCURRENCE_FIELDS = [
    "key",
    "scientificName",
    "acceptedScientificName",
    "taxonRank",
    "eventDate",
    "year",
    "month",
    "decimalLatitude",
    "decimalLongitude",
    "country",
    "stateProvince",
    "locality",
    "basisOfRecord",
    "occurrenceStatus",
    "individualCount",
    "sex",
    "lifeStage",
    "recordedBy",
    "institutionCode",
    "collectionCode",
    "catalogNumber",
]

def compact_occurrences(data):
    if not isinstance(data, dict):
        return data

    results = data.get("results")

    if not isinstance(results, list):
        return data

    compact_results = [
        {
            field: record[field]
            for field in OCCURRENCE_FIELDS
            if field in record and record[field] is not None
        }
        for record in results
    ]

    return {
        "count": data.get("count"),
        "results": compact_results,
    }

# Cargar la API key desde el entorno
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
)









def get_openai_response(question, json):
    try:
        if not json:
            return "Hi 👋! You must perform a search first using the sidebar before interacting with the chat."

        # Reduce el tamaño de los datos antes de enviarlos al modelo
        compact_data = compact_occurrences(json)

        # Convertir los datos a JSON compacto
        json_content = __import__("json").dumps(
            compact_data,
            ensure_ascii=False,
            separators=(",", ":")
        )

        chat_history = [
            {
                "role": "system",
                "content": (
                    "You are an assistant bot specialized in interpreting "
                    "and providing information about species and biodiversity "
                    "data from the GBIF portal. Your primary focus is on "
                    "providing accurate and relevant information based on "
                    "the supplied data. Always respond in English."
                )
            },
            {
                "role": "system",
                "content": (
                    "You have access to the retrieved data shown below. "
                    "Base your answers on this data and do not invent "
                    "facts that are not supported by it."
                )
            },
            {
                "role": "system",
                "content": json_content
            },
            {
                "role": "system",
                "content": (
                    "Assume that questions are related to the available "
                    "GBIF data unless the user explicitly states otherwise. "
                    "If the data does not contain enough information to "
                    "answer, explain this limitation."
                )
            },
            {
                "role": "system",
                "content": (
                    "You can guide users to ask about dataset metadata "
                    "or select a specific dataset from the list. "
                    "Do not mention JSON."
                )
            },
            {
                "role": "system",
                "content": (
                    "If users ask about topics unrelated to species, "
                    "biodiversity, or GBIF data, politely explain that "
                    "the application is limited to biodiversity-related "
                    "queries and tasks."
                )
            },
            {
                "role": "system",
                "content": (
                    "You can also assist with related tasks, such as "
                    "drafting emails to contacts found in the dataset."
                )
            }
        ]

        if "selected_dataset_title" in st.session_state:
            chat_history.append({
                "role": "system",
                "content": (
                    "The selected dataset title is: "
                    f"{st.session_state.selected_dataset_title}"
                )
            })

        chat_history.append({
            "role": "user",
            "content": question
        })

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
import streamlit as st
import requests
from streamlit_estilos import aplicar_estilos, mostrar_pie_de_pagina

# Aplicar estilos visuales
aplicar_estilos()

# Título principal
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color:#00629b;'>University Explorer</h1>
        <p style='color:#00a9e0; font-size: 1.1em; margin-top: -10px;'>A Case Study in Retrieval-Augmented Generation with Knowledge Graphs</p>
    </div>
    <hr style='border: 2px solid #00629b; margin-top: 0.5rem; margin-bottom: 2rem;'>
""", unsafe_allow_html=True)


# Input del usuario
question = st.text_input("Write your question here:")

# Checkboxes de fuentes
st.markdown("Select additional data sources:")
use_wikidata = st.checkbox("Wikidata", value=True)
use_dbpedia = st.checkbox("DBpedia", value=True)

# Enviar petición
if st.button("Send"):
    if question:
        try:
            response = requests.post(
                "http://langchain-api:5000/ask_question",
                json={
                    "question": question,
                    "use_wikidata": use_wikidata,
                    "use_dbpedia": use_dbpedia
                }
            )
            if response.status_code == 200:
                respuesta = response.json()["answer"]
                source = response.json()["source"]
                # Mostrar respuesta estilizada con título azul
                # Mostrar respuesta estilizada con título azul
                st.markdown(f"<h3 style='color:#00629b;'>Answer:</h3>", unsafe_allow_html=True)

                # Mostrar respuesta estilizada
                if respuesta.startswith("⚠️"):
                    advertencia, contenido = respuesta.split("\n\n", 1)
                    st.warning(advertencia)
                    st.markdown(f"<div class='respuesta'>{contenido}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='respuesta'>{respuesta}</div>", unsafe_allow_html=True)

                # Mostrar fuente
                st.markdown(f"<p style='font-size: 0.9em; color: grey;'>Source: <strong>{source}</strong></p>", unsafe_allow_html=True)

            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"❌ API connection error: {str(e)}")
    else:
        st.warning("Please write a question before sending.")

mostrar_pie_de_pagina()
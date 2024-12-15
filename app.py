import streamlit as st
from pydantic import BaseModel, Field
import random
from database.retrieve_check_server import get_new_check_fact


# Paso 1: Ingreso de la consulta del usuario desde el sidebar
with st.sidebar:
    st.title("MPox Search News Engine")
    query = st.sidebar.text_input("Input your question about Mpox", "")

# Estilo para las tarjetas (cards)
card_style = """
    <style>
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        margin: 10px 0;
        border-radius: 10px;
        box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
    }
    .card h3 {
        margin: 0;
    }
    .card p {
        font-size: 14px;
        color: #333;
    }
    .score {
        font-weight: bold;
        color: #008000;
    }
    </style>
"""

if len(query)>5:
    # Paso 2: Mostrar resultados relacionados
    st.write(f"Results for the query: **{query}**")
    
    # Incluir el estilo para las tarjetas (cards)
    st.markdown(card_style, unsafe_allow_html=True)

    # Simulación de búsqueda de noticias relacionadas
    related_news = get_new_check_fact(query)

    print(related_news)

    # Paso 3: Verificar la veracidad de las noticias y mostrar cada resultado como una "card"
    for news in related_news:

        # Crear el contenido de cada tarjeta (card) usando HTML/CSS
        card_content = f"""
        <div class="card">
            <h3><a href="{news['url']}" target="_blank">{news['url']}</a></h3>
            <p><strong>Category: </strong> {news['label']}</p>
            <p><strong>Content: </strong> {news['abstract'][0:80]+"..."}</p>
            <p><strong>Fact Score: </strong> <span class="score">{news['score']}</span></p>
            <p><strong>Justitication: </strong> {news["justification"]}</p>
        </div>
        """
        # Mostrar cada "card" con su información
        st.markdown(card_content, unsafe_allow_html=True)


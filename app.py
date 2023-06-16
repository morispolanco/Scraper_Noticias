import streamlit as st
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup

# Función para extraer los artículos de las fuentes de noticias
def extract_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')
    return articles

# Función para analizar el sentimiento de un texto
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return 'Positivo'
    elif sentiment < 0:
        return 'Negativo'
    else:
        return 'Neutral'

# URL de las fuentes de noticias
xataka_url = 'https://www.xataka.com/'
gizmodo_url = 'https://es.gizmodo.com/'

# Obtener los artículos de Xataka
xataka_articles = extract_articles(xataka_url)

# Obtener los artículos de Gizmodo
gizmodo_articles = extract_articles(gizmodo_url)

# Configuración de la aplicación de Streamlit
st.title('Análisis de Sentimientos de Marcas de Tecnología')
search_query = st.text_input('Ingresa el nombre de un producto o una marca:')
st.subheader('Xataka')
for article in xataka_articles:
    title = article.find('h2').text.strip()
    content_element = article.find('p')
    if content_element:
        content = content_element.text.strip()
        if search_query.lower() in title.lower() or search_query.lower() in content.lower():
            sentiment = analyze_sentiment(content)
            st.write(f'Título: {title}')
            st.write(f'Contenido: {content}')
            st.write(f'Sentimiento: {sentiment}')
            st.write('---')

st.subheader('Gizmodo')
for article in gizmodo_articles:
    title = article.find('h2').text.strip()
    content_element = article.find('p')
    if content_element:
        content = content_element.text.strip()
        if search_query.lower() in title.lower() or search_query.lower() in content.lower():
            sentiment = analyze_sentiment(content)
            st.write(f'Título: {title}')
            st.write(f'Contenido: {content}')
            st.write(f'Sentimiento: {sentiment}')
            st.write('---')

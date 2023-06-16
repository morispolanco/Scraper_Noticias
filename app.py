import streamlit as st
from datetime import datetime, date
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt

# Función para extraer los artículos de una fuente de noticias
def extract_articles(source_url):
    response = requests.get(source_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')
    return articles

# Función para obtener la fecha de un artículo
def get_article_date(article):
    date_element = article.find('time')
    if date_element and date_element.has_attr('datetime'):
        date_string = date_element['datetime']
        article_date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        return article_date.date()
    return None

# Función para realizar el análisis de sentimientos
def analyze_sentiment(text):
    # Aquí iría tu lógica de análisis de sentimientos
    # Esta es solo una función de ejemplo
    return 'Positivo'

# URL de las fuentes de noticias
xataka_url = 'https://www.xataka.com/'
gizmodo_url = 'https://es.gizmodo.com/'
theverge_url = 'https://www.theverge.com/'
engadget_url = 'https://www.engadget.com/'
digitaltrends_url = 'https://www.digitaltrends.com/'

# Título y descripción de la aplicación
st.title('Análisis de Sentimientos de Marcas de Tecnología')
st.markdown('Esta aplicación analiza el sentimiento de las noticias relacionadas con marcas de tecnología.')

# Entradas de usuario en la columna izquierda
with st.sidebar:
    st.markdown('**Filtros**')
    search_query = st.text_input('Producto o Marca')
    start_date = st.date_input('Fecha de Inicio')
    end_date = st.date_input('Fecha de Fin')

    # Convertir las fechas de inicio y fin a objetos datetime
    start_date = datetime.combine(start_date, datetime.min.time())
    end_date = datetime.combine(end_date, datetime.max.time())

# Obtener los artículos de las fuentes de noticias
xataka_articles = extract_articles(xataka_url)
gizmodo_articles = extract_articles(gizmodo_url)
theverge_articles = extract_articles(theverge_url)
engadget_articles = extract_articles(engadget_url)
digitaltrends_articles = extract_articles(digitaltrends_url)

# Listas para almacenar los sentimientos
sentiments = []
labels = ['Positivo', 'Neutral', 'Negativo']
values = [0, 0, 0]

# Obtener sentimientos de los artículos de Xataka
for article in xataka_articles:
    title_element = article.find('h2')
    if title_element:
        title = title_element.text.strip()
        content_element = article.find('p')
        if content_element:
            content = content_element.text.strip()
            article_date = get_article_date(article)
            if article_date and start_date <= article_date <= end_date and (search_query.lower() in title.lower() or search_query.lower() in content.lower()):
                sentiment = analyze_sentiment(content)
                sentiments.append(sentiment)

# Obtener sentimientos de los artículos de Gizmodo
for article in gizmodo_articles:
    title_element = article.find('h2')
    if title_element:
        title = title_element.text.strip()
        content_element = article.find('p')
        if content_element:
            content = content_element.text.strip()
            article_date = get_article_date(article)
            if article_date and start_date <= article_date <= end_date and (search_query.lower() in title.lower() or search_query.lower() in content.lower()):
                sentiment = analyze_sentiment(content)
                sentiments.append(sentiment)

# Obtener sentimientos de los artículos de The Verge
for article in theverge_articles:
    title_element = article.find('h2')
    if title_element:
        title = title_element.text.strip()
        content_element = article.find('p')
        if content_element:
            content = content_element.text.strip()
            article_date = get_article_date(article)
            if article_date and start_date <= article_date <= end_date and (search_query.lower() in title.lower() or search_query.lower() in content.lower()):
                sentiment = analyze_sentiment(content)
                sentiments.append(sentiment)

# Obtener sentimientos de los artículos de Engadget
for article in engadget_articles:
    title_element = article.find('h2')
    if title_element:
        title = title_element.text.strip()
        content_element = article.find('p')
        if content_element:
            content = content_element.text.strip()
            article_date = get_article_date(article)
            if article_date and start_date <= article_date <= end_date and (search_query.lower() in title.lower() or search_query.lower() in content.lower()):
                sentiment = analyze_sentiment(content)
                sentiments.append(sentiment)

# Obtener sentimientos de los artículos de Digital Trends
for article in digitaltrends_articles:
    title_element = article.find('h2')
    if title_element:
        title = title_element.text.strip()
        content_element = article.find('p')
        if content_element:
            content = content_element.text.strip()
            article_date = get_article_date(article)
            if article_date and start_date <= article_date <= end_date and (search_query.lower() in title.lower() or search_query.lower() in content.lower()):
                sentiment = analyze_sentiment(content)
                sentiments.append(sentiment)

# Calcular la distribución de sentimientos
for sentiment in sentiments:
    if sentiment == 'Positivo':
        values[0] += 1
    elif sentiment == 'Neutral':
        values[1] += 1
    elif sentiment == 'Negativo':
        values[2] += 1

# Gráfico de pie de sentimientos
fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%')
ax.axis('equal')
st.pyplot(fig)

import streamlit as st
from datetime import date
from bs4 import BeautifulSoup
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# Función para extraer los artículos de una fuente de noticias
def extract_articles(source_url):
    response = requests.get(source_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')
    return articles

# Función para obtener la fecha actual
def get_current_date():
    return date.today()

# Función para analizar el sentimiento de un texto utilizando VADER
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    if compound_score >= 0.05:
        sentiment = 'Positivo'
    elif compound_score <= -0.05:
        sentiment = 'Negativo'
    else:
        sentiment = 'Neutral'
    return sentiment

# Obtener artículos de las fuentes de noticias
xataka_articles = extract_articles('https://www.xataka.com/')
gizmodo_articles = extract_articles('https://es.gizmodo.com/')

# Obtener fecha actual
current_date = get_current_date()

# Lista para almacenar los sentimientos
sentiments = []

# Análisis de sentimientos para los artículos de Xataka
for article in xataka_articles:
    title_element = article.find('h2')
    if title_element:
        title = title_element.text.strip()
        content_element = article.find('p')
        if content_element:
            content = content_element.text.strip()
            sentiment = analyze_sentiment(content)
            sentiments.append(sentiment)

# Análisis de sentimientos para los artículos de Gizmodo
for article in gizmodo_articles:
    title_element = article.find('h2')
    if title_element:
        title = title_element.text.strip()
        content_element = article.find('p')
        if content_element:
            content = content_element.text.strip()
            sentiment = analyze_sentiment(content)
            sentiments.append(sentiment)

# Calcular la distribución de sentimientos
values = [0, 0, 0]  # Positivo, Neutral, Negativo
labels = ['Positivo', 'Neutral', 'Negativo']

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

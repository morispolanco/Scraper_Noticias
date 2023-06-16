import streamlit as st
from datetime import date
from bs4 import BeautifulSoup
import requests
import torch
from transformers import BertTokenizer, BertForSequenceClassification
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

# Función para analizar el sentimiento de un texto utilizando BERT
def analyze_sentiment(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
    model = BertForSequenceClassification.from_pretrained('bert-base-multilingual-cased', num_labels=3)
    model.load_state_dict(torch.load('sentiment_model.pth', map_location=torch.device('cpu')))
    encoded_input = tokenizer.encode_plus(text, add_special_tokens=True, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        logits = model(encoded_input['input_ids'], token_type_ids=encoded_input['token_type_ids'])[0]
        probabilities = torch.softmax(logits, dim=1).tolist()[0]
    sentiment_labels = ['Positivo', 'Neutral', 'Negativo']
    sentiment_index = probabilities.index(max(probabilities))
    sentiment = sentiment_labels[sentiment_index]
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
st.pyplot

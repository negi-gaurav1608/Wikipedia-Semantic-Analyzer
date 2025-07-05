from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
from textblob import TextBlob
import nltk
from nltk.tokenize import sent_tokenize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import os
import re

nltk.download('punkt')

app = Flask(__name__)
CORS(app)

STATIC_FOLDER = os.path.join(app.root_path, 'static')
os.makedirs(STATIC_FOLDER, exist_ok=True)

def scrape_wikipedia(topic):
    topic = topic.strip().replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{topic}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    text = " ".join([p.text for p in paragraphs if len(p.text.strip()) > 30])
    return text

def clean_text(text):
    text = re.sub(r'\[[^\]]*\]', '', text)
    text = re.sub(r'\W+', ' ', text.lower())
    return text

def analyze_text(text):
    cleaned = clean_text(text)
    words = cleaned.split()
    word_count = len(words)
    polarity = TextBlob(cleaned).sentiment.polarity
    freq = Counter(words).most_common(10)

    # Word cloud
    wordcloud = WordCloud(width=800, height=400).generate(cleaned)
    wordcloud.to_file(os.path.join(STATIC_FOLDER, 'wordcloud.png'))

    # Bar chart
    labels, values = zip(*freq)
    plt.figure(figsize=(8, 4))
    plt.bar(labels, values)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(STATIC_FOLDER, 'bar_chart.png'))
    plt.close()

    return word_count, polarity, freq

def classify_sentences(text):
    sentences = sent_tokenize(text)
    result = []
    for sent in sentences:
        polarity = TextBlob(sent).sentiment.polarity
        if polarity > 0.2:
            label = "Positive"
        elif polarity < -0.2:
            label = "Negative"
        else:
            label = "Neutral"
        result.append((sent, label))
    return result

@app.route("/analyze", methods=["POST"])
def analyze():
    topic = request.json.get("topic", "")
    text = scrape_wikipedia(topic)
    word_count, polarity, _ = analyze_text(text)
    classified = classify_sentences(text)

    return jsonify({
        "word_count": word_count,
        "polarity": polarity,
        "positive_sentences": [s for s, l in classified if l == "Positive"][:5],
        "negative_sentences": [s for s, l in classified if l == "Negative"][:5],
        "neutral_sentences": [s for s, l in classified if l == "Neutral"][:5]
    })

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(STATIC_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)

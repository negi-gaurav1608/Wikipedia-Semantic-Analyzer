# 🧠 Wikipedia Sentiment Analyzer

A full-stack data science web application that scrapes content from Wikipedia, analyzes its sentiment using NLP, and presents insights visually through word clouds and bar charts.


## ✨ Features

- 🔍 **Wikipedia Scraping** — Automatically fetches text from any Wikipedia topic.
- 💬 **Sentiment Analysis** — Classifies text into **positive**, **negative**, and **neutral** using `TextBlob`.
- 📌 **Highlighted Sentences** — Displays categorized sentences based on sentiment.
- 📊 **Data Visualization** — Generates:
  - **Word Cloud** for top frequent words.
  - **Bar Chart** showing word frequencies.
- ⚡ **Live Frontend UI** — Built with **React + Vite** and styled using **Tailwind CSS**.
- 🔄 **Auto-Refreshing Visuals** — Word cloud and bar chart update without manual reload.


## 🔧 Tech Stack

### Frontend
- React
- Vite
- Tailwind CSS
- Axios

### Backend
- Python + Flask
- TextBlob + NLTK (for NLP)
- Matplotlib + WordCloud (for visuals)
- BeautifulSoup (for scraping)

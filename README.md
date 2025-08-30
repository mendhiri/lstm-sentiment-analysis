# BMLP Sentiment Analysis

This project is a sentiment analysis solution for Bahasa Indonesia, focusing on user reviews and social media data. It combines traditional machine learning (LightGBM + TF-IDF) and deep learning (BiLSTM) models to classify sentiment (positive, negative, neutral) from text.

## Project Scope

- Scraping tweets and user reviews (using custom Python scripts)
- Preprocessing and cleaning text data
- Training and evaluating sentiment classification models
- Saving and reusing trained models for predictions

## What I've Done

- Built scrapers for Twitter and app reviegit ws
- Cleaned and preprocessed large datasets
- Trained a LightGBM model with TF-IDF features
- Trained a BiLSTM model using Keras
- Achieved solid accuracy on test data (see below)
- Provided scripts and notebooks for reproducibility

## Model Achievements

- **LightGBM + TF-IDF**: Good baseline, fast inference
- **BiLSTM**: Higher accuracy, better at capturing context
- Both models outperform simple baselines on Indonesian sentiment data

## How to Install & Run

1. Clone this repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Run scrapers to get fresh data
4. Use the provided notebooks/scripts to train or test models

---

Feel free to explore, modify, and use the models for your own Indonesian sentiment analysis tasks!

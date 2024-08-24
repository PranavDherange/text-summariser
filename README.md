# Low Ratings Analysis of Horror Movies

# 🎥 Analyzing Reasons for Low Ratings in Horror Movies

This repository contains a project aimed at understanding the reasons behind low ratings in horror movies by analyzing user reviews. By applying various Natural Language Processing (NLP) techniques, including topic modeling, sentiment analysis, and summarization, the project identifies and summarizes the key aspects that contribute to poor ratings.

## 📝 Table of Contents

- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Preprocessing](#preprocessing)
- [Topic Modeling](#topic-modeling)
- [Sentiment Analysis](#sentiment-analysis)
- [Results and Insights](#results-and-insights)
- [License](#license)

## 📋 Project Overview

This project investigates the common reasons for bad ratings in horror movies based on user reviews. By leveraging techniques such as LDA for topic modeling, RoBERTa for sentiment analysis, and aspect-based summarization, the project aims to extract meaningful insights that can help filmmakers improve their content.

## 📊 Dataset

The dataset used in this project consists of user reviews of horror movies. The dataset includes the following fields:

- **Review Text**: The content of the user's review.
- **Rating**: The numerical rating provided by the user.
- **Movie ID**: Identifier for the movie being reviewed.

## 🛠️ Preprocessing

To prepare the reviews for analysis, the following preprocessing steps were applied:

- **Tokenization**: Splitting text into individual tokens (words).
- **Stop Word Removal**: Filtering out common words that do not contribute to the meaning.
- **Lemmatization**: Converting words to their base forms.

## 🔍 Topic Modeling

Latent Dirichlet Allocation (LDA) was used to identify the underlying topics in the reviews. Each review was assigned a dominant topic, and representative reviews for each topic were identified.

## 😊 Sentiment Analysis

Sentiment analysis was performed using RoBERTa-based models to classify reviews into three categories:

- **Bad**
- **Neutral**
- **Good**

This step helped in filtering reviews that were likely to contain negative sentiment, which are the primary focus of this analysis.

## 📈 Results and Insights

The analysis revealed several recurring themes in the negative reviews of horror movies, including:

- **Poor Plot Development**
- **Lackluster Special Effects**
- **Weak Character Development**
- **Predictable Jump Scares**

These insights provide valuable feedback for filmmakers and producers to consider when developing horror movies.


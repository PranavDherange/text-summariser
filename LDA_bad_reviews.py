import gensim
from gensim import corpora
import json
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer
import nltk
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis

nltk.download('wordnet')

# Load data
with open('horror_movies_ratings_reviews_updated.json', 'r') as json_file:
    data_dict = json.load(json_file)

documents = []
for movie_id in data_dict.keys():
    if len(data_dict[movie_id]) > 0:
        for item in data_dict[movie_id]:
            if item["rating"] <= 5:
                documents.append(item["review"])

# Tokenize, remove stopwords, etc.
def preprocess(text):
    result = []
    for token in simple_preprocess(text):
        if token not in STOPWORDS:
            result.append(WordNetLemmatizer().lemmatize(token, pos='v'))
    return result

processed_reviews = [preprocess(review) for review in documents]

# Create dictionary and corpus
dictionary = corpora.Dictionary(processed_reviews)
corpus = [dictionary.doc2bow(text) for text in processed_reviews]

lda_model = gensim.models.LdaModel(corpus, num_topics=30, id2word=dictionary, passes=15)
dominant_topics = []

for i, review in enumerate(corpus):
    # Get topic probability distribution for a review
    topic_probs = lda_model.get_document_topics(review)

    # Sort the topics by probability
    topic_probs = sorted(topic_probs, key=lambda x: x[1], reverse=True)

    # Get the dominant topic and its probability
    dominant_topic = topic_probs[0][0]
    prob = topic_probs[0][1]

    dominant_topics.append((i, dominant_topic, prob))

N = 50  # You can adjust this number as needed

# For each topic, get the reviews with the highest probability
num_topics = lda_model.num_topics
representative_reviews = {}
for t in range(num_topics):
    # Filter reviews belonging to the topic and sort by probability
    topic_reviews = sorted([r for r in dominant_topics if r[1] == t], key=lambda x: x[2], reverse=True)

    # Get top N reviews for the topic
    top_n_reviews = topic_reviews[:N]
    representative_reviews[t] = [documents[i[0]] for i in top_n_reviews]

print("LDA IS READY !!!")

# To display the representative reviews
for topic_id, reviews in representative_reviews.items():
    # Get topic content (most significant words for the topic)
    topic_content = lda_model.print_topic(topic_id, 20)  # top 20 words; you can adjust the number as needed

    print(f"\nTopic {topic_id} ({topic_content}):")
    for idx, review in enumerate(reviews, 1):
        print(f"{idx}. {review}\n")

# -*- coding: utf-8 -*-
"""my_topic_modeling.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kag66Xffnu6JbTMCV5VR1OSaZlg2hzFx
"""

# Install required libraries
!pip install gensim pyLDAvis

# Import necessary libraries
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.models import Word2Vec
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

# Download stopwords if not already downloaded
nltk.download('stopwords')

# Load the dataset
newsgroups = fetch_20newsgroups(subset='all', categories=['rec.sport.baseball', 'rec.sport.hockey', 'sci.electronics', 'talk.politics.mideast'])
documents = newsgroups.data

# Preprocess the text data
stop_words = stopwords.words('english')
vectorizer = CountVectorizer(stop_words=stop_words)
doc_term_matrix = vectorizer.fit_transform(documents)

# Tokenize the documents
tokenized_docs = [doc.split() for doc in documents]

# Create a dictionary and corpus for Gensim LDA
dictionary = corpora.Dictionary(tokenized_docs)
corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

# Create Gensim LDA model
lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=4, random_state=42, passes=10)

# Display the discovered topics
topics = lda_model.print_topics()
for idx, topic in topics:
    print(f"Topic {idx + 1}: {topic}")

# LDA Visualization with pyLDAvis
lda_display = gensimvis.prepare(lda_model, corpus, dictionary, sort_topics=False)

# Display the visualization inline (only works in Jupyter/Colab)
pyLDAvis.display(lda_display)

# Alternatively, save the visualization to an HTML file
pyLDAvis.save_html(lda_display, 'lda_visualization.html')

# Train Word2Vec model
word2vec_model = Word2Vec(sentences=tokenized_docs, vector_size=100, window=5, min_count=2, workers=4)

# Represent documents as averaged word vectors
def document_vector(doc):
    doc = [word for word in doc if word in word2vec_model.wv.key_to_index]
    return np.mean(word2vec_model.wv[doc], axis=0) if len(doc) > 0 else np.zeros(100)

doc_vectors = [document_vector(doc) for doc in tokenized_docs]

# Calculate the similarity matrix
similarity_matrix = cosine_similarity(doc_vectors)

# Apply K-Means clustering
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(similarity_matrix)

# Visualization of clusters
plt.scatter(similarity_matrix[:, 0], similarity_matrix[:, 1], c=kmeans.labels_)
plt.title('Document Clusters based on Similarity')
plt.show()


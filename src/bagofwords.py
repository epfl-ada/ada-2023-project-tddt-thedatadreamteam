import pandas as pd
import os
import random

import spacy

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

def find_unique_words(article, nlp):
    unique_words = set()
    stop_words = set(stopwords.words('english'))
    
    for line in article:
        if line.strip().startswith("Retrieved from"):
            break

        # Tokenize the text
        tokens = nlp(line.lower())
        lemmatized_tokens = [token.lemma_ for token in tokens]

        # Remove stopwords (common words that typically don't carry much meaning)
        filtered_tokens = [word for word in lemmatized_tokens if word.isalnum() and word not in stop_words and not word.isdigit()]
        
        unique_tokens = set(filtered_tokens)
        unique_words = unique_words | unique_tokens
    return unique_words

def create_doc_word_vector(article, df_words, nlp):
    stop_words = set(stopwords.words('english'))
    word_vector = []
    full_text = ""
    for line in article:
        if line.strip().startswith("Retrieved from"):
            break
        full_text += line

    # print(full_text)
    tokens = nlp(full_text.lower())
    lemmatized_tokens = [token.lemma_ for token in tokens]
    filtered_tokens = [word for word in lemmatized_tokens if word.isalnum() and word not in stop_words]
    filtered_tokens.sort()
    # print(filtered_tokens)
    
    last_word = filtered_tokens[0]
    count = 0
    for i in filtered_tokens:
        if i != last_word:
            if df_words.isin([last_word]).any().any():
                # print("last word: {}".format(last_word))
                idx = df_words[df_words["word"]==last_word].index[0]
                # print("idx {}".format(idx))
                word_vector.append([idx,count])
            last_word = i
            count = 1
            continue
        count +=1
    if df_words.isin([last_word]).any().any():
        # print("last word: {}".format(last_word))
        idx = df_words[df_words["word"]==last_word].index[0]
        # print("idx {}".format(idx))
        word_vector.append([idx,count])
                        
    return word_vector

#### CODE ####

PATH = os.path.join("Data", "plaintext_articles")

df_articles = pd.read_csv(
    os.path.join("Data", "wikispeedia_paths-and-graph", "articles.tsv"),
    sep="\t",
    comment='#',
    skip_blank_lines=True,
    header=None,
    names=["name"]
)
# print(df_articles)
nlp = spacy.load("en_core_web_sm")
N = 25
selection = random.sample(range(0, len(df_articles)), N)
# print(selection)
# selection=[45,35,666]
# rnd_article_name = "Human"
tmp = ["Rocks This is a small repeat repeated USA U.S.A Test. string with repeating repeating repeating words in words as in words"]

unique_words = set()
print("Generating Word set")
for i in selection:
    rnd_article_name = df_articles.name[i]
    print(rnd_article_name)
    rnd_article = open(os.path.join(PATH,"{}.txt".format(rnd_article_name)), "r")
    tokens = find_unique_words(rnd_article, nlp)
    # print(len(tokens))
    unique_words = unique_words | tokens
    rnd_article.close()
print("In {} Articles, found {} unique tokens".format(N, len(unique_words)))

df_unqiue_words = pd.DataFrame(list(unique_words), columns = ["word"])
df_training_articles = df_articles.iloc[selection]
df_training_articles.reset_index(inplace = True, drop = True)

# print(df_unqiue_words)
# print(df_training_articles)

# DocID, WordID, Count
bag_of_words = []

print("Generating Bag of Words")
for i in range(N):
    rnd_article_name = df_training_articles.name[i]
    print(rnd_article_name)
    rnd_article = open(os.path.join(PATH,"{}.txt".format(rnd_article_name)), "r")
    vector = create_doc_word_vector(rnd_article, df_unqiue_words, nlp)
    rnd_article.close()
    for entry in vector:
        bag_of_words.append((i, entry[0], entry[1]))
        # if entry[0]==623:
        #     print((i, entry[0], entry[1]))

# for i in bag_of_words:
#     print(i)
# print(df_unqiue_words)
# print(df_unqiue_words.word[623])

output = open(os.path.join("Output", "BagOfWords.csv"), "w")
output.write("Document, Word, Count\n")
for i in bag_of_words:
    output.write("{}, {}, {}\n".format(i[0], i[1], i[2]))
output.close()

output = open(os.path.join("Output", "Articles.txt"), "w")
for i in range(N):
    output.write("{}\t{}\n".format(i, df_training_articles.name[i]))
output.close()

output = open(os.path.join("Output", "Words.txt"), "w")
for i in range(len(df_unqiue_words)):
    output.write("{}\t{}\n".format(i, df_unqiue_words.word[i]))
output.close()
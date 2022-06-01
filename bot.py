from newspaper import Article
import random
import string 
import nltk
import nltk.data
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
import spacy

warnings.filterwarnings("ignore")

nltk.download("punkt", quiet=True)
tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')


article = Article("https://es.wikipedia.org/wiki/Sigmund_Freud")
article.download()
article.parse()
article.nlp()
corpus = article.text
#print(corpus)
#Tokenization
text = corpus
#sentence_list = nltk.sent_tokenize(text, language='spanish')
#sentence_list = tokenizer.tokenize(text)
nlp = spacy.load("es_dep_news_trf")
doc = nlp(text)
sentence_list = [token.text for token in doc]
#print(tokens)
print(sentence_list)


def greeting_response(text):
    text = text.lower()
    bot_greeting = ["howdi", "hi", "hey", "hello", "hola"]
    user_greeting = ["hi", "hey", "greetings", "hello", "hola"]
    for word in text.split():
        if word in user_greeting:
            return random.choice(bot_greeting)


def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))
    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                #swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index


def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ""
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    #print(similarity_scores_list)
    index = index_sort(similarity_scores_list)
    #print("index")
    #print(index)
    response_flag = 0
    j = 0 
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            #print(sentence_list[index[i]])
            bot_response = bot_response +" "+sentence_list[index[i]]
            response_flag = 1
            j = j+1
        if j > 10000:
            break
    if response_flag == 0:
        bot_response = bot_response+" NO ENTENDER!"
    sentence_list.remove(user_input)

    return bot_response

exit_list = "exit"
while(True):
    user_input = input()
    if user_input == "exit": break 
    if greeting_response(user_input) != None:
        print("Bot: " + greeting_response(user_input))
    else: 
        print("Bot: " + bot_response(user_input))







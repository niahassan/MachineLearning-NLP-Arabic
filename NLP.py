# Importations des bibliothèques
import pymongo
import nltk
import string
from nltk.stem.snowball import ArabicStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim.models import Word2Vec

# Connection à la base de données
connection = pymongo.MongoClient('localhost', 27017)
database = connection["Articles"]
coll = database["Articles_tab"]


# Tokenization
def no_punct(text):
    no_punctuation = "".join([word for word in text if word not in string.punctuation])
    return no_punctuation


def unigram(text):
    uni = word_tokenize(text)
    return uni


def bigram(unig):
    bi = list(nltk.ngrams(unig, 2))
    return bi


def trigam(unig):
    trigam_string = []
    phrase = ""
    tri = list(nltk.ngrams(unig, 3))
    for liste in tri:
        for mot in liste:
            phrase = phrase + mot + " "
        trigam_string.append(phrase)
        phrase = ""
    return trigam_string


# Stop words
def remove_StopWords(text):
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words('Arabic')]
    text = "".join(tokens_without_sw)
    return text


# Stemming
def get_Stem(text):
    stemmer = ArabicStemmer()
    text_tokens = word_tokenize(text)
    text = ""
    for word in text_tokens:
        text += " " + stemmer.stem(word)
    return text


# Lemmatization
def get_Lemm(text):
    lemmatizer = WordNetLemmatizer()
    text_tokens = word_tokenize(text)
    text = ""
    for word in text_tokens:
        text += "" + lemmatizer.lemmatize(word)
    return text


# POS tagging
def get_pos(text):
    text_tokens = word_tokenize(text)
    text = nltk.pos_tag(text_tokens)
    return text


# Bag of words
def get_bof(text):
    wordfreq = {}

    text_tokens = word_tokenize(text)
    for word in text_tokens:
        if word not in wordfreq.keys():
            wordfreq[word] = 1
        else:
            wordfreq[word] += 1
    return wordfreq


# Word2Vec
def get_w2v(text):
    text_tokens = word_tokenize(text)
    for word in text_tokens:
        word2vec = Word2Vec(text_tokens, min_count=2)

    vocabulary = word2vec.wv.vocab
    return vocabulary


for document in coll.find():
    text = document['article']
    no_pun = no_punct(text)
    process = remove_StopWords(no_pun)
    process = get_Lemm(process)
    process = get_Stem(process)
    unig = unigram(process)
    big = bigram(unig)
    trig = trigam(unig)
    posTag = get_pos(no_pun)
    bof = get_bof(no_pun)
    w2v = get_w2v(no_pun)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")  #creation d'une nouvelle collection
database = myclient["Articles"]
collection = database["NLP_tab"]

post = {
    "Text": no_pun,
    "Article_sans_sw_avec_lemma_stem": process,
    "Unigram": unig,
    "Bigram": big,
    "Trigram": trig,
    "PosTagging": posTag,
    "bagOFwords": bof,
    "Word2Vec": w2v
}

posted = collection.insert_one(post)   # insertion des resultats dans la nouvelle collection

if posted.acknowledged:       #verification de l'insertion
    print('resultats processus nlp est disponible dans id' + str(posted.inserted_id))

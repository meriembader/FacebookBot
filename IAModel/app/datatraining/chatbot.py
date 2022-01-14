import random
import json 
import pickle
from nltk.corpus.reader.chasen import test
import numpy as np 
 


from datetime import datetime

import nltk 
from nltk.stem.snowball import FrenchStemmer
 
from tensorflow.keras.models import load_model
import sys 


#############################

################


fr = FrenchStemmer('french')
intents = json.loads(open('./app/datatraining/intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('chatbotmodel.h5')
#model = load_model('model_chatbot.model')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [fr.stem(word) for word in sentence_words]
    return sentence_words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag =[0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THREHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THREHOLD]
    results.sort (key= lambda x: x[1], reverse=True)
    return_list = []
    for r in results: 
        return_list.append({'intent': classes[r[0]], 'probability': str})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("Chatbot is running")
#while True :
#    message = input("")   
#    ints = predict_class(message)
#    res =  get_response(ints, intents)
#   print(res)
#    #return res
def trainingchat(message):
    #while True :
    #message = input("")   
    ints = predict_class(message)
    res =  get_response(ints, intents)
    #print(res)
    return res
      
     
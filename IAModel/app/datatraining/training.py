import random
import json
import pickle
import numpy as np
import nltk
#import nltk
#nltk.download('stopwords')
# for the eng : from nltk.stem import WordNetLemmatizer
#from nltk.stem import WordNetLemmatizer
# pour le francais :
from nltk.stem.snowball import FrenchStemmer
#from nltk.stem import WordNetLemmatizer
#from nltk.stem import WordNetLemmatizer
#from nltk.tokenize import word_tokenize
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras.optimizers import SGD 

fr = FrenchStemmer('french')
#lemmatizer = WordNetLemmatizer()
#lemmatizer = WordNetLemmatizer
intents = json.loads(open('./app/datatraining/intents.json').read())

# parcours du intents.json
#fr = SnowballStemmer('french')

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']
 
for intent in intents['intents']:
    for pattern in intent['patterns']:
        #word_list = nltk.word_tokenize(pattern)
        word_list = nltk.word_tokenize(pattern)
        #words.append(word_list)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

#print(documents)
print('----------------------------------------------------------------------------------------------------------------------------------------------')
# tw el franch stemmer0
words = [fr.stem(word) for word in words if word not in ignore_letters]
words = sorted(set(words))
#print(words)

classes = sorted(set(classes))
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(words, open('classes.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

#neoral network

training = []
output_empty = [0] * len(classes)

for document in documents :
    bag = []
    word_patterns = document[0]
    word_patterns = [fr.stem(word.lower()) for word in word_patterns]
    for word in words: 
       bag.append(1) if word in word_patterns else bag.append(0)
    
    
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])


#shuffle data
random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])


#keras work 
model = keras.Sequential()
model.add(layers.Dense(128, input_shape= (len(train_x[0]),), activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(64,activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(len(train_y[0]), activation='softmax'))
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

model.compile(loss='categorical_crossentropy', optimizer=sgd , metrics=['accuracy'])

#model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5 ,verbose=1)

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbotmodel.h5', hist)
#model.save('model_chatbot.model')
print("done")

#print('done')
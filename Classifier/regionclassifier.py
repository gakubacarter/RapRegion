# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 11:52:44 2018

@author: Carter
"""

import keras
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import matplotlib
import matplotlib.pyplot as plt
#%matplotlib inline

def lyricframe(region):

	from os import listdir
	import pandas as pd
	import nltk
	import string
	from string import punctuation
	from nltk.corpus import stopwords
	from nltk.probability import FreqDist

	lyric_df = pd.DataFrame(columns=['name','lyrics'])


	for lyricfile in listdir(region):
	    lyricfile = (region)+(lyricfile)
	    #print(lyricfile)
	    rawlyrics= pd.read_json(lyricfile)
	    songs = rawlyrics.get('songs')
	    
	    for x in songs:
	        lyric_df = lyric_df.append({
	            'name': x.get('title'),
	            'lyrics': x.get('lyrics')
	        }, ignore_index=True)
	    
	#lyric_df.shape
	return(lyric_df)
    
south = lyricframe('south\\')
east = lyricframe('eastcoast\\')




from string import punctuation
eastlyrics_punct = [];
southlyrics_punct = [];

for n in east['lyrics']:
    #print(n)
    removal_string = punctuation+("""’""") #genius.com uses a special ’ character
    transtable = str.maketrans('','',removal_string)
    eastlyrics_punct.append(n.translate(transtable))
    
    
    
for n in south['lyrics']:
    removal_string = punctuation+("""’""") #genius.com uses a special ’ character
    transtable = str.maketrans('','',removal_string)
    southlyrics_punct.append(n.translate(transtable))
    
    
stop_words = stopwords.words('english')
#the two most common contractions that aren't in stopwords.words,
#as well as words used to denote the sections of a song
stop_words.extend(['im','ill','verse','hook','chorus','bridge']) 
stop_words = set(stop_words) #element removal is faster using set than list

word_tokens = nltk.word_tokenize(str(eastlyrics_punct))
word_tokens = [w.lower() for w in word_tokens]

allwords = [w for w in word_tokens if w not in stop_words]

fdeast = FreqDist(allwords)

fdeast.plot(20, cumulative = False)





word_tokens = nltk.word_tokenize(str(southlyrics_punct))
word_tokens = [w.lower() for w in word_tokens]

allwords = [w for w in word_tokens if w not in stop_words]

fdsouth = FreqDist(allwords)

fdsouth.plot(20, cumulative = False)




eastlist = fdeast.most_common(1000)
southlist = fdsouth.most_common(1000)

bothdict = {}

for i in range(1000):
    bothdict[eastlist[i][0]] = i
    
southdict = {}

for i in range(1000):
    southdict[southlist[i][0]] = i
    
delkeys = []

for key in bothdict:
    try: 
        print(southdict[key])
    except:
        delkeys.append(key)
        
for key in delkeys:
    del bothdict[key]
    
    
from keras.models import Model, Sequential
from keras.layers import Dense, Activation
import keras.backend  as K
K.clear_session()

nh = len(east)+len(south)
nin = len(bothdict);
nout = 1;
model = Sequential()
model.add(Dense(nh, input_shape=(nin,), activation='sigmoid', name='hidden'))
model.add(Dense(1, activation='sigmoid', name='output'))
model.summary()

from keras import optimizers

opt = optimizers.Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
model.compile(optimizer=opt,
              loss='binary_crossentropy',
              metrics=['accuracy'])


    
allwords_fd = np.load('trainingwords_fd.npy')

i=1
mapdict = {}

for key in bothdict:
    mapdict.update({key:i})
    i+=1

X = []

for i in range(nh):
    X.append([allwords_fd[i][key]*mapdict[key] for key in bothdict])
    
Xtr = np.array(X)
y = np.zeros(4336)
y[0:1721]=1;
y[1722:]=0
y = np.array(y)

isiteast = model.fit(Xtr, y, epochs=10, batch_size=100)

Xfab = np.load('Xfab.npy')
Xluda = np.load('Xluda.npy')

model.predict(Xfab)
model.predict(Xluda)
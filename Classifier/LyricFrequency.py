


def lyricfreq(region):

	from os import listdir
	import pandas as pd
	import nltk
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




	#creates a string containing the lyrics of every song in the lyrics dataframe
	lyrics = ''.join(lyric_df.lyrics)
	#removes punctuation

	removal_string = string.punctuation+("""’""") #genius.com uses a special ’ character
	transtable = str.maketrans('','',removal_string)
	lyrics_punct = lyrics.translate(transtable)



	#tokenizes string and finds frequency of each word (counts punctuation as a word)
	 
	stop_words = stopwords.words('english')
	#the two most common contractions that aren't in stopwords.words,
	#as well as words used to denote the sections of a song
	stop_words.extend(['im','ill','verse','hook','chorus','bridge']) 
	stop_words = set(stop_words) #element removal is faster using set than list

	word_tokens = nltk.word_tokenize(lyrics_punct) 
	word_tokens = [w.lower() for w in word_tokens]

	filtered_tokens = [w for w in word_tokens if w not in stop_words] 
	#print(filtered_tokens)

	fd = FreqDist(filtered_tokens)

	fd.plot(20, cumulative = False)
	return fd
import numpy as np 
import pandas as pd 
import json
from preprocess import rap_izer
import cPickle

# read in csv of lines & convert to standard format:
df = pd.read_csv('fire_bars.csv')

# get rid of the empty lines in the dataset
df = df.loc[df['verses'] != '']

# open vocabulary:
vocab = pd.read_csv('rap_vocab.csv')

# remove the row if it has a frequency less than a threshold amount:
thresh = 2 
vocab = vocab.loc[vocab['freqs'] >= thresh]

# turn vocab into a dictionary (lookup table):
LUT = { str(vocab.ix[i,1]) : vocab.ix[i,0] for i in range(len(vocab))}
LUT['UNK'] = len(LUT)+1 # add the UNKnown words at the end of dictionary
print('lookup table is the length of: ', len(LUT))

# save memory by deleting unneeded array
del vocab

def get_word_index(word):
	''' 
	takes in the word, finds it location in the LUT or assigns
	the UNK index number to it 
	'''
	try:
		# we have the word in vocab
		indx = LUT[str(word)]
	except:
		# it's not in vocabulary
		indx = LUT['UNK']

	return indx

# for each "sse" tag, loop over each line and create (inpt,target) pairs, by index #
data = [] # will append data to this list...
song = -1 # counts up when reaches next song, set as -1 to be initialized as 0
for i in range(len(df)-1):
	# ignores the last line because it will be covered in the code below
	# turn on switch if sse - (start of new song):
	if df['verses'][i] == 'sse':
		song += 1 # record as next song
		# don't add this line or the next line basically as anew song starting

	else:
		if df['verses'][i+1] == 'sse':
			# if the next line is sse then song ends and we can get rid of the line:
		else:
			# turn the lines into a vector of words...		
			line1 = rap_izer(str(df['verses'][i])).split()
			line2 = rap_izer(str(df['verses'][i+1])).split()

			# convert each word into its index number, if it's not in
			# there then give it a UNK number

			l1 = [get_word_index(word) for word in line1] 
			l2 = [get_word_index(word) for word in line2]

			# add these sequences to the dataset:
			data.append([l1,l2])
			if (i % 100) == 0:
				# show the data every so often because, why not?
				print('iteration %s\'s data looks like' % i)
				print('input bar\n',l1,'\n\noutput bar\n'l2)

# save the 3d data set by pickling it:
cPickle.dump( data, open( "filename.pkl", "wb" ) )









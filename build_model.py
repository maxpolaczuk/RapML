import numpy as np 
import pandas as pd
import _pickle as cPickle
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Embedding, RepeatVector, TimeDistributed, LeakyReLU
import random
from rapml_functions import *

# read in the vocab
vocab = pd.read_csv('rap_vocab.csv')

# get size of vocab
vocabsize = np.max(vocab.ix[:,0].tolist())
print(vocabsize) 
del vocab

print('vocab size is' , vocabsize)
#=============================================================================
# make functions to prepare data

def zero_pad(row, hard_size = 20):
	# pass in a pandas row 
	try:
		row = row.tolist()
		size = len(row) # this is the number of dimensions of the sequence
	except:
		print('using list type already')
		size = hard_size 	

	# make a sparse array the size of vocab & sequence:
	tmp = np.zeros(size, dtype=int)

	# need to pad out the number of entries
	num_entries = len([x for x in row if str(x) != 'nan']) # how many in current sequence

	# pad it to length we require
	padding = size - num_entries

	for i in range(num_entries):
		# one hot this
		tmp[i+padding] = int(row[i])

	return tmp.tolist()	


def embed_and_pad(row, vocab_size = vocabsize):
	# this is for outputs...
	# pass in a pandas row 
	try:
		row = row.tolist()
	except:
		print('using list type already')

	size = len(row) # this is the number of dimensions of the sequence

	# make a sparse array the size of vocab & sequence:
	tmp = np.zeros((size, vocab_size+1))

	# need to pad out the number of entries
	num_entries = len([x for x in row if str(x) != 'nan']) # how many in current sequence

	# pad it to length we require
	padding = size - num_entries

	for i in range(num_entries):
		# push the sequence to the left...
		# one hot this

		tmp[i,int(row[i])] = 1

	return tmp	


def get_sampleweight(row):
	# this is for sample weights of output...
	# pass in a pandas row 
	try:
		row = row.tolist()
	except:
		print('using list type already')

	size = len(row) # this is the number of dimensions of the sequence

	# make an array the size of samples & sequence:
	tmp = np.zeros(size)

	# need to pad out the number of entries
	num_entries = len([x for x in row if str(x) != 'nan']) # how many in current sequence

	# pad it to length we require
	padding = size - num_entries

	for i in range(num_entries):
		# one hot this
		tmp[i] = 1

	return tmp

def get_word_index(word, LUT):
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



def decode_prediction(prediction):
	# takes in one line of prediction 2D array
	# (num_seq, vocab):

	# for each sequence get maximum word activation:
	phrase = []
	conf = []

	for word in range(np.shape(prediction)[0]):
		idx = np.argmax(prediction[word])

		phrase.append(idx) # add in the confidence score and the word index
		conf.append(prediction[word][idx])

	return phrase, conf

#=================================================================================

## because of RAM limitations, make the data into batches: 

def make_batch(inputs_ = pd.read_csv('inputs.csv'),targets_ = pd.read_csv('targets.csv'),batch_size = 2000):
	# they should have same number of samples

	# randomly assign 2000 index numbers to make into a batch
	idxs = random.sample(range(len(inputs_)), batch_size)

	# convert the data into their sampled form...

	ins = [] # empty list
	outs = [] 
	sampleweight = []
	for i in idxs:
		# convert the nans to none
		ins.append(zero_pad(inputs_.ix[i,:]))
		outs.append(embed_and_pad(targets_.ix[i,:]))
		sampleweight.append(get_sampleweight(targets_.ix[i,:]))

	del idxs

	return np.array(ins), np.array(outs), np.array(sampleweight) 

# make the data using the above function
ins, targs, smpweight = make_batch()


# save one output row - for the first one:
pd.DataFrame(targs[0]).transpose().to_csv('first target output.csv')

# build model architecture in keras - (Seq2Seq)
# easy and straightforward so can just use sequential model
if True == True: 
	# hyperparams
	hidden_dim1 = 128
	hidden_dim2 = 64
	embed_dim = 128
	densedim = 256
	n_nxt = 20 # dimension of output sequences

	# model structure
	model = Sequential()
	model.add(Embedding(vocabsize+1,embed_dim, input_length=n_nxt, mask_zero = True))

	# encoder network
	model.add(LSTM(hidden_dim1, return_sequences = True, stateful= False,forget_bias_init='one'))
	model.add(LSTM(hidden_dim2, return_sequences = True, stateful= False,forget_bias_init='one'))
	model.add(LSTM(hidden_dim2, return_sequences = False, stateful= False,forget_bias_init='one'))
	model.add(Dense(densedim, activation='linear'))
	model.add(Dropout(0.5))
	model.add(LeakyReLU(alpha=0.01))
	model.add(RepeatVector(n_nxt))

	# decoder network
	model.add(LSTM(hidden_dim2,return_sequences=True,stateful=False,forget_bias_init='one'))	        
	model.add(TimeDistributed(Dense(vocabsize+1, activation = "softmax")))
	model.compile(loss='categorical_crossentropy', optimizer='rmsprop',sample_weight_mode='temporal')


# fit the model in batches:
epochs = 5
for i in range(epochs):
	print('BATCH %s' % i)
	if i > 0:
		# not the first batch so make some new data
		try:
			# remove the old input data - so we have memory:
			del ins
			del targs
			del smpweight
		except:
			print('ins and targs are already deleted')
		# make some new data:
		ins, targs, smpweight = make_batch()

	# fit the model on this batch
	model.fit(ins,targs, validation_split = 0.1, batch_size=10,nb_epoch = 1, sample_weight= smpweight)
	# remove ins and targs for memory:
	del ins
	del targs
	del smpweight



# make a prediction:
print('MAKE A PREDICTION!')
# read back in vocabulary
vocab = pd.read_csv('rap_vocab.csv')
# make vocab lookup table
LUT = {  str(vocab.ix[i,1]) : vocab.ix[i,0] for i in range(len(vocab))} 
LUT['UNK'] = len(LUT)+1 # add the UNKnown words at the end of dictionary

# make reverse lookup:
INVLUT = { vocab.ix[i,0] :  str(vocab.ix[i,1]) for i in range(len(vocab))} 
INVLUT[len(LUT)+1] = 'UNK'


del vocab


close = False # 
while close == False:
	predline = input('Please enter your first line: \n')
	print('predicting next verse from: ', rap_izer(predline))
	# 
	print('splitting into common words:')
	predline_inp = rap_izer(predline).split()

	pred_inp = [] # setup empty array
	# get each index from vocab:
	for word in predline_inp:
		pred_inp.append(get_word_index(word,LUT))

	# convert pred_inp into np array:
	pred_inp = np.array(zero_pad(pred_inp))
	print('shape of array is: ', np.shape(pred_inp))
	# reshape maybe:
	pred_inp = np.reshape(pred_inp,(1,np.shape(pred_inp)[0]))

	print('\nprediction input looks like:\n', pred_inp)

	# try a prediction:
	pred_result = model.predict(pred_inp)

	print('prediction result shape is: ' , np.shape(pred_result))

	# reshape prediction:
	pred_result = np.reshape(pred_result,(np.shape(pred_result)[1],np.shape(pred_result)[2]))
	
	# need to decode the predictions into a sentence...
	pred, conf = decode_prediction(pred_result)
	print(pred,conf)

	# decode index #'s into real words:
	strng = '' # store the word here
	for word_idx in pred:
		# get the word
		strng +=  str(INVLUT[int(word_idx)])
		strng += ' ' # add spaces

	print('prediction is:\n',strng)

	# continue
	choice = input('do another phrase? (y/n): ')
	if choice == 'n':
		# finish the program!
		break
		close = True




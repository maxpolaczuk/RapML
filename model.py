import numpy as np 
import _pickle as cPickle # for name convience (from python 2.7)
import pandas as pd 

#import seq2seq
#from seq2seq.models import AttentionSeq2Seq


# load in the datasets
inps = pd.read_csv('inputs.csv')
targets = pd.read_csv('targets.csv')
vocab = pd.read_csv('rap_vocab.csv')

# get size of vocab
vocabsize = np.max(vocab.ix[:,0].tolist())
print(vocabsize) 
del vocab

def embed_and_pad(row, vocab_size = vocabsize):
	# pass in a pandas row 
	row = row.tolist()

	size = len(row) # this is the number of dimensions of the sequence

	# make a sparse array the size of vocab & sequence:
	tmp = np.zeros((size, vocab_size))

	# need to pad out the number of entries
	num_entries = len([x for x in row if str(x) != 'nan']) # how many in current sequence

	# pad it to length we require
	padding = size - num_entries

	for i in range(num_entries):
		# one hot this
		tmp[i+padding,int(row[i])] = 1

	return tmp	


# preprocess them to be one-hot for each array

print('show 3 inputs')

# split it into 3 batches of data and save them...
for b in range(3):
	inputs = [] # store the preprocessed inputs in here
	outputs = [] # same with outputs
	for i in range(b*1000,1000 + b*1000):
		inputs.append(embed_and_pad(inps.ix[i,:]))
	# save the inputs array as a pickle
	cPickle.dump( inputs, open( "input batch %s.pkl" % b, "wb" ) )
	
	
	for i in range(b*1000,1000 + b*1000):
		outputs.append(embed_and_pad(inps.ix[i,:]))
	# save output arrays
	cPickle.dump( outputs, open( "output batch %s.pkl" % b, "wb" ) )
	

print(np.dstack(inputs))


# Define the model:



#model = AttentionSeq2Seq(input_dim=5, input_length=7, hidden_dim=10, output_length=8, output_dim=20, depth=4)
#model.compile(loss='mse', optimizer='rmsprop'
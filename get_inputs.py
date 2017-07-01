import numpy as np 
import pandas as pd 
import json
import _pickle as cPickle

print('make inputs!')

# make everything more 'hip hop'
def rap_izer(line):
	# convert words to be more rap like
	line = line.lower().replace('(','').replace(')','').replace('#','').replace(':','').replace('*','')
	line = line.replace('--','').replace('+','').replace('-','').replace(',','')
	line = line.replace('ing',"in'").replace('you all',"y'all")
	line = line.replace("do not", "do'nt").replace('that is',"that's").replace('‚Äô','')
	line = line.replace("'ll"," will").replace(' are', "'re").replace('somethin',"somethin'")
	line = line.replace('aaaah','aah').replace('aagh','aah').replace('skkrrrrrrttt','skrrrt')
	line = line.replace('skrrr','skrrrt').replace('skrrt','skrrrt').replace('skrt','skrrrt')
	return line

# read in csv of lines & convert to standard format:
df = pd.read_csv('fire_bars.csv')

# get rid of the empty lines in the dataset
df = df.loc[df['verses'] != '']

# open vocabulary:
vocab = pd.read_csv('rap_vocab.csv')

# remove the row if it has a frequency less than a threshold amount:
#thresh = 0
#vocab = vocab.loc[vocab['freqs'] >= thresh].reset_index(drop=True)

# turn vocab into a dictionary (lookup table):
LUT = { str(vocab.ix[i,1]) : vocab.ix[i,0] for i in range(len(vocab))}
LUT['UNK'] = len(LUT)+2 # add the UNKnown words at the end of dictionary
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

inpt = [] # for the input array
outpt = [] # for the output array

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
			# ignore
			continue
		else:
			# turn the lines into a vector of words...		
			line1 = rap_izer(str(df['verses'][i])).split()
			line2 = rap_izer(str(df['verses'][i+1])).split()

			# convert each word into its index number, if it's not in
			# there then give it a UNK number

			l1 = [get_word_index(word) for word in line1] 
			l2 = [get_word_index(word) for word in line2]

			# if l1 OR l2 is shorter than the threshold then don't add to data:
			len_min = 5
			len_max = 20
			if (len(l1) >= len_min) & (len(l2) >= len_min) & (len(l1) <= len_max) & (len(l2) <= len_max):
				# add these sequences to the dataset:
				data.append([l1,l2])
				inpt.append(l1)
				outpt.append(l2)

			if (i % 100) == 0:
				# show the data every so often because, why not?
				print('iteration %s\'s data looks like' % i)
				print('input bar\n',l1,'\n\noutput bar\n',l2)


# turn into input and output csvs
inpts = pd.DataFrame(inpt).to_csv('inputs.csv', index=False)
targs = pd.DataFrame(outpt).to_csv('targets.csv', index= False)

# save the 3d data set by pickling it:
#cPickle.dump( data, open( "filename.pkl", "wb" ) )









import numpy as np 
import pandas as pd 
import json

# read in csv & convert to standard format:
df = pd.read_csv('fire_bars.csv')

# make everything more 'hip hop'
def rap_izer(line):
	# convert words to be more rap like
	line = line.lower().replace('(','').replace(')','').replace('#','').replace(':','').replace('*','')
	line = line.replace('--','').replace('+','').replace('-','')
	line = line.replace('ing',"in'").replace('you all',"y'all")
	line = line.replace("do not", "do'nt").replace('that is',"that's").replace('‚Äô','')
	line = line.replace("'ll"," will").replace(' are', "'re").replace('somethin',"somethin'")
	line = line.replace('aaaah','aah').replace('aagh','aah').replace('skkrrrrrrttt','skrrrt')
	line = line.replace('skrrr','skrrrt').replace('skrrt','skrrrt').replace('skrt','skrrrt')
	return line

# build vocabulary
voca = []

for i in range(len(df)):
	line = rap_izer(str(df['verses'][i])).split()
	for j,word in enumerate(line):
		voca.append(str(word))
	# then make voca unique to save memory
	voca = np.unique(voca).tolist()

	#show vocab len at every 100 lines:
	if i % 100 == 0:
		print('iteration %s' % i)
		print('vocabulary is currently: ' , len(voca) )
	# show the vocab at every 1000 lines
	if i % 1000 == 0: 
		print(voca)

# save vocab:

print('saving csv...')
vocab = pd.DataFrame(voca)
vocab.to_csv('rap_vocab.csv')
print('csv saved')
vocab = pd.read_csv('rap_vocab.csv')


# convert vocab to dictionary LUT:
LUT = {  str(vocab.ix[i,1]) : vocab.ix[i,0] for i in range(len(vocab))}
print(LUT)

# get word frequencies:
# setup new col in dataframe:
vocab['freqs'] = np.zeros(len(vocab))

for i in range(len(df)):
	line = rap_izer(str(df['verses'][i])).split()
	for j,word in enumerate(line):
		# add one to the word frequency
		vocab['freqs'][LUT[str(word)]] = vocab['freqs'][LUT[str(word)]] + 1

	if i % 100 == 0:
		print('iteration %s' % i)

# save CSV with frequencies now
print('overwriting csv...')
vocab.to_csv('rap_vocab.csv')
print('csv saved')


# for memory delete what is not needed
del vocab
del voca

# save as a json file
with open('vocab.json', 'w') as f:
    #data['new_key'] = [1, 2, 3]
	json.dump(LUT, f)

print('Saved lookup table to json')

# for every sentence


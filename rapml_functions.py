''' functions we use in rapML '''


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

	
# scrape rap lyrics in python from rap genius
# create a dataset
import pandas as pd
import urllib.request as url
from bs4 import BeautifulSoup

# start with a kendrick song
URL = 'https://genius.com/Kendrick-lamar-element-lyrics'

if True == True:
        # ^^^^ build into a function later ^^^^
        # pretend we using mozilla...
		hdr = {'User-Agent': 'Mozilla/5.0'}
		req = url.Request(URL, headers=hdr)
		page = url.urlopen(req)
		# make the BS object
		soup = BeautifulSoup(page,"html.parser")
		# get the lyrics body section tag:
		body = soup.find_all(class_ = 'lyrics')
		bars = [] #
		for i in body:
			# save this to an array:
			print(i.find_all(text = True))
			
			if ('[' in i.find_all(text = True)) | (i.find_all(text = True) == '\n'):
				# dont add if it contains '['
				# & remove verse if it is only '\n'
				continue
			else:
				# add this line to bars:
				bars.append(i.find_all(text = True))
				
		print('making "bars" into a csv')
		fire = pd.DataFrame(bars,columns=['verses'])
		fire.to_csv('fire_bars.csv')		
		print('saved csv successfully')

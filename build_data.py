# scrape rap lyrics in python from rap genius
# create a dataset
import pandas as pd
import urllib.request as url
from bs4 import BeautifulSoup

# start with a kendrick song
URL = 'https://genius.com/Kendrick-lamar-element-lyrics'

# make a list of some rap songs to make a corpus from
URLS = ['https://genius.com/Eminem-rap-god-lyrics',
'https://genius.com/Eminem-lose-yourself-lyrics',
'https://genius.com/Eminem-the-monster-lyrics',
'https://genius.com/Logic-nikki-lyrics',
'https://genius.com/Logic-under-pressure-lyrics',
'https://genius.com/Logic-alright-lyrics',
'https://genius.com/Logic-gang-related-lyrics',
'https://genius.com/Logic-fade-away-lyrics',
'https://genius.com/Logic-44-bars-lyrics',
'https://genius.com/A-ap-rocky-fuckin-problems-lyrics',
'https://genius.com/Kendrick-lamar-maad-city-lyrics',
'https://genius.com/Kendrick-lamar-swimming-pools-drank-lyrics',
'https://genius.com/Big-sean-control-lyrics',
'https://genius.com/Kendrick-lamar-poetic-justice-lyrics',
'https://genius.com/Kanye-west-ultralight-beam-lyrics',
'https://genius.com/Chance-the-rapper-no-problem-lyrics',
'https://genius.com/Chance-the-rapper-cocoa-butter-kisses-lyrics',
'https://genius.com/Chance-the-rapper-favorite-song-lyrics',
'https://genius.com/Machine-gun-kelly-bad-things-lyrics',
'https://genius.com/French-montana-ocho-cinco-lyrics',
'https://genius.com/Machine-gun-kelly-wild-boy-lyrics',
'https://genius.com/Machine-gun-kelly-mind-of-a-stoner-lyrics',
'https://genius.com/Lil-wayne-love-me-lyrics',
'https://genius.com/Rich-gang-tapout-lyrics',
'https://genius.com/Future-low-life-lyrics',
'https://genius.com/21-savage-and-metro-boomin-x-lyrics',
'https://genius.com/Rocko-uoeno-lyrics',
'https://genius.com/Future-march-madness-lyrics',
'https://genius.com/Future-mask-off-lyrics',
'https://genius.com/Ace-hood-bugatti-lyrics',
'https://genius.com/Future-fuck-up-some-commas-lyrics',
'https://genius.com/Future-where-ya-at-lyrics',
'https://genius.com/Post-malone-white-iverson-lyrics',
'https://genius.com/Post-malone-congratulations-lyrics',
'https://genius.com/Kanye-west-fade-lyrics',
'https://genius.com/Post-malone-deja-vu-lyrics',
'https://genius.com/Post-malone-too-young-lyrics',
'https://genius.com/Post-malone-go-flex-lyrics',
'https://genius.com/A-ap-ferg-work-remix-lyrics',
'https://genius.com/A-ap-rocky-1-train-lyrics',
'https://genius.com/A-ap-ferg-shabba-lyrics',
'https://genius.com/A-ap-rocky-goldie-lyrics',
'https://genius.com/A-ap-rocky-wild-for-the-night-lyrics',
'https://genius.com/Kanye-west-monster-lyrics',
'https://genius.com/French-montana-pop-that-lyrics',
'https://genius.com/Rick-ross-diced-pineapples-lyrics',
'https://genius.com/Rick-ross-stay-schemin-lyrics',
'https://genius.com/Dj-khaled-no-new-friends-lyrics',
'https://genius.com/Migos-versace-lyrics',
'https://genius.com/Migos-bad-and-boujee-lyrics',
'https://genius.com/Migos-t-shirt-lyrics',
'https://genius.com/Kanye-west-mercy-lyrics',
'https://genius.com/Drake-all-me-lyrics',
'https://genius.com/2-chainz-birthday-song-lyrics',
'https://genius.com/2-chainz-no-lie-lyrics',
'https://genius.com/Kanye-west-dont-like-lyrics',
'https://genius.com/Kanye-west-runaway-lyrics',
'https://genius.com/Kanye-west-new-god-flow-lyrics',
'https://genius.com/Kanye-west-so-appalled-lyrics',
'https://genius.com/Future-move-that-dope-lyrics',
'https://genius.com/Wiz-khalifa-see-you-again-lyrics',
'https://genius.com/Ty-dolla-sign-or-nah-remix-lyrics',
'https://genius.com/Mike-will-made-it-23-lyrics',
'https://genius.com/Ab-soul-terrorist-threats-lyrics',
'https://genius.com/Eminem-detroit-vs-everybody-lyrics',
'https://genius.com/Danny-brown-xxx-lyrics',
'https://genius.com/Noisey-the-rap-monument-lyrics',
'https://genius.com/Danny-brown-grown-up-lyrics',
'https://genius.com/Schoolboy-q-collard-greens-lyrics',
'https://genius.com/Macklemore-and-ryan-lewis-white-walls-lyrics',
'https://genius.com/Schoolboy-q-studio-lyrics',
'https://genius.com/Tech-n9ne-worldwide-choppers-lyrics',
'https://genius.com/Tech-n9ne-fragile-lyrics',
'https://genius.com/Tech-n9ne-speedom-worldwide-choppers-2-lyrics',
'https://genius.com/Tech-n9ne-am-i-a-psycho-lyrics',
'https://genius.com/Tech-n9ne-so-dope-they-wanna-lyrics',
'https://genius.com/Rihanna-work-lyrics',
'https://genius.com/Drake-know-yourself-lyrics',
'https://genius.com/Drake-back-to-back-lyrics',
'https://genius.com/Drake-0-to-100-the-catch-up-lyrics',
'https://genius.com/Desiigner-panda-lyrics',
'https://genius.com/Desiigner-tiimmy-turner-lyrics',
'https://genius.com/Drake-started-from-the-bottom-lyrics',
'https://genius.com/Drake-fake-love-lyrics',
'https://genius.com/Drake-the-motto-lyrics',
'https://genius.com/Drake-and-future-jumpman-lyrics',
'https://genius.com/Drake-pound-cake-paris-morton-music-2-lyrics',
'https://genius.com/Drake-furthest-thing-lyrics',
'https://genius.com/Drake-hyfr-lyrics',
'https://genius.com/Drake-over-my-dead-body-lyrics',
'https://genius.com/Drake-the-language-lyrics',
'https://genius.com/Drake-energy-lyrics',
'https://genius.com/Drake-worst-behavior-lyrics',
'https://genius.com/Drake-summer-sixteen-lyrics',
'https://genius.com/Partynextdoor-come-and-see-me-lyrics',
'https://genius.com/Partynextdoor-recognize-lyrics',
'https://genius.com/Partynextdoor-wus-good-curious-lyrics',
'https://genius.com/Partynextdoor-break-from-toronto-lyrics',
'https://genius.com/Rich-gang-lifestyle-lyrics',
'https://genius.com/Ti-about-the-money-lyrics',
'https://genius.com/Young-thug-best-friend-lyrics',
'https://genius.com/Young-thug-check-lyrics',
'https://genius.com/Kanye-west-highlights-lyrics',
'https://genius.com/Young-thug-power-lyrics',
'https://genius.com/Drake-and-future-diamonds-dancing-lyrics',
'https://genius.com/Drake-feel-no-ways-lyrics',
'https://genius.com/Drake-and-future-big-rings-lyrics',
'https://genius.com/Future-i-won-lyrics',
'https://genius.com/Future-trap-niggas-lyrics',
'https://genius.com/Future-move-that-dope-lyrics',
'https://genius.com/Eminem-stan-lyrics',
'https://genius.com/Eminem-without-me-lyrics',
'https://genius.com/Eminem-love-game-lyrics',
'https://genius.com/Eminem-till-i-collapse-lyrics',
'https://genius.com/Eminem-the-real-slim-shady-lyrics',
'https://genius.com/Eminem-no-love-lyrics',
'https://genius.com/Eminem-legacy-lyrics',
'https://genius.com/Eminem-8-mile-final-battle-lyrics',
'https://genius.com/Eminem-stronger-than-i-was-lyrics']


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

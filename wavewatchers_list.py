from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

waveWatchers = ['albonobo@googlewave.com',
				'jeremy.ngl@googlewave.com',
				'samsonthehero@googlewave.com',
				'antimatter15@googlewave.com',
				'alexandrojv9@googlewave.com',
				'sdrinf@googlewave.com',
				'ruben.v.rivera@googlewave.com',
				'cpwernham@googlewave.com',
				'tomhorrocks@googlewave.com',
				'poojasrinivas@googlewave.com',
				'tjb654@googlewave.com',
				'sirdarkstar@googlewave.com',
				'jblossom@googlewave.com',
				'lsmiller221@googlewave.com',
				'nat.abbotts@googlewave.com',
				'mpoole32@googlewave.com',
				'rogerjhenry@googlewave.com',
				'yoann.moinet@googlewave.com',
				'wave-watchers@appspot.com',
				'rooneyrox3@googlewave.com',
				'crcmark@googlewave.com',
				'daybead@googlewave.com',
				'nunn.joshua@googlewave.com']
safe = waveWatchers + [ 'pamela.fox@googlewave.com',
						'nat.abbotts@wavesandbox.com']
						#'austin.chau@googlewave.com',
						#'larster@googlewave.com',
						#'skhannon@googlewave.com'
ifPublic = ('wave-watchers@googlegroups.com', 'public@a.gwave.com')
bad = (	'bononcinid@googlewave.com',
		'elton.gremi@googlewave.com',
		'isenzation@googlewave.com',
		'charanwilliams@googlewave.com',
		'anulia7921@googlewave.com',
		'thewaveframe@googlewave.com',
		'crod2730@googlewave.com',
		'cibaitroll@googlewave.com',
		'tomborrocks@googlewave.com',
		'lazerustd@googlewave.com',
		'maikuliu@googlewave.com',
		'iytytotouy@googlewave.com',
		'immasucks@googlewave.com',
		'chinsienz@googlewave.com',
		'samsonthezero@googlewave.com',
		'pamelo.fox@googlewave.com',
		'pojasrinivas@googlewave.com',
		'jblosom@googlewave.com',
		'tom.horrock@googlewave.com',
		'ruben.v.riverra@googlewave.com',
		'aaron.tieng@googlewave.com',
		'akashleo88@googlewave.com',
		'brn05267@googlewave.com',
		'canles@googlewave.com',
		'chankingguan@googlewave.com',
		'vctrtang@googlewave.com',
		'niefuend@googlewave.com',
		'taschentuchb@googlewave.com',
		'misamisala@googlewave.com',
		'newnar2010@googlewave.com',
		'mahfuzatiku@googlewave.com',
		'kenna180@googlewave.com',
		'',
		'',
		'greylist:',
		'jacky.lvm85@googlewave.com',
		'skvantx@googlewave.com',
		'maryzerafa@googlewave.com',
		'vaughnjovi@googlewave.com',
		'bitoomcom@googlewave.com',
		'',
		'',
		'')
		
if __name__ == '__main__':
  print("\n\n")
  print("Wave-watchers\n\n")
  print(waveWatchers)
  print("Safe\n\n")
  print(safe)
  print("Bad\n\n")
  print(bad)
  

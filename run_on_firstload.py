from google.appengine.ext import db
import wavewatcher_class

MEMBERS = ['tomhorrocks@googlewave.com', 'sirdarkstar@googlewave.com', 'jblossom@googlewave.com', 'antimatter15@googlewave.com', 'daybead@googlewave.com', 'nunn.joshua@googlewave.com', 'rooneyrox3@googlewave.com', 'crcmark@googlewave.com', 'mpoole32@googlewave.com', 'alexandrojv9@googlewave.com', 'rogerjhenry@googlewave.com']
OWNERS = ['sdrinf@googlewave.com', 'albonobo@googlewave.com', 'lsmiller221@googlewave.com', 'jeremy.ngl@googlewave.com', 'tjb654@googlewave.com', 'cpwernham@googlewave.com', 'samsonthehero@googlewave.com', 'ruben.v.rivera@googlewave.com', 'poojasrinivas@googlewave.com', 'yoann.moinet@googlewave.com', 'nat.abbotts@googlewave.com']
NICE_ROBOTS = ['wave-watchers@appspot.com', 'statusee@appspot.com', 'followapp@appspot.com']
TRUSTED = ['pamela.fox@googlewave.com', 'wave-watchers@googlegroups.com']

BLACKLIST = ['bononcinid@googlewave.com', 'elton.gremi@googlewave.com', 'isenzation@googlewave.com', 'charanwilliams@googlewave.com', 'anulia7921@googlewave.com', 'thewaveframe@googlewave.com', 'crod2730@googlewave.com', 'cibaitroll@googlewave.com', 'tomborrocks@googlewave.com', 'lazerustd@googlewave.com', 'maikuliu@googlewave.com', 'iytytotouy@googlewave.com', 'immasucks@googlewave.com', 'chinsienz@googlewave.com', 'samsonthezero@googlewave.com', 'pamelo.fox@googlewave.com', 'pojasrinivas@googlewave.com', 'jblosom@googlewave.com', 'tom.horrock@googlewave.com', 'ruben.v.riverra@googlewave.com', 'aaron.tieng@googlewave.com', 'akashleo88@googlewave.com', 'brn05267@googlewave.com', 'canles@googlewave.com', 'chankingguan@googlewave.com', 'vctrtang@googlewave.com', 'niefuend@googlewave.com', 'taschentuchb@googlewave.com', 'misamisala@googlewave.com', 'newnar2010@googlewave.com', 'mahfuzatiku@googlewave.com', 'kenna180@googlewave.com',]
GREYLIST = ['jacky.lvm85@googlewave.com', 'skvantx@googlewave.com', 'maryzerafa@googlewave.com', 'vaughnjovi@googlewave.com', 'bitoomcom@googlewave.com',]

for wavewatcher in MEMBERS:
    rec = wavewatcher_class.WaveWatchers(userid=wavewatcher, level=wavewatcher_class.ACCESS_LEVELS['MEMBER'])
    rec.put()
    
for wavewatcher in OWNERS:
    rec = wavewatcher_class.WaveWatchers(userid=wavewatcher, level=wavewatcher_class.ACCESS_LEVELS['OWNER'])
    rec.put()

for robot in NICE_ROBOTS:
    rec = wavewatcher_class.WaveWatchers(userid=robot, level=wavewatcher_class.ACCESS_LEVELS['ROBOT'])
    rec.put()

for trusted in TRUSTED:
    rec = wavewatcher_class.WaveWatchers(userid=trusted, level=wavewatcher_class.ACCESS_LEVELS['TRUSTED'])
    rec.put()

for troll in BLACKLIST:
    rec = wavewatcher_class.Villain(userid=troll, level=wavewatcher_class.VILLAIN_LEVELS['BLACKLIST'])
    rec.put()
    
for grey in GREYLIST:
    rec = wavewatcher_class.Villain(userid=grey, level=wavewatcher_class.VILLAIN_LEVELS['BLACKLIST'])
    rec.put()

if __name__ == "__main__":
    print()
    print()
    print(MEMBERS)
    print()
    print(OWNERS)
    print()
    print(NICE_ROBOTS)
    print()
    print(TRUSTED)
    print()
    print(BLACKLIST)
    print()
    print(GREYLIST)
    print()
    

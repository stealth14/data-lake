import couchdb
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json


#######API TWITTER########################
ckey = "URgKLmlHaoUGggjynVvgELYqz"
csecret = "dLnT08kNMPB5hzEPjlslPdYtw2KAVtkAzujXAnjFX016EvJSTR"
atoken = "1279073084696399875-jnY0frFBDirHaXXG0cp43rrFRxaLfV"
asecret = "xHR7qQ1nKcTGJf2hXxbAtTmcypbPBpWM0Yh6WEGtKclVf"
#####################################

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            doc = db.save(dictTweet)
            print ("SAVED" + str(doc) +"=>" + str(data))
        except:
            print ("Already exists")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

'''========couchdb'=========='''
server = couchdb.Server('http://admin:ander123@localhost:5984/')
try:
    db = server.create('politico')
except:
    db = server['politico']
    
'''===============WORDS=============='''    
#twitterStream.filter(locations=[-78.619545,-0.365889,-78.441315,-0.047208])#Quito 
words=['Ecuador','cne','#CNEInforma','presidente','#Elecciones2021','#Elecciones2021Ec','#EleccionesEcuador2021',
'#CalendarioElectoral','presidencia','candidatos','candidatura','elecciones','presidenciales','listas','voto',
'politicos','2021','Lenin Moreno','Rafael Correa','Guillermo Lasso','Pachakutik','Jaime Nebot','mashi',
'Socialcristiano','Lucio Gutierrez']
twitterStream.filter(track=words)
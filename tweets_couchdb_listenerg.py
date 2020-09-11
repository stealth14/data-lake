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
    
'''===============LOCATIONS 20 CITIES ECUADOR=============='''    
#twitterStream.filter(locations=[-78.619545,-0.365889,-78.441315,-0.047208])#Quito 
#twitterStream.filter(locations=[-79.95912,-2.287573,-79.856351,-2.053362])#Guayaquil
twitterStream.filter(locations=[-79.5983,-3.1761,-78.8471,-2.5578]) #Cuenca
#twitterStream.filter(locations=[-79.5484,-0.6987,-78.7461,0.0191]) #Santo Domingo 
#twitterStream.filter(locations=[-80.02869,-3.354746,-79.84235,-3.190935])#Machala
#twitterStream.filter(locations=[-80.912795,-1.135691,-80.663985,-0.928689])#Manta
#twitterStream.filter(locations=[-80.5625,-1.202987,-80.316762,-0.929944]) #Potoviejo
#twitterStream.filter(locations=[-79.269946,-4.132863,-79.137379,-3.850106])#Loja
#twitterStream.filter(locations=[-78.937982,-1.470916,-78.5368,-1.1098])#Ambato
#twitterStream.filter(locations=[-79.8353,0.5667,-79.4046,1.0486]) #Esmeraldas
#twitterStream.filter(locations=[-79.616489,-1.194387,-79.368954,-0.939314]) #Quevedo
#twitterStream.filter(locations=[-78.479556,-0.412589,-78.393941,-0.290761]) #Sangolqui
#twitterStream.filter(locations=[-78.723592,-1.710588,-78.595487,-1.633713]) #Riobamba
#twitterStream.filter(locations=[-78.17586,0.260163,-78.025016,0.499894]) #Ibarra
#twitterStream.filter(locations=[-79.671471,-2.133047,-79.201259,-1.619683]) #Babahoyo
#twitterStream.filter(locations=[-78.667182,-1.008675,-78.40152,-0.867442]) #Latacunga
#twitterStream.filter(locations=[-79.893517,-2.167096,-79.6477,-1.863685]) #Samborondon
#twitterStream.filter(locations=[-80.245823,-3.502263,-80.117762,-3.416315]) #Huaquillas
#twitterStream.filter(locations=[-78.5494,0.6053,-77.5255,1.1979]) #Tulcan
#twitterStream.filter(locations=[-80.2864,-0.8627,-79.5972,0.0894]) #Chone
import pymongo
import pprint
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

'''========Conexion with mongodb=========='''

myClient = pymongo.MongoClient("mongodb://localhost:27017")

mydb = myClient["politico"]
mycol = mydb["politico"]

tweets = mydb.tweets

#######-API TWITTER-#################
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
            
            doc = tweets.insert_one(dictTweet);
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

    
'''===============LOCATIONS PROVINCES ECUADOR=============='''    
#twitterStream.filter(locations=[-80.1029,0.0618,-78.4267,1.4696])  #Esmeraldas
#twitterStream.filter(locations=[-79.5484,-0.6987,-78.7461,0.0191])  #Santo Domingo
#twitterStream.filter(locations=[-79.3709,-0.7211,-77.8397,0.3273])  #Pichincha
#twitterStream.filter(locations=[-79.5275,-2.8367,-78.5679,-2.2169])  #Cañar
#twitterStream.filter(locations=[-78.937982,-1.523145,-78.110204,-0.988147])  #Tungurahua
#twitterStream.filter(locations=[-81.0848,-1.9515,-79.4019,0.3757])  #Manabi
#twitterStream.filter(locations=[-79.8775,-2.133,-79.0816,-0.5374])  #Los Rios
#twitterStream.filter(locations=[-81.0114,-2.5076,-80.1999,-1.6687])  #Santa Elena
#twitterStream.filter(locations=[-80.5634,-3.0643,-79.1019,-0.8367])  #Guayas
#twitterStream.filter(locations=[-80.4678,-3.8901,-79.3654,-3.0471])  #El Oro
#twitterStream.filter(locations=[-92.2072,-1.6122,-89.0382,1.8836])  #Galapagos
#twitterStream.filter(locations=[-79.7637,-3.6284,-78.4236,-2.5544])  #Azuay
#twitterStream.filter(locations=[-78.074092,0.356681,-77.795661,0.588566])  #Bolivar
#twitterStream.filter(locations=[-78.5494,0.3567,-77.5255,1.1979])  #Carchi
#twitterStream.filter(locations=[-79.3393,-1.22,-78.3809,-0.3308])  #Cotopaxi
#twitterStream.filter(locations=[-79.2545,-2.5673,-78.3585,-1.4301]) #Chimborazo 
#twitterStream.filter(locations=[-79.2758,0.1229,-77.8104,0.8766])  #Imbabura
twitterStream.filter(locations=[-80.4847,-4.7489,-79.1007,-3.3296])  #Loja
#twitterStream.filter(locations=[-78.5878,-2.8554,-77.6434,-2.0052])  #Morona Santiago
#twitterStream.filter(locations=[-78.4273,-1.2487,-77.027,0.0343])  #Napo
#twitterStream.filter(locations=[-77.6281,-1.5642,-75.1925,-0.0378])  #Orellana
#twitterStream.filter(locations=[-78.18,-2.609,-75.585,-1.0038])  #Pastaza
#twitterStream.filter(locations=[-77.9795,-0.6558,-75.2233,0.6621])  #Sucumbios
#twitterStream.filter(locations=[-79.4306,-5.0159,-78.3677,-3.3419])  #Zamora Chinchipe
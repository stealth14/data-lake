
import couchdb
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json


###API ########################
ckey = "T7YapWrdqUUlEWxuMCSG2OL9V"
csecret = "X1IIN6iMtPbEtY8chLwV1h77qoIN7uHujFyQMB4MysTlByELxh"
atoken = "1280671151283412992-WuvBt4rcDnFXnoGkqpg2OWGX9NsF1s"
asecret = "FOEFQQS0MBtBAiCCXhe9UKqgrWP1omebDaYm8a639Tuzg"
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
server = couchdb.Server('http://Vicente:Vicente@127.0.0.1:5984/')  #('http://115.146.93.184:5984/')
try:
    db = server.create('gamesmobile')
except:
    db = server['gamesmobile']
    
'''===============LOCATIONS=============='''    

#twitterStream.filter(locations=[40.71427,-74.00597])
#twitterStream.filter(locations=[-74,40,-73,41])  
twitterStream.filter(track=['#mejores', '#videojuegos','#mobiles','#top','celular','#fortnite','Año2020','#Gamer','#FreeFire','#asphalt9','#Callofdutymobile','#historia','#PokemonGo','gamers','#Android','Android','#ios'])
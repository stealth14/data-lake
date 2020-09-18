
##mongo
import pymongo
import pprint

#tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

'''========mongodb'=========='''

myClient = pymongo.MongoClient("mongodb://localhost:27017")

mydb = myClient["gamestoplomasesperado"]
mycol = mydb["tweets"]

posts = mydb.posts

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
            
            doc = posts.insert_one(dictTweet);
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

    
'''===============LOCATIONS=============='''    

#twitterStream.filter(locations=[-78.619545,-0.365889,-78.441315,-0.047208])  
#twitterStream.filter(track=['#mejores', '#videojuegos', '#pc','#moviles','#top','consola','pc','#LoMasEsperado','Ano2020','#Gamer','juegos'])
twitterStream.filter(track=['#mejores', '#videojuegos', '#pc','#moviles','#top','consola','pc','#LoMasEsperado','Ano2020','#Gammer','juegos'])


import pymongo
import pprint
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

'''========conexion mongodb=========='''

myClient = pymongo.MongoClient("mongodb://localhost:27017")

mydb = myClient["music"]
mycol = mydb["music"]

tweets = mydb.tweets

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


'''===============WORDS=============='''    
words=['#music','#musica','#Spotify','#rock','#rap','#reggaeton','#reggae','#latino','#urban','#hiphop','#indie','#trap','#rapper',
'#Musica','#Jazz','#bachata','#Playlist','#Musique','#musicproducer','#MusicLife','#Piano','#Guitarra','#Bajo','#Bateria','#Violin',
'#song','#cancion','#songwriter','#artist','#SoundCloud','#musicalatina','#Salsa']
twitterStream.filter(track=words)
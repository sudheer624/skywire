'''
Created on Jun 27, 2013

@author: swatha
'''
import oauth2
import json
 
def downloadTweets(url):
    consumer = oauth2.Consumer(key = "trO3ZoqxRBFtKVaaxub8ZA", secret = "F5omXHErzDHffGiAEH1QBmDXZhD7udsTaT3x3XVAwag")
    token = oauth2.Token(key = "15847783-SepzF2WIpMuzR6dpCVuLfloxTpGKN6LaHJmBMeQTR", secret = "cHQEfA367zP9KppLNNwNmkMmR9A65d6fFQO7WAjWM")
    client = oauth2.Client(consumer, token)
    return client.request(url)

def getMinimumTweetID(tweetIds):
    minTweetId = tweetIds[0]
    for tweetId in tweetIds :
        if tweetId < minTweetId :
            minTweetId = tweetId
    return minTweetId

def getMaximumTweetID(tweetIds):
    minTweetId = tweetIds[0]
    for tweetId in tweetIds :
        if tweetId > minTweetId :
            minTweetId = tweetId
    return minTweetId
    
if __name__ == '__main__':
    url = "https://api.twitter.com/1.1/search/tweets.json?q=" + "skywire" + "&count=1"
    res, content = downloadTweets(url)
    data = json.loads(content)
    max_id = json.dumps(data['statuses'][0]['id'])
    max_id = 349113569381593088;
    for i in xrange(306,1000) :
        url = "https://api.twitter.com/1.1/search/tweets.json?q=" + "skywire" + "&max_id=" + str(max_id) + "&count=100"
        res, content = downloadTweets(url)
        data = json.loads(content)
        print content
        tweetIds = []
        for tweetInfo in data['statuses'] :
            tweetIds.append(json.dumps(tweetInfo['id']))
        max_id = getMinimumTweetID(tweetIds)
                
        #write to file
        filename = "/home/swatha/workspace-skywire/tweets/skywire-" + str(i)
        file = open(filename, "w")
        file.write(content)
        file.close()
        print " written file : " +  filename
        print " max_id = " + str(max_id)

        

'''
Created on Jul 1, 2013

@author: swatha
'''
import os
import json
import httplib2
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

def readFiles( dir ):
    for dirname, dirnames, filenames in os.walk(dir):
        tweetIds = set();
        count = 0    
        lat = []
        lng = []
        # print path to all filenames.
        for filename in filenames:
            filePath = os.path.join(dirname, filename)
            line = open(filePath).readline()
            tweetContent = json.loads(line)
            for tweetInfo in tweetContent['statuses'] :
                tweetIds.add(json.dumps(tweetInfo['id']))
                tweedText = json.dumps(tweetInfo['text']).lower()
                if "jesus" in tweedText :
                    address = json.dumps(tweetInfo['user']['location'])
                    address = address.replace("\"", "")
                    if len(address) > 0 :
                        address = address.replace(" ", ",+").replace(",,",",")
                        count = count + 1
                        geocodes = getGeoCode( address )
                        for geocode in geocodes :
                            print geocode
                            lat.append(np.float(geocode['lat']))
                            lng.append(np.float(geocode['lng']))
        # orthogonal projection of the Earth
        m = Basemap(projection='mill', lat_0=45, lon_0=10)
        # draw the borders of the map
        m.drawmapboundary()
        # draw the coasts borders and fill the continents
        m.drawcoastlines()
        m.fillcontinents()
        # map city coordinates to map coordinates
        x, y = m(lng, lat)
        # draw a red dot at cities coordinates
        plt.plot(x, y, 'ro')    
        plt.show()  
            
                    
    print "total number of tweets is " + str(len(tweetIds))
    print "Number of tweets with jesus in them : " +  str(count);
    print (count * 100)/len(tweetIds)
            
            
def getGeoCode( address ):
    url = "http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=" + address
    resp, content = httplib2.Http().request(url)
    geocodes = []
    contentJson = json.loads(content)
    if not json.dumps(contentJson['status']).find("OK") == -1 :
        for result in contentJson['results'] : 
            geocode = {}
            geocode['lat'] = json.dumps(result['geometry']['location']['lat'])
            geocode['lng'] = json.dumps(result['geometry']['location']['lng']) 
            geocodes.append(geocode)
    return geocodes

    
if __name__ == '__main__':
    readFiles("/home/swatha/workspace-skywire/tweets/tmp")
    #geocodes = getGeoCode("madanapalle,+india");
    #for geocode in geocodes :
    #    print geocode['lat']
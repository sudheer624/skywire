'''
Created on Apr 18, 2014

@author: sramoji
'''
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site

import httplib2
from bs4 import BeautifulSoup
import json

class Summerizer(Resource):
    def render_GET(self, request):
        request.setHeader("content-type", "application/json")
        if "url" in request.args:
            print request.args['url']
            h = httplib2.Http(".cache")
            resp, content = h.request(request.args['url'][0], "GET")
            dataParser = BeautifulSoup(content)
            dataElems = []
            for elem in dataParser.find_all('p'):
                dataElems.append(self.getTextFromTag(elem))
            return json.dumps(self.getResponseJson(request.args['url'][0], dataElems))
    
    def getTextFromTag(self, hTag):
        return ''.join(hTag.strings)
    
    def getResponseJson(self, url, dataElems):
        response = {"queryUrl" : url,
                    "data" : dataElems}
        return response

rootResource = Resource()
rootResource.putChild("summerize", Summerizer())
factory = Site(rootResource)
reactor.listenTCP(8081, factory)
reactor.run()
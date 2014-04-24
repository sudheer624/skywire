'''
Created on Apr 18, 2014

@author: sramoji
'''
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet.task import deferLater
from twisted.web.server import NOT_DONE_YET

import httplib2
from bs4 import BeautifulSoup
import json
import urllib

from DocumentSummerizer import DocumentSummerizer

class Summerizer(Resource):
    def _delayedRender(self, request):
        request.setHeader("content-type", "application/json")
        if "url" in request.args:
            print request.args['url']
            h = httplib2.Http(".cache")
            resp, content = h.request(request.args['url'][0], "GET")
            dataParser = BeautifulSoup(content)
            dataElems = []
            for elem in dataParser.find_all('p'):
                dataElems.append(self.getTextFromTag(elem))
            query = ""
            if "query" in request.args:
                query = request.args['query'][0]
            print dataElems
            if len(dataElems) > 0:
                summerizer = DocumentSummerizer(dataElems, urllib.unquote(query).decode('utf8'))
                summary = summerizer.getSummary();
                request.write(json.dumps(self.getResponseJson(request.args['url'][0], dataElems, summary)))
                request.finish()
            else:
                request.write(json.dumps(self.getResponseJson(request.args['url'][0], dataElems, "")))
                request.finish()
    
    
    def render_GET(self, request):
        d = deferLater(reactor, 0.1, lambda: request)
        d.addCallback(self._delayedRender)
        return NOT_DONE_YET
    
    def getTextFromTag(self, hTag):
        return ''.join(hTag.strings)
    
    def getResponseJson(self, url, dataElems, summary):
        response = {"queryUrl" : url,
                    "data" : dataElems,
                    "summary" : summary}
        return response

rootResource = Resource()
rootResource.putChild("summerize", Summerizer())
factory = Site(rootResource)
reactor.listenTCP(8081, factory)
reactor.run()
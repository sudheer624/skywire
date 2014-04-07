'''
Created on Jan 7, 2014

@author: swatha
'''

from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site

import time

class RequestHandler(Resource):
    def render_GET(self, request):
        print request
        return "Hello World"
    
rootResource = Resource()
rootResource.putChild("testme", RequestHandler())
factory = Site(rootResource)
reactor.listenTCP(8080, factory)
reactor.run()

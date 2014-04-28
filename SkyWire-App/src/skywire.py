'''
Created on Apr 26, 2014

@author: sramoji
'''
from gevent import monkey; monkey.patch_all()
from gevent import Greenlet
import gevent

from time import sleep
from bottle import get, run, request

import httplib2
from bs4 import BeautifulSoup
import json
import urllib
import urllib2
from datetime import datetime

from DocumentSummerizer import DocumentSummerizer

def getTextFromTag(hTag):
    return ''.join(hTag.strings)

def getResponseJson(url, dataElems, summary):
    response = {"queryUrl" : url,
                "data" : dataElems,
                "summary" : summary}
    return response

def printDelay(startTime):
    endTime = datetime.now();
    delay = endTime - startTime
    print "delay : ", delay.microseconds, "starTime : ", startTime, "endtime", endTime

def process(url, query):
    #h = httplib2.Http(".cache")
    #resp, content = h.request(url, "GET")
    resp = urllib2.urlopen(url)
    content = resp.read()
    gevent.sleep(0)
    return processHtmlData(content, url, query)

def processHtmlData(content, url, query):
    dataParser = BeautifulSoup(content)
    dataElems = []
    for elem in dataParser.find_all('p'):
        dataElems.append(getTextFromTag(elem))

    if len(dataElems) > 0:
        summerizer = DocumentSummerizer(dataElems, urllib.unquote(query).decode('utf8'))
        summary = summerizer.getSummary();
        return json.dumps(getResponseJson(url, dataElems, summary))
    else:
        return json.dumps(getResponseJson(url, dataElems, ""))

@get('/summerize')
def summerize():
    g = Greenlet.spawn(process, request.query.url, request.query.query)
    gevent.joinall([g])
    yield g.value

run(host='0.0.0.0', port=8081, server='gevent', debug=True)
'''
Created on Jan 2, 2014

@author: swatha
'''

class Node :
    def __init__(self):
        self.childNodes = []
        self.subIP = None
    def setIP(self, subIP):
        self.subIP = subIP
    def addChild(self, childNode):
        self.childNodes.append(childNode)
    def getSubIP(self):
        return self.subIP
    def getChildren(self):
        return self.childNodes

def printTree(node, ip):
    
    if(len(node.getChildren()) > 0) :
        for cNode in node.getChildren():
            ip.insert(0, str(cNode.getSubIP()))
            printTree(cNode, ip)
    else :
        #ipStr = "."
        #ipStr  = ipStr.join(ip)
        print node.getSubIP()
            

def printDFTree(rootNode):
    stack = []
    ip = []
    ip.insert(0, rootNode.getSubIP())
    for node in rootNode.getChildren():
        stack.insert(0, node)
    
    while len(stack) > 0 :
        
        
def addChildNode(ipStr, parentNode, subStrIndex):
    numOfDigits = len(ipStr)
    newNode = Node()
    newNode.setIP(int(ipStr[numOfDigits - subStrIndex:]))
    parentNode.addChild(newNode)
    return newNode
          
def findIP(ipStr, node) :
    numOfDigits = len(ipStr)
    #Base case
    if(numOfDigits <= 3):
        subIP = int(ipStr)
        if(subIP <= 255) :
            addChildNode(ipStr, node, 3)

    if(numOfDigits > 1):
        childNode = addChildNode(ipStr, node, 1)
        findIP(ipStr[:numOfDigits-1], childNode)
        if(numOfDigits > 2):
            childNode = addChildNode(ipStr, node, 2)
            findIP(ipStr[:numOfDigits-2], childNode)
            if(numOfDigits > 3):
                subIP = int(ipStr[numOfDigits - 3:])
                if(subIP <= 255) :
                    childNode = addChildNode(ipStr, node, 3)
                    findIP(ipStr[:numOfDigits-3], childNode)


if __name__ == '__main__':
    ipStr = "19216811"
    rootNode = Node()
    findIP(ipStr, rootNode)
    ip = []
    printTree(rootNode, ip)
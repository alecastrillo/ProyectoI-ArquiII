import logging

class ChipBus:
    
    def __init__(self):

        self.requestsQueue = []
        self.controller2P0 = []
        self.controller2P1 = []
    
    def addToRequestsQueue(self, element):
        self.requestsQueue.append(element)

    def removeFirstRequestsQueue(self):
        self.requestsQueue.pop(0)
    
    def getFirstRequestsQueue(self):
        return self.requestsQueue[0]
    
    def updateController2P(self, P, element):
        if P=='P0':
            self.controller2P0 = element
        else: 
            self.controller2P1 = element
    
    def getController2P(self, P):
        if P=='P0':
            return self.controller2P0
        else: 
            return self.controller2P1

print([]==None)
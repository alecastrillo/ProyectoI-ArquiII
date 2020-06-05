import logging

class Bus:
    
    def __init__(self):

        self.L2RequestsQueue = []
        self.MemToL2RequestsQueue = []
        self.controller2L20 = []
        self.controller2L21 = []
        self.controller2Mem = []

        self.responseMem2L2 = []


    def addToL2RequestsQueue(self, element):
        self.L2RequestsQueue.append(element)

    def removeFirstL2RequestsQueue(self):
        self.L2RequestsQueue.pop(0)
    
    def getFirstL2RequestsQueue(self):
        return self.L2RequestsQueue[0]
    
    def addToMemToL2RequestsQueue(self, element):
        self.MemToL2RequestsQueue.append(element)

    def removeFirstMemToL2RequestsQueue(self):
        self.MemToL2RequestsQueue.pop(0)
    
    def getFirstMemToL2RequestsQueue(self):
        return self.MemToL2RequestsQueue[0]

    def updateController2L2(self, chipId, element):
        if chipId == 0:
            self.controller2L20 = element
        else: 
            self.controller2L21 = element
    
    def getController2L2(self, chipId):
        if chipId == 0:
            return self.controller2L20
        else: 
            return self.controller2L21
        
    def getController2Mem(self):
        return self.controller2Mem

    def updateController2Mem(self, element):
        self.controller2Mem = element

    def updateResponseMem2L2(self, chipId, element):
        if chipId == 0:
            self.responseMem2L2 = element
        else: 
            self.responseMem2L2 = element
    
    def getResponseMem2L2(self, chipId):
        if chipId == 0:
            return self.responseMem2L2
        else: 
            return self.responseMem2L2
        



    

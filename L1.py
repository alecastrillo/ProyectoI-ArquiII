from time import sleep
import myglobals 
import logging

class L1():

    def __init__(self, processorId, chipId, bus):
        self.processorId = processorId
        self.chipId = chipId  
        self.bus = bus
        self.memory = [[],[]] 
        logging.info('Cache L1 created for processor '+self.processorId+' from chip '+ str(chipId) +'.')
        self.fill_mem()
        logging.info('Cache L1 initialized for processor '+self.processorId+' from chip '+ str(chipId) +'.')
        self.print_mem()

    def fill_mem(self):
        for i in range(2):
            self.memory[i]= [i,'I', '0', 'FFFF']
    
    def print_mem(self):
        for i in self.memory:
            print(i)
        
    # FROM PROCESSOR

    def requestPrRd(self, address):
        logging.debug('L1.py - requestPrRd')
        cacheBlockIndex = address%2
        cacheBlock = self.memory[cacheBlockIndex]
        if cacheBlock[2] == address:
            if cacheBlock[1] == 'M' or cacheBlock == 'S':
                logging.info('Cache READ HIT - '+self.processorId+','+str(str(self.chipId))+' L1 for address: '+str(address))
                return cacheBlock[3]
            else:
                logging.info('Cache READ MISS - '+self.processorId+','+str(self.chipId)+' L1 for address: '+str(address))
                logging.info('BusRd from '+self.processorId+','+str(self.chipId)+' L1, for address: '+str(address))
                self.bus.addToRequestsQueue(['BusRd', self.processorId, address])
                while self.bus.getController2P(self.processorId)==[]:
                    pass
                cacheBlock[1] = 'S'
                cacheBlock[2] = address
                cacheBlock[3] = self.bus.getController2P(self.processorId)
                self.memory[cacheBlockIndex] = cacheBlock
                self.bus.updateController2P(self.processorId, [])  
        else: 
            logging.info('Cache READ MISS - '+self.processorId+','+str(self.chipId)+' L1 for address: '+str(address))
            logging.info('BusRd from '+self.processorId+','+str(self.chipId)+' L1, for address: '+str(address))
            self.bus.addToRequestsQueue(['BusRd', self.processorId, address])
            while self.bus.getController2P(self.processorId)==[]:
                pass
            cacheBlock[1] = 'S'
            cacheBlock[2] = address
            cacheBlock[3] = self.bus.getController2P(self.processorId)
            self.memory[cacheBlockIndex] = cacheBlock
            self.bus.updateController2P(self.processorId, [])
        
    def requestPrWr(self, address, data):
        logging.debug('L1.py - requestPrWR')
        cacheBlockIndex = address%2
        cacheBlock = self.memory[cacheBlockIndex]
        if cacheBlock[1]=='M':
            logging.info('Cache WRITE MISS - '+self.processorId+','+str(self.chipId)+' L1 for address: '+str(address))
            logging.info('BusRdX from '+self.processorId+','+str(self.chipId)+' L1, for address: '+str(address))
            self.bus.addToRequestsQueue(['BusRdX', self.processorId, cacheBlock[2:], [address,data]])
            cacheBlock[1] = 'M'
            cacheBlock[2] = address
            cacheBlock[3] = data
            self.memory[cacheBlockIndex] = cacheBlock
        else: 
            cacheBlock[1]='M'
            cacheBlock[2]=address
            cacheBlock[3]=data
            self.memory[cacheBlockIndex]=cacheBlock
            logging.info('Cache WRITE HIT - '+self.processorId+','+str(self.chipId)+' L1 for address: '+str(address))
            logging.info('BusUpgr from '+self.processorId+','+str(self.chipId)+' L1, for address: '+str(address))
            logging.debug('L1.py - requestPrWr - adding BusUpgr to requestQueue')
            cacheBlock[1] = 'M'
            cacheBlock[2] = address
            cacheBlock[3] = data
            self.memory[cacheBlockIndex] = cacheBlock
            self.bus.addToRequestsQueue(['BusUpgr', self.processorId, [address,data]])
    
    ## FROM BUS

    def requestBusUpgr(self, address): 
        logging.debug('L1.py - requestBusUpgr')
        logging.debug(str(self.memory[0])+str(self.memory[1]))
        cacheBlockIndex = address%2
        if self.memory[cacheBlockIndex][2]==address:
            self.memory[cacheBlockIndex][1]='I'
        
    def requestFlush(self, address):
        logging.debug('L1.py - requestFlush')
        cacheBlockIndex = address%2
        if self.memory[cacheBlockIndex][2]==address:
            self.memory[cacheBlockIndex][1]='S'


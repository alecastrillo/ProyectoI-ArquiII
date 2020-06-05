import logging
import myglobals

class DirectoryController():
    
    def __init__(self, L2C0, L2C1, mainMemory, bus):
        self.L2C0 = L2C0
        self.L2C1 = L2C1
        self.mainMemory = mainMemory
        self.bus = bus
    
    def requestBusRd(self, remitentProcessorId, remitentChipId, address):
        logging.debug('directoryController.py - requestBusRd - start')
        logging.info('L2Rd from '+remitentProcessorId+','+str(remitentChipId)+' L2, for address: '+str(address))
        result = self.mainMemory.L2Read(remitentChipId, address)
        logging.debug('directoryController.py - requestBusRd - end - '+str(result))
        self.bus.updateController2L2(remitentChipId, result)
        logging.debug('directoryController.py - requestBusRd - end - '+str(result))

    def requestBusUpgr(self, remitentId, address):
        logging.debug('directoryController.py - requestBusUpgr')
        if remitentId == 0:
            self.L2C1.requestBusUpgr(address)
            #self.bus.updateController2L2(0, [])
        else:
            self.L2C0.requestBusUpgr(address)
            #self.bus.updateController2L2(1, [])
        
        return True
    
    def requestMem2L2Upgr(self, remitentChipId, address):
        if remitentChipId == 0:
            self.L2C1.requestMemUpgr(address)
        else:
            self.L2C0.requestMemUpgr(address)
    
    def requestMemRd(self, remitentChipId, address):
        result = ''
        if remitentChipId == 0:
            result = self.L2C1.requestMemRd(remitentChipId, address)
        else:
            result = self.L2C0.requestMemRd(remitentChipId ,address)
        self.bus.updateResponseMem2L2( remitentChipId, result)
    
    def runL2toMem(self):
        try:
            while True:
                while self.bus.L2RequestsQueue==[]:
                    pass
                request = self.bus.getFirstL2RequestsQueue() # FIFO
                logging.info('directoryController.py current request: '+str(request))
                if request[0]=='BusUpgr':
                    self.requestBusUpgr(request[1], request[2])
                elif request[0]=='BusRd':
                    self.requestBusRd(request[1], request[2], request[3])
                self.bus.removeFirstL2RequestsQueue()
        except Exception:
            logging.exception(Exception)
            exit()
    
    def runMemtoL2(self):
        try:
            while True:
                while self.bus.MemToL2RequestsQueue==[]:
                    pass
                request = self.bus.getFirstMemToL2RequestsQueue() # FIFO
                logging.info('directoryController.py current request: '+str(request))
                if request[0]=='Mem2L2Upgr':
                    self.requestBusUpgr(request[1], request[2])
                elif request[0]=='MemRd':
                    self.requestMemRd(request[1], request[2])
                self.bus.removeFirstMemToL2RequestsQueue()
        except Exception:
            logging.exception(Exception)
            exit()

        
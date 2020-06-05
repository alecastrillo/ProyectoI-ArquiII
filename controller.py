import myglobals
import logging 

class Controller():
    
    def __init__(self, chipId, L1P0, L1P1, L2, bus):
        self.chipId = chipId
        self.L1P0 = L1P0
        self.L1P1 = L1P1
        self.L2 = L2
        self.bus = bus

    def requestBusRd(self, remitentId, address):
        logging.debug('controller.py - requestBusRd')
        logging.info('L1Rd from '+remitentId+','+str(self.chipId)+' L1, for address: '+str(address))
        data = self.L2.requestL1Rd(remitentId, address)
        logging.info('BusRd result: ' + data)
        self.bus.updateController2P(remitentId, data)       

    def requestBusRdX(self, remitentId, oldBlock, newBlock):
        logging.debug('controller.py - requestBusRdX')
        logging.info('L1Wr from '+remitentId+','+str(self.chipId)+' L1, writing address '+str(newBlock[0])+' to L2 and let new address '+str(newBlock[0])+' in L1')
        self.L2.requestL1Wr(remitentId, oldBlock[0], oldBlock[1])
        self.requestBusUpgr(remitentId, newBlock[0])

    def requestBusUpgr(self, remitentId, address):
        logging.debug('controller.py - requestBusUpgr')
        if remitentId == 'P0':
            self.L1P1.requestBusUpgr(address)
        else:
            self.L1P0.requestBusUpgr(address)

    def run(self):
        try:
            while True:
                while self.bus.requestsQueue==[]:
                    pass
                request = self.bus.getFirstRequestsQueue() # FIFO
                logging.debug('controller.py request: '+str(request))
                if request[0]=='BusRd':
                    self.requestBusRd(request[1],request[2])
                elif request[0]=='BusRdX':
                    self.requestBusRdX(request[1],request[2],request[3])
                elif request[0]=='BusUpgr':
                    self.requestBusUpgr(request[1], request[2][0])
                self.bus.removeFirstRequestsQueue()
        except Exception:
            logging.exception(Exception)
            exit()

    

    
        
        
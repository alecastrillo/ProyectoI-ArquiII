from time import sleep
import logging
import myglobals 

class Memory:

    def __init__(self, bus):
        self.memory = [None] * 16
        self.fill_mem()
        self.bus = bus
        self.print_mem()

    def fill_mem(self):
        for i in range(16):
            self.memory[i]= [i,'DS', [], 'FFFF']

    def L2Write(self, isRemitentOwner ,remitentChipId, data, address):
        logging.debug('memory.py - write')
        memoryBlock = self.memory[address]
        memoryBlock[1] = 'DM'
        memoryBlock[3] = data
        if isRemitentOwner:
            memoryBlock[2] = [remitentChipId]
        else:
            memoryBlock[2] = []
        self.memory[address]=memoryBlock
        logging.info('Mem2L2Upgr from C'+str(remitentChipId)+' L2, for address '+str(address))
        self.bus.addToL2RequestsQueue(['BusUpgr',remitentChipId, address])
        sleep(myglobals.CPI_MEMORY*(1/myglobals.FREQUENCY))
    
    def read(self, address):
        logging.debug('memory.py - read')
        #sleep(CPI_READ*(1/FREQUENCY))
        return self.memory[address]
    
    def print_mem(self):
        for i in self.memory:
            print(i)

    def requestBusUpgr(self, address):
        self.memory[address][1] = 'DI'

    def L2Read(self, remitentChipId, address):
        logging.debug('memory.py - L2Read start - address' + str(address))
        memoryBlock = self.memory[address]
        logging.info(str(memoryBlock))
        if memoryBlock[1]=='DS':
            logging.info('MEMORY READ HIT - from C'+str(remitentChipId)+' for address: '+str(address))
            logging.debug('memory.py - L2Read memoryBlock[1]==DS -  address' + str(address))
            isC0owner = 0 in memoryBlock[2]
            isC1owner = 1 in memoryBlock[2]
            if remitentChipId == 0:
                if not isC0owner:
                    memoryBlock[2].append(remitentChipId)

                if isC1owner:
                    self.bus.addToL2RequestsQueue(['Mem2L2Upgr', remitentChipId, address])            
            else:
                if not isC1owner:
                    memoryBlock[2].append(remitentChipId)
                if isC0owner:
                    self.bus.addToL2RequestsQueue(['Mem2L2Upgr', remitentChipId, address])            
            self.memory[address] = memoryBlock
        elif memoryBlock[1]=='DM':
            logging.info('MEMORY READ HIT - from C'+str(remitentChipId)+' for address: '+str(address))
            logging.debug('memory.py - L2Read memoryBlock[1]==DM -  address' + str(address))
            isC0owner = 0 in memoryBlock[2]
            isC1owner = 1 in memoryBlock[2]
            if remitentChipId == 0:
                if not isC0owner:
                    memoryBlock[2].append(remitentChipId)
                if isC1owner:
                    self.bus.addToL2RequestsQueue(['Mem2L2Upgr', remitentChipId, address])            
            else:
                if not isC1owner:
                    memoryBlock[2].append(remitentChipId)
                if isC0owner:
                    self.bus.addToL2RequestsQueue(['Mem2L2Upgr', remitentChipId, address])            
            memoryBlock[1] = 'DS'
            self.memory[address] = memoryBlock
        else:
            logging.debug('memory.py - L2Read memoryBlock[1]==DI -  address' + str(address))
            result = '0000'
            self.bus.addToMemToL2RequestsQueue(['MemRd', remitentChipId, address])
            logging.debug('memory.py - L2Read waiting for address '+ str(address))
            while self.bus.getResponseMem2L2(remitentChipId) == []:
                pass
            result = self.bus.getResponseMem2L2(remitentChipId)
            logging.debug('memory.py - L2Read gotten address '+ str(address)+' data '+str(result))
            memoryBlock[1] = 'DS'
            memoryBlock[2] = [0,1]
            memoryBlock[3] = result
            self.bus.updateResponseMem2L2(remitentChipId,[])
            self.memory[address] = memoryBlock
        sleep(myglobals.CPI_MEMORY*(1/myglobals.FREQUENCY))
        return [0 in self.memory[address][2] and 1 in self.memory[address][2],self.memory[address][3]]
            




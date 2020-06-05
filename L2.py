from time import sleep
import myglobals 
import logging

class L2:

    def __init__(self, chipId, bus, mainMemory):
        self.bus = bus
        self.chipId = chipId
        self.memory = [[],[],[],[]]
        self.mainMemory = mainMemory
        logging.info('Cache L2 created for chip '+ str(chipId))
        self.fill_mem()
        logging.info('Cache L2 initialized for chip '+ str(chipId))
        self.print_mem()

    def fill_mem(self):
        for i in range(4):
            # index, state, owner, shared externaly?, address, data
            self.memory[i]= [i,'DI', [], False, '', '0000']
    
    def print_mem(self):
        for i in self.memory:
            print(i)

    ### REQUESTS FROM CONTROLLER L1 TO L2 

    def requestL1Rd(self, remitentId, address):
        logging.debug('L2.py - requestL1Rd')
        cacheBlockIndex = address%4
        cacheBlock = self.memory[cacheBlockIndex]
        #logging.info('cache block' + str(cacheBlock))
        if cacheBlock[4]==address:
            if cacheBlock[1]=='DS':
                logging.info('Cache READ HIT - '+ remitentId  +','+str(self.chipId)+' L2 for address: '+str(address))
                if not (remitentId in cacheBlock[2]):
                    cacheBlock[2].append(remitentId)
                self.memory[cacheBlockIndex] = cacheBlock
                return cacheBlock[5]
            elif cacheBlock[1]=='DM':
                logging.info('Cache READ HIT - '+ remitentId  +','+str(self.chipId)+' L2 for address: '+str(address))
                ##########################################
                # WRITE TO MEM
                self.mainMemory.L2Write(True, self.chipId, cacheBlock[5], cacheBlock[4])
                # self.bus.addToL2RequestsQueue(['BusUpgr', self.chipId, address])
                ########################################################
                logging.info('Address' +str(address)+' in state DM writing it into MEMORY and change it in L2 to DS')
                if not (remitentId in cacheBlock[2]):
                    cacheBlock[2].append(remitentId)
                cacheBlock[1]='DS'
                self.memory[cacheBlockIndex] = cacheBlock
                return cacheBlock[5]
            else:
                logging.info('Cache READ MISS - '+ remitentId  +','+str(self.chipId)+' L2 for address: '+str(address))
                logging.info('BusRd from '+remitentId+','+str(self.chipId)+' L2, for address: '+str(address))
                self.bus.addToL2RequestsQueue(['BusRd', remitentId, self.chipId, address])
                while self.bus.getController2L2(self.chipId) == []:
                    pass
                result = self.bus.getController2L2(self.chipId)
                self.bus.updateController2L2(self.chipId, [])
                logging.debug('L2.py - requestL1Rd - '+str(result))
                if result[0] == False:
                    #result = self.mainMemory.read(address)
                    cacheBlock[1] = 'DS'
                    cacheBlock[2] = [remitentId]
                    cacheBlock[3] = False
                    cacheBlock[4] = address
                    cacheBlock[5] = result[1]
                    self.memory[cacheBlockIndex] = cacheBlock
                    return cacheBlock[5]
                else:
                    cacheBlock[1] = 'DS'
                    cacheBlock[2] = [remitentId]
                    cacheBlock[3] = True
                    cacheBlock[4] = address
                    cacheBlock[5] = result[1]
                    self.memory[cacheBlockIndex] = cacheBlock
                    return cacheBlock[5]
        else:
            logging.info('Cache READ MISS - '+ remitentId  +','+str(self.chipId)+' L2 for address: '+str(address))
            logging.info('BusRd from '+remitentId+','+str(self.chipId)+' L2, for address: '+str(address))
            self.bus.addToL2RequestsQueue(['BusRd', remitentId, self.chipId, address])
            while self.bus.getController2L2(self.chipId) == []:
                pass
            result = self.bus.getController2L2(self.chipId)
            self.bus.updateController2L2(self.chipId, [])
            logging.debug('L2.py - requestL1Rd - '+str(result))
            if result[0] == False:
                #result = self.mainMemory.read(address)
                cacheBlock[1] = 'DS'
                cacheBlock[2] = [remitentId]
                cacheBlock[3] = False
                cacheBlock[4] = address
                cacheBlock[5] = result[1]
                self.memory[cacheBlockIndex] = cacheBlock
                return cacheBlock[5]
            else:
                cacheBlock[1] = 'DS'
                cacheBlock[2] = [remitentId]
                cacheBlock[3] = True
                cacheBlock[4] = address
                cacheBlock[5] = result[1]
                self.memory[cacheBlockIndex] = cacheBlock
                return cacheBlock[5]

    def requestL1Wr(self, remitentId, address, data):
        logging.debug('L2.py - requestL1Wr')
        cacheBlockIndex = address%4
        cacheBlock = self.memory[cacheBlockIndex]
        if cacheBlock[1] == 'DM':
            logging.info('Cache WRITE MISS - '+ remitentId  +','+str(self.chipId)+' L2 for address: '+str(address))
            logging.info('BusRdx from '+remitentId+','+str(self.chipId)+' L2, writing address '+str(cacheBlock[4])+' to Mem and let new address '+str(address)+' in L2')
            logging.info('MemWr from '+remitentId+','+str(self.chipId)+' L2, writing address '+str(cacheBlock[4]))
            self.mainMemory.L2Write(False,  self.chipId, cacheBlock[5], cacheBlock[4])
            cacheBlock[1] = 'DM'
            cacheBlock[2] = [remitentId]
            cacheBlock[3] = False
            cacheBlock[4] = address
            cacheBlock[5] = data
            self.memory[cacheBlockIndex] = cacheBlock
            logging.info('BusUpgr from '+remitentId+','+str(self.chipId)+' L2, for address '+str(address))
            self.bus.addToL2RequestsQueue(['BusUpgr',self.chipId, address])
            self.mainMemory.requestBusUpgr(address)
            return True
        else:
            logging.info('Cache WRITE HIT - '+ remitentId  +','+str(self.chipId)+' L2 for address: '+str(address))
            self.mainMemory.requestBusUpgr(address)
            cacheBlock[1] = 'DM'
            cacheBlock[2] = [remitentId]
            cacheBlock[3] = False
            cacheBlock[4] = address
            cacheBlock[5] = data
            self.memory[cacheBlockIndex] = cacheBlock
            logging.info('BusUpgr from '+remitentId+','+str(self.chipId)+' L2, for address '+str(address))
            self.bus.addToL2RequestsQueue(['BusUpgr',self.chipId, address])
            return True

    def requestBusUpgr(self, address):
        logging.debug('L2.py - requestBusUpgr')
        cacheBlockIndex = address%4
        cacheBlock = self.memory[cacheBlockIndex]
        if cacheBlock[4] == address:
            cacheBlock[1] =  'DI'
            self.memory[cacheBlockIndex] = cacheBlock
        return True

    # REQUEST FROM L2 CONTROLLER 

    def requestMemRd(self,remitentChipId, address):
        logging.debug('L2.py - requestMemRd - address ' + str(address))
        cacheBlockIndex = address%4
        cacheBlock = self.memory[cacheBlockIndex]
        cacheBlock[1] = 'DS'
        cacheBlock[3] = True
        self.memory[cacheBlockIndex] = cacheBlock
        return cacheBlock[5]

    def requestMemUpgr(self, address):
        logging.debug('L2.py - requestMemUpgr - address ' + str(address))
        cacheBlockIndex = address%4
        cacheBlock = self.memory[cacheBlockIndex]
        if cacheBlock[4] == address:
            cacheBlock[3] = True
            self.memory[cacheBlockIndex] = cacheBlock









from time import sleep
import myglobals 
import instructions
import logging

class Processor:

    def __init__(self, processorId, chipId, L1):
        self.processorId = processorId
        self.chipId = chipId
        self.instructions = instructions.Instructions(processorId,chipId)
        self.L1 = L1
    
    def run(self):
        while True:
            for i in self.instructions.memory:
                logging.info('Executing instruction: '+str(i))
                if i[2]=='CALC':
                    sleep(myglobals.CPI_CALC*(1/myglobals.FREQUENCY))
                elif i[2]=='READ':
                    logging.info('PrRd from '+self.processorId+','+str(self.chipId)+' for address: '+str(i[3]))
                    data = self.L1.requestPrRd(i[3])
                    sleep(myglobals.CPI_READ*(1/myglobals.FREQUENCY))
                else:
                    logging.info('PrWr from '+self.processorId+','+str(self.chipId)+' for address: '+str(i[3]))
                    data = self.L1.requestPrWr(i[3], i[4])
                    sleep(myglobals.CPI_WRITE*(1/myglobals.FREQUENCY))
            self.instructions.generate_instructions()
    


import random 
import numpy
import myglobals
import logging

class Instructions:

    def __init__(self, processor, chip):
        self.processor = processor
        self.chip = chip
        self.memorySize = 100
        self.memory = [0] * self.memorySize 
        self.generate_instructions()

    def get_instruction(self, position):
        return self.memory[position]

    def generate_instructions(self):
        for i in range(self.memorySize):
            isCalc = numpy.random.binomial(1, myglobals.CALC_INSTRUCTIONS_PROBABILITY)
            if isCalc:
                self.memory[i] = [self.processor, str(self.chip), 'CALC']
            else:
                isRead = numpy.random.binomial(1, myglobals.READ_INSTRUCTIONS_PROBABILITY)
                memoryAddress = random.randrange(0,myglobals.MAIN_MEMORY_SIZE-1,1)
                if isRead: 
                    self.memory[i] = [self.processor, str(self.chip), 'READ',memoryAddress]
                else: 
                    tmp = str(hex(random.randint(0,65535)))[2:]
                    data = '0'*(4-len(tmp))+tmp 
                    self.memory[i] = [self.processor, str(self.chip), 'WRITE',memoryAddress,data]
        logging.info('Instructions generated for processor '+ self.processor+' from chip ' + str(self.chip)+'.')
        self.print_mem()

    def print_mem(self):
        for i in self.memory:
            print(i)

i = Instructions('P0', 0)
i.generate_instructions()
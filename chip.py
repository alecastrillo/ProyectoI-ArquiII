import threading
import processor 
import controller 
import myglobals
import L1
import L2
import directoryController
import chipBus

class Chip:

    def __init__(self, chipId, memory, bus, directoryController, L2):
        self.bus = bus
        self.memory = memory
        self.chipId = chipId
        self.chipBus = chipBus.ChipBus()
        self.directoryController = directoryController
        self.L1P0 = L1.L1('P0',self.chipId, self.chipBus)
        self.L1P1 = L1.L1('P1',self.chipId, self.chipBus)
        self.P0 = processor.Processor('P0', self.chipId, self.L1P0)
        self.P1 = processor.Processor('P1', self.chipId, self.L1P1)
        self.L2 = L2
        self.controller = controller.Controller(self.chipId, self.L1P0, self.L1P1, self.L2, self.chipBus)
        

    def run(self):
        t1 = threading.Thread(target=self.P0.run)
        t2 = threading.Thread(target=self.P1.run)
        t3 = threading.Thread(target=self.controller.run)
        t1.start()
        t2.start()
        t3.start()

import time 
import threading
import logging
import chip
import L2
import memory
import myglobals
import bus 
import directoryController
from Tkinter import *
from ttk import *
import ScrolledText
import Tkinter as tk


class MultiProcessorSystem():

    def __init__(self):
        self.bus = bus.Bus()
        self.memory = memory.Memory(self.bus)
        self.L2C0 = L2.L2(0, self.bus, self.memory)
        self.L2C1 = L2.L2(1, self.bus, self.memory)
        self.directoryController = directoryController.DirectoryController(self.L2C0, self.L2C1, self.memory, self.bus)
        self.C0 = chip.Chip(0, self.memory, self.bus, self.directoryController, self.L2C0)
        self.C1 = chip.Chip(1, self.memory, self.bus, self.directoryController, self.L2C1)

        self.window = Tk()
        self.tableL1P0C0=Treeview(self.window, height = 2)
        self.tableL1P1C0=Treeview(self.window, height = 2)
        self.tableL1P0C1=Treeview(self.window, height = 2)
        self.tableL1P1C1=Treeview(self.window, height = 2)
        self.tableL2C0=Treeview(self.window, height = 4)
        self.tableL2C1=Treeview(self.window, height = 4)
        self.tableMemory=Treeview(self.window, height = 16)


        self.t1 = threading.Thread(target=self.C0.run)
        self.t2 = threading.Thread(target=self.C1.run)
        self.t3 = threading.Thread(target=self.directoryController.runL2toMem)
        self.t4 = threading.Thread(target=self.directoryController.runMemtoL2)
        self.t5 = threading.Thread(target=self.updateMemories)
        
    

    def GUI(self):
        self.window.title('Multiprocessor System')
        self.window.geometry("1150x530")
        C0L1Frame = Frame(self.window, width=570, height=50)
        
        ##########################################################
        ## C0 P0 L1

        # Define columns 
        self.tableL1P0C0["columns"]=("state","address", "data")
        self.tableL1P0C0.column("#0", width=70, minwidth=70, anchor=CENTER)
        self.tableL1P0C0.column("state", width=70, minwidth=70,anchor=CENTER)
        self.tableL1P0C0.column("address", width=70, minwidth=70, anchor=CENTER)
        self.tableL1P0C0.column("data", width=70, minwidth=70, anchor=CENTER)
        
        # Define headings
        self.tableL1P0C0.heading("#0",text="Index",anchor=CENTER)
        self.tableL1P0C0.heading("state", text="State",anchor=CENTER)
        self.tableL1P0C0.heading("address", text="Address",anchor=CENTER)
        self.tableL1P0C0.heading("data", text="Data",anchor=CENTER)

        for i in self.C0.L1P0.memory:
            self.tableL1P0C0.insert("", 2, "", text=str(i[0]), values=(i[1], i[2], i[3]))
        # Pack it 

        self.tableL1P0C0.grid(row = 0, column = 0, pady = 2) 

        ##########################################################
        ## C0 P1 L1

        # Define columns 
        self.tableL1P1C0["columns"]=("state","address", "data")
        self.tableL1P1C0.column("#0", width=70, minwidth=70, anchor=CENTER)
        self.tableL1P1C0.column("state", width=70, minwidth=70,anchor=CENTER)
        self.tableL1P1C0.column("address", width=70, minwidth=70, anchor=CENTER)
        self.tableL1P1C0.column("data", width=70, minwidth=70, anchor=CENTER)
        
        # Define headings
        self.tableL1P1C0.heading("#0",text="Index",anchor=CENTER)
        self.tableL1P1C0.heading("state", text="State",anchor=CENTER)
        self.tableL1P1C0.heading("address", text="Address",anchor=CENTER)
        self.tableL1P1C0.heading("data", text="Data",anchor=CENTER)

        for i in self.C0.L1P0.memory:
            self.tableL1P1C0.insert("", 2, "", text=str(i[0]), values=(i[1], i[2], i[3]))
        # Pack it 
        self.tableL1P1C0.grid(row = 0, column = 1, pady = 2) 


        ##########################################################
        ## C1 P0 L1

        # Define columns 
        self.tableL1P0C1["columns"]=("state","address", "data")
        self.tableL1P0C1.column("#0", width=70, minwidth=70, anchor=CENTER)
        self.tableL1P0C1.column("state", width=70, minwidth=70,anchor=CENTER)
        self.tableL1P0C1.column("address", width=70, minwidth=70, anchor=CENTER)
        self.tableL1P0C1.column("data", width=70, minwidth=70, anchor=CENTER)
        
        # Define headings
        self.tableL1P0C1.heading("#0",text="Index",anchor=CENTER)
        self.tableL1P0C1.heading("state", text="State",anchor=CENTER)
        self.tableL1P0C1.heading("address", text="Address",anchor=CENTER)
        self.tableL1P0C1.heading("data", text="Data",anchor=CENTER)

        for i in self.C1.L1P0.memory:
            self.tableL1P0C1.insert("", 2, "", text=str(i[0]), values=(i[1], i[2], i[3]))
        # Pack it 

        self.tableL1P0C1.grid(row = 0, column = 2, pady = 2) 

        ##########################################################
        ## C1 P1 L1

        # Define columns 
        self.tableL1P1C1["columns"]=("state","address", "data")
        self.tableL1P1C1.column("#0", width=70, minwidth=70, anchor=CENTER)
        self.tableL1P1C1.column("state", width=70, minwidth=70,anchor=CENTER)
        self.tableL1P1C1.column("address", width=70, minwidth=70, anchor=CENTER)
        self.tableL1P1C1.column("data", width=70, minwidth=70, anchor=CENTER)
        
        # Define headings
        self.tableL1P1C1.heading("#0",text="Index",anchor=CENTER)
        self.tableL1P1C1.heading("state", text="State",anchor=CENTER)
        self.tableL1P1C1.heading("address", text="Address",anchor=CENTER)
        self.tableL1P1C1.heading("data", text="Data",anchor=CENTER)

        for i in self.C1.L1P0.memory:
            self.tableL1P1C1.insert("", 2, "", text=str(i[0]), values=(i[1], i[2], i[3]))
        # Pack it 
        self.tableL1P1C1.grid(row = 0, column = 3, pady = 2) 

        
        ##########################################################
        ## C0 L2

        # Define columns 
        self.tableL2C0["columns"]=("state",'owners', 'sharedE', "address", "data")
        self.tableL2C0.column("#0", width=85, minwidth=85, anchor=CENTER)
        self.tableL2C0.column("state", width=85, minwidth=85, anchor=CENTER)
        self.tableL2C0.column("owners", width=85, minwidth=85, anchor=CENTER)
        self.tableL2C0.column("sharedE", width=85, minwidth=85, anchor=CENTER)
        self.tableL2C0.column("address", width=85, minwidth=85, anchor=CENTER)
        self.tableL2C0.column("data", width=85, minwidth=85, anchor=CENTER)
        
        # Define headings
        self.tableL2C0.heading("#0",text="Index",anchor=CENTER)
        self.tableL2C0.heading("state", text="State",anchor=CENTER)
        self.tableL2C0.heading("owners", text="Owner(s)",anchor=CENTER)
        self.tableL2C0.heading("sharedE", text="E",anchor=CENTER)
        self.tableL2C0.heading("address", text="Address",anchor=CENTER)
        self.tableL2C0.heading("data", text="Data",anchor=CENTER)

        for i in self.L2C0.memory:
            self.tableL2C0.insert("", 2, "", text=str(i[0]), values=(i[1], i[2], i[3],i[4], i[5]))
        

        # Pack it 
        self.tableL2C0.grid(row = 2, column = 0, columnspan=2, pady = 2) 
        
        ##########################################################
        ## C1 L2

        # Define columns 
        self.tableL2C1["columns"]=("state",'owners', 'sharedE', "address", "data")
        self.tableL2C1.column("#0", width=85, minwidth=85, anchor=CENTER)
        self.tableL2C1.column("state", width=85, minwidth=85, anchor=CENTER)
        self.tableL2C1.column("owners", width=85, minwidth=85, anchor=CENTER)
        self.tableL2C1.column("sharedE", width=85, minwidth=85, anchor=CENTER)
        self.tableL2C1.column("address", width=85, minwidth=85, anchor=CENTER)
        self.tableL2C1.column("data", width=85, minwidth=85, anchor=CENTER)
        
        # Define headings
        self.tableL2C1.heading("#0",text="Index",anchor=CENTER)
        self.tableL2C1.heading("state", text="State",anchor=CENTER)
        self.tableL2C1.heading("owners", text="Owner(s)",anchor=CENTER)
        self.tableL2C1.heading("sharedE", text="E",anchor=CENTER)
        self.tableL2C1.heading("address", text="Address",anchor=CENTER)
        self.tableL2C1.heading("data", text="Data",anchor=CENTER)

        for i in self.L2C1.memory:
            self.tableL2C1.insert("", 2, "", text=str(i[0]), values=(i[1], i[2], i[3],i[4], i[5]))
        

        # Pack it 
        self.tableL2C1.grid(row = 2, column = 2, columnspan=2, pady = 2) 

        ##########################################################
        ## Memory self.table 

        # Define columns 
        self.tableMemory["columns"]=("state", "owners","data")
        self.tableMemory.column("#0", width=70, minwidth=70, anchor=CENTER)
        self.tableMemory.column("state", width=70, minwidth=70, anchor=CENTER)
        self.tableMemory.column("owners", width=70, minwidth=70, anchor=CENTER)
        self.tableMemory.column("data", width=70, minwidth=70, anchor=CENTER)
        
        # Define headings
        self.tableMemory.heading("#0",text="Address",anchor=CENTER)
        self.tableMemory.heading("state", text="State",anchor=CENTER)
        self.tableMemory.heading("owners", text="Owner(s)",anchor=CENTER)
        self.tableMemory.heading("data", text="Data",anchor=CENTER)

        for i in self.memory.memory:
            self.tableMemory.insert("", 2, "", text=str(i[0]), values=(i[1], i[2], i[3]))
        

        # Pack it 
        self.tableMemory.grid(row = 3, column = 0, columnspan=2,pady = 2) 



        #########################################################################3
        #########################################################################3
        # Add text widget to display logging info
        st = ScrolledText.ScrolledText(self.window, state='disabled')
        st.configure(font='TkFixedFont')
        st.grid(column=1, row=3, columnspan=3,sticky='e')

        # Create textLogger
        text_handler = TextHandler(st)       

        # Add the handler to logger
        logger = logging.getLogger()        
        logger.addHandler(text_handler)

        self.t5.start()
        
        self.window.mainloop()
        
    
    def updateMemories(self):
        while True:
            x = self.tableL1P0C0.get_children()
            n=0
            for item in x: 
                i = self.C0.L1P0.memory[n]
                self.tableL1P0C0.item(item, text=str(i[0]), values=(i[1], i[2], i[3]))
                n+=1
            
            x = self.tableL1P1C0.get_children()
            n=0
            for item in x: 
                i = self.C0.L1P1.memory[n]
                self.tableL1P1C0.item(item, text=str(i[0]), values=(i[1], i[2], i[3]))
                n+=1

            x = self.tableL1P0C1.get_children()
            n=0
            for item in x: 
                i = self.C1.L1P0.memory[n]
                self.tableL1P0C1.item(item, text=str(i[0]), values=(i[1], i[2], i[3]))
                n+=1

            x = self.tableL1P1C1.get_children()
            n=0
            for item in x: 
                i = self.C1.L1P1.memory[n]
                self.tableL1P1C1.item(item, text=str(i[0]), values=(i[1], i[2], i[3]))
                n+=1
            
            x = self.tableL2C0.get_children()
            n=0
            for item in x: 
                i = self.L2C0.memory[n]
                self.tableL2C0.item(item, text=str(i[0]), values=(i[1], i[2], i[3],i[4], i[5]))
                n+=1
            
            x = self.tableL2C1.get_children()
            n=0
            for item in x: 
                i = self.L2C1.memory[n]
                self.tableL2C1.item(item, text=str(i[0]), values=(i[1], i[2], i[3],i[4], i[5]))
                n+=1
            
            x = self.tableMemory.get_children()
            n=0
            for item in x: 
                i = self.memory.memory[n]
                self.tableMemory.item(item, text=str(i[0]), values=(i[1], i[2], i[3]))
                n+=1

            time.sleep(1)
    
    def run(self):
        self.t1.start()
        self.t2.start()
        self.t3.start()
        self.t4.start()
        self.GUI()



class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


multiP = MultiProcessorSystem()
multiP.run()





    



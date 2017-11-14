'''
Eric Evans

The GUI. Interacts with Main/MyController through vc (View Controller)
'''

import yaml
from tkinter import *


class Application(Frame):

    def __init__(self, master=None, vc=None):
        Frame.__init__(self, master)

        # Configure Master (Main Window)
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.title('Durak Real-Time Assistant')
        width = 300
        height = int(width*(16/9))
        master.minsize(width=width,height=height)
        master.resizable(width=False, height=False) 

        # Set View Controller
        self.vc = vc
        
        # Set Up Grid
        self.grid() # just self
        for r in range(15): # of rows
            self.master.rowconfigure(r, weight=1)
            
        for c in range(9): # of columns
            self.master.columnconfigure(c, weight=1)

        # Add Frames
        self.trump = Frame(self.master, bg='red')
        self.trump.grid(row=0, column=0, rowspan=1, columnspan=9, sticky=W+E+N+S)
        Label(self.trump, text='trump suit').pack()

        self.trump_txt = StringVar()
        Label(self.trump, textvariable=self.trump_txt).pack()
        
        # Comm
        self.clear_comm = Button(self.master, text='X', command=self.vc.clear_comm).grid(row=1, column=0, rowspan=3, columnspan=1, sticky=W+E+N+S)

        self.comm = Frame(self.master, bg='blue')
        self.comm.grid(row=1, column=1, rowspan=3, columnspan=7, sticky=W+E+N+S)
        Label(self.comm, text='community cards').pack()

        self.comm_txt = StringVar()
        Label(self.comm, textvariable=self.comm_txt).pack()
        
        self.add_comm = Button(self.master, text='+', command=self.vc.add_comm_cards).grid(row=1, column=8, rowspan=3, columnspan=1, sticky=W+E+N+S)

        # Hand
        self.clear_hand = Button(self.master, text='X', command=self.vc.clear_hand).grid(row=4, column=0, rowspan=3, columnspan=1, sticky=W+E+N+S)
        
        self.hand = Frame(self.master, bg='green')
        self.hand.grid(row=4, column=1, rowspan=3, columnspan=7, sticky=W+E+N+S)
        Label(self.hand, text='hand cards').pack()

        self.hand_txt = StringVar()
        Label(self.hand, textvariable=self.hand_txt).pack()
        
        self.add_hand = Button(self.master, text='+', command=self.vc.add_hand_cards).grid(row=4, column=8, rowspan=3, columnspan=1, sticky=W+E+N+S)

        # Advice Controls
        self.advice = Frame(self.master, bg='orange')
        self.advice.grid(row=7, column=0, rowspan=5, columnspan=9, sticky=W+E+N+S)
        Label(self.advice, text='best possible plays').pack()

        self.advice_txt = StringVar()
        Label(self.advice, textvariable=self.advice_txt).pack()

        self.defend = Button(self.master, text='Defend', command=self.vc.defend).grid(row=12, column=0, rowspan=3, columnspan=3, sticky=W+E+N+S)
        
        self.attack = Button(self.master, text='Attack', command=self.vc.attack).grid(row=12, column=3, rowspan=3, columnspan=3, sticky=W+E+N+S)

        self.fight = Button(self.master, text='Fight', command=self.vc.fight).grid(row=12, column=6, rowspan=3, columnspan=3, sticky=W+E+N+S)

    # Text Update Handlers
    def update_hand(self,cards):
        self.hand_txt.set(str(cards))
        self.update_advice('')
        
    def update_comm(self,cards):
        self.comm_txt.set(str(cards))
        self.update_advice('')

    def update_advice(self,advc):
        self.advice_txt.set(str(advc))

    def update_trump(self,tp):
        self.trump_txt.set(tp)

        
if __name__ == '__main__':        
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    
                

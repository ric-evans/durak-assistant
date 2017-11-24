'''
 Eric Evans

The GUI. Interacts with Main/MyController through vc (View Controller)
'''

import yaml
from tkinter import *
import os

GRAPHICS_DIR = './graphics/'

class Application(Frame):

    graphics = dict()

    
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
        master.maxsize(width=width,height=height)
        
        # Set View Controller
        self.vc = vc
        
        # Set Up Grid
        self.grid() # just self
        for r in range(15): # of rows
            self.master.rowconfigure(r, weight=1)
            
        for c in range(9): # of columns
            self.master.columnconfigure(c, weight=1)

        # Add Frames
        self.init_trump_frame()
        self.init_comm_frame()
        self.init_hand_frame()
        self.init_advice_frame()

        # Load Graphics
        self.load_graphics()


    # load all graphics from GRAPHICS_DIR into self.graphics
    def load_graphics(self):
        for card_file in os.listdir(GRAPHICS_DIR):
            full_path = os.path.join(GRAPHICS_DIR,card_file)
            photo = PhotoImage(file=full_path)
            card_name = os.path.splitext(card_file)[0]
            self.graphics[card_name] = photo
        #print(self.graphics)
        
        
    # Set Up Trump Controls
    def init_trump_frame(self):
        self.trump = Frame(self.master, bg='red')
        self.trump.pack_propagate(False)
        self.trump.grid(row=0, column=0, rowspan=1, columnspan=9, sticky=W+E+N+S)
        Label(self.trump, text='trump suit').pack()

        self.trump_txt = StringVar()
        Label(self.trump, textvariable=self.trump_txt).pack()
        
    # Set Up Comm Controls
    def init_comm_frame(self):
        # Clear Button
        self.clear_comm = Button(self.master, text='X', command=self.vc.clear_comm).grid(row=1, column=0, rowspan=3, columnspan=1, sticky=W+E+N+S)
        
        # Comm Frame
        self.comm = Frame(self.master, bg='blue')
        self.comm.pack_propagate(False)
        self.comm.grid(row=1, column=1, rowspan=3, columnspan=7, sticky=W+E+N+S)
        Label(self.comm, text='community cards').pack()

        self.comm_txt = StringVar()
        Label(self.comm, textvariable=self.comm_txt).pack()

        # Add Button
        self.add_comm = Button(self.master, text='+', command=self.vc.add_comm_cards).grid(row=1, column=8, rowspan=3, columnspan=1, sticky=W+E+N+S)

    # Set Up Hand Controls
    def init_hand_frame(self):
        # Clear Button
        self.clear_hand = Button(self.master, text='X', command=self.vc.clear_hand).grid(row=4, column=0, rowspan=3, columnspan=1, sticky=W+E+N+S)

        # Hand Frame
        #scrl = Scrollbar(orient="horizontal")
        self.hand = Frame(self.master, bg='green')#, xscrollcommand=scrl.set)
        #self.hand.config(state=DISABLED)
        self.hand.pack_propagate(False)
        self.hand.grid(row=4, column=1, rowspan=3, columnspan=7, sticky=W+E+N+S)
        #Label(self.hand, text='hand cards').pack()

        self.hand_txt = StringVar()
        #Label(self.hand, textvariable=self.hand_txt).pack()

        # Add Button
        self.add_hand = Button(self.master, text='+', command=self.vc.add_hand_cards).grid(row=4, column=8, rowspan=3, columnspan=1, sticky=W+E+N+S)
        
        
    # Set Up Advice Controls
    def init_advice_frame(self):
        # Advice Frame
        self.advice = Frame(self.master, bg='orange')
        self.advice.pack_propagate(False)
        self.advice.grid(row=7, column=0, rowspan=5, columnspan=9, sticky=W+E+N+S)
        Label(self.advice, text='best possible plays').pack()

        self.advice_txt = StringVar()
        Label(self.advice, textvariable=self.advice_txt).pack()

        # Defend Button
        self.defend = Button(self.master, text='Defend', command=self.vc.defend)
        self.defend.grid(row=12, column=0, rowspan=3, columnspan=3, sticky=W+E+N+S)
        self.defend.pack_propagate(False)

        # Attack Button
        self.attack = Button(self.master, text='Attack', command=self.vc.attack)
        self.attack.grid(row=12, column=3, rowspan=3, columnspan=3, sticky=W+E+N+S)
        self.attack.pack_propagate(False)
        
        # Fight Button
        self.fight = Button(self.master, text='Fight', command=self.vc.fight)
        self.fight.grid(row=12, column=6, rowspan=3, columnspan=3, sticky=W+E+N+S)
        self.fight.pack_propagate(False)

        
    # Text Update Handlers
    def update_hand(self,cards):
        self.hand_txt.set(str(cards))
        Label(self.hand, image=self.graphics['2H']).pack(side=LEFT)
        Label(self.hand, image=self.graphics['5D']).pack(side=LEFT)
        Label(self.hand, image=self.graphics['AS']).pack(side=LEFT)
        Label(self.hand, image=self.graphics['2H']).pack(side=LEFT)
        Label(self.hand, image=self.graphics['5D']).pack(side=LEFT)
        Label(self.hand, image=self.graphics['AS']).pack(side=LEFT)
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
    
                

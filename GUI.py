'''
 Eric Evans

The GUI. Interacts with Main/MyController through vc (View Controller)
'''

import yaml
from tkinter import *
import os
import time
from Card import Card

GRAPHICS_DIR = './graphics/big/'
SMALL_GRAPHICS_DIR = './graphics/small/'


class Application(Frame):
    
    graphics = dict()
    small_graphics = dict()
    trump_buttons = dict()
    advice_buttons = dict()
    CANVAS_HEIGHT = 40
    COLOR = {'dark_grey':'#272727',
             'yellow':'#ffe400',
             'green':'#14a76c',
             'orange':'#ff652f',
             'red':'#cc0000',
             'black':'black', 
             'grey':'#747474',
             'light_grey': '#d9d9d9',
             'off_white':'#ececec'}
    ADVICE_COLOR = {'Defend':COLOR['yellow'],
                    'Attack':COLOR['green'],
                    'Fight':COLOR['orange']}
    SUIT_COLOR = {'H':COLOR['red'],
                  'D':COLOR['red'],
                  'S':COLOR['black'],
                  'C':COLOR['black']}
    TEXT_COLOR = COLOR['light_grey']
    FONT = 'Ubuntu 13 bold'
    SUIT_FONT = 'Ubuntu 27 bold'
    SCAN_FONT = 'Ubuntu 20 bold'
    
    X_ADVICE_DRAW_OFFSET = 10

    
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
            
        for c in range(12): # of columns
            self.master.columnconfigure(c, weight=1)

        # Add Frames
        self.init_trump_frame()
        self.init_comm_frame()
        self.init_hand_frame()
        self.init_advice_frame()

        # Load Graphics
        self.load_graphics()


    # load all graphics from GRAPHICS_DIR into self.graphics
    # and from SMALL_GRAPHICS_DIR into self.small_graphics
    def load_graphics(self):
        for card_file in os.listdir(GRAPHICS_DIR):
            full_path = os.path.join(GRAPHICS_DIR,card_file)
            photo = PhotoImage(file=full_path)
            card_name = os.path.splitext(card_file)[0]
            self.graphics[card_name] = photo
        for card_file in os.listdir(SMALL_GRAPHICS_DIR):
            full_path = os.path.join(SMALL_GRAPHICS_DIR,card_file)
            photo = PhotoImage(file=full_path)
            card_name = os.path.splitext(card_file)[0]
            self.small_graphics[card_name] = photo
        #print(self.graphics)
        #print(self.small_graphics)
        
        
    # Set Up Trump Controls
    def init_trump_frame(self):
        #print(sorted(list(tkf.families())))
        # Trump Suit Label
        self.trump = Frame(self.master, bg='red')
        self.trump.pack_propagate(False)
        self.trump.grid(row=0, column=0, rowspan=1, columnspan=12, sticky=W+E+N+S)
        Label(self.trump, text='Trump Suit', fg=self.TEXT_COLOR, bg=self.COLOR['grey'], font=self.FONT).pack(fill=X, side='bottom')
        self.trump.configure(bg=self.COLOR['grey'], highlightthickness=0)

        # Hearts Button
        self.trump_buttons['H'] = Button(self.master, text='♥', font=self.SUIT_FONT, command=self.vc.pick_hearts)
        self.trump_buttons['H'].grid(row=1, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
        self.trump_buttons['H'].configure(highlightthickness=0, borderwidth=0)
        #print(self.trump_buttons['H'].cget('activebackground'))

        # Spades Button
        self.trump_buttons['S'] = Button(self.master, text='♠', font=self.SUIT_FONT, command=self.vc.pick_spades)
        self.trump_buttons['S'].grid(row=1, column=3, rowspan=1, columnspan=3, sticky=W+E+N+S)
        self.trump_buttons['S'].configure(highlightthickness=0, borderwidth=0)

        # Diamonds Button
        self.trump_buttons['D'] = Button(self.master, text='♦', font=self.SUIT_FONT, command=self.vc.pick_diamonds)
        self.trump_buttons['D'].grid(row=1, column=6, rowspan=1, columnspan=3, sticky=W+E+N+S)
        self.trump_buttons['D'].configure(highlightthickness=0, borderwidth=0)

        # Clubs Button
        self.trump_buttons['C'] = Button(self.master, text='♣', font=self.SUIT_FONT, command=self.vc.pick_clubs)
        self.trump_buttons['C'].grid(row=1, column=9, rowspan=1, columnspan=3, sticky=W+E+N+S)
        self.trump_buttons['C'].configure(highlightthickness=0, borderwidth=0)
        
        # Color Buttons
        self.color_trump_buttons()

        
    # Set Up Comm Controls
    def init_comm_frame(self):
        # Clear Button
        self.clear_comm = Button(self.master, text='×', font=self.SCAN_FONT, command=self.vc.clear_comm)
        self.clear_comm.grid(row=2, column=0, rowspan=3, columnspan=1, sticky=W+E+N+S)
        self.clear_comm.configure(bg=self.COLOR['dark_grey'], highlightthickness=0, borderwidth=0)
        
        # Comm Frame
        self.comm = Canvas(self.master, bg='blue', height=self.CANVAS_HEIGHT)
        self.comm.pack_propagate(False)
        self.comm.grid(row=2, column=1, rowspan=3, columnspan=10, sticky=W+E+N+S)
        Label(self.comm, text='Community Cards', fg=self.TEXT_COLOR, bg=self.COLOR['dark_grey'], font=self.FONT).pack(fill=X)
        self.comm.configure(bg=self.COLOR['dark_grey'], highlightthickness=0)
        
        #self.comm_txt = StringVar()
        #Label(self.comm, textvariable=self.comm_txt).pack()

        # Add Button
        self.add_comm = Button(self.master, text='+', font=self.SCAN_FONT, command=self.vc.add_comm_cards)
        self.add_comm.grid(row=2, column=11, rowspan=3, columnspan=1, sticky=W+E+N+S)
        self.add_comm.configure(bg=self.COLOR['dark_grey'], highlightthickness=0, borderwidth=0)

        
    # Set Up Hand Controls
    def init_hand_frame(self):
        # Clear Button
        self.clear_hand = Button(self.master, text='×', font=self.SCAN_FONT, command=self.vc.clear_hand)
        self.clear_hand.grid(row=5, column=0, rowspan=3, columnspan=1, sticky=W+E+N+S)
        self.clear_hand.configure(bg=self.COLOR['grey'], highlightthickness=0, borderwidth=0)
        self.clear_hand.pack_propagate(False)
        
        # Hand Frame
        #scrl = Scrollbar(orient="horizontal")
        self.hand = Canvas(self.master, bg='green', height=self.CANVAS_HEIGHT)
        #self.hand.config(state=DISABLED)
        self.hand.pack_propagate(False)
        self.hand.grid(row=5, column=1, rowspan=3, columnspan=10, sticky=W+E+N+S)
        Label(self.hand, text='Your Hand', fg=self.TEXT_COLOR, bg=self.COLOR['grey'], font=self.FONT).pack(fill=X)
        self.hand.configure(bg=self.COLOR['grey'], highlightthickness=0)
        
        #self.hand_txt = StringVar()
        #Label(self.hand, textvariable=self.hand_txt).pack()

        # Add Button
        self.add_hand = Button(self.master, text='+', font=self.SCAN_FONT, command=self.vc.add_hand_cards)
        self.add_hand.grid(row=5, column=11, rowspan=3, columnspan=1, sticky=W+E+N+S)
        self.add_hand.configure(bg=self.COLOR['grey'], highlightthickness=0, borderwidth=0)
        
        
    # Set Up Advice Controls
    def init_advice_frame(self):
        # Advice Frame
        self.advice = Canvas(self.master, bg='orange', height=self.CANVAS_HEIGHT)
        self.advice.pack_propagate(False)
        self.advice.grid(row=8, column=0, rowspan=6, columnspan=12, sticky=W+E+N+S)
        Label(self.advice, text='Your Best Possible Plays', font=self.FONT, fg=self.TEXT_COLOR, bg=self.COLOR['dark_grey']).pack(fill=X)
        self.advice.configure(bg=self.COLOR['dark_grey'], highlightthickness=0)
        
        #self.advice_txt = StringVar()
        #Label(self.advice, textvariable=self.advice_txt).pack()

        button_row_span = 1
        
        # Defend Button
        self.advice_buttons['Defend'] = Button(self.master, text='Defend', font=self.FONT, command=self.vc.defend)
        self.advice_buttons['Defend'].grid(row=14, column=0, rowspan=button_row_span, columnspan=4, sticky=W+E+N+S)
        self.advice_buttons['Defend'].pack_propagate(False)
        self.advice_buttons['Defend'].configure(highlightthickness=0)

        # Attack Button
        self.advice_buttons['Attack'] = Button(self.master, text='Attack', font=self.FONT, command=self.vc.attack)
        self.advice_buttons['Attack'].grid(row=14, column=4, rowspan=button_row_span, columnspan=4, sticky=W+E+N+S)
        self.advice_buttons['Attack'].pack_propagate(False)
        self.advice_buttons['Attack'].configure(highlightthickness=0)
        
        # Fight Button
        self.advice_buttons['Fight'] = Button(self.master, text='Fight', font=self.FONT, command=self.vc.fight)
        self.advice_buttons['Fight'].grid(row=14, column=8, rowspan=button_row_span, columnspan=4, sticky=W+E+N+S)
        self.advice_buttons['Fight'].pack_propagate(False)
        self.advice_buttons['Fight'].configure(highlightthickness=0)

        # Color Buttons
        self.color_advice_buttons()

        
    # receive new hand cards
    def set_hand(self, cards):
        #cards = [Card('X','H'), Card('3','D')]
        self._draw_list_cards(cards,self.hand)
        self.color_advice_buttons()

        
    # recieve new comm cards
    def set_comm(self,cards):
        self._draw_list_cards(cards, self.comm)
        self.color_advice_buttons()

        
    # clear the advice canvas
    def clear_advice(self):
        self.advice.delete('all')
        
        
    # draw cards on canvas in an overlapping fashion, returning to new line after row_amt
    def _draw_list_cards(self, cards, canvas):
        canvas.delete('all')
        
        if not cards or len(cards) < 1:
            return
        
        cards = [c.short() for c in cards]
        x = 0
        y = 22
        x_shift = 20.8
        y_shift = 43
        row_amt = 11
        col = 0
        
        for c in cards:
            if col > row_amt:
                col = 0
                y = y + y_shift
                x = 0
            canvas.create_image(x, y, anchor=NW, image=self.graphics[c] )
            x = x + x_shift
            col = col + 1

            
    # receive defending advice
    def set_defend_advice(self,advice_tuple):
        self.color_advice_buttons('Defend')

        # uncomment to test canvas drawing
        '''
        advice_tuple = (True,
                 {'defend': [(Card('3', 'H'), Card('8', 'D')),
                             (Card('4', 'H'), Card('X', 'D'))],
                  'pass': [Card('8', 'S'),
                           Card('8', 'H')]
                 })
        '''

        self._draw_defense_cards(advice_tuple)


    # draw cards:
    # defend -> in vt overlapping 'this beats that' fashion
    # pass -> in hz overlapping fashion
    # advice tuple ->
    # (Bool,
    #   {'pass'  : [(card_pass),...],
    #    'defend': [ ( (card_defend),(card_comm) ),... ] }
    # )
    def _draw_defense_cards(self, advice_tuple):
        self.clear_advice()

        if not advice_tuple or len(advice_tuple) < 1:
            return

        # check if play is winnable
        if not advice_tuple[0]:
            print('Not Winnable')
            self.advice.create_text(150, 75, text='Play Is Not Winnable', fill=self.TEXT_COLOR)
        else:
            print('Winnable')

        # Grab play moves dict with pass and defend
        plays = advice_tuple[1]

        # Defending Plays
        if 'defend' in plays.keys():
            defend_duos = [ (d.short(),c.short()) for d,c in plays['defend'] ]
            print('Defend with {}'.format(defend_duos))

            # Draw 
            x = self.X_ADVICE_DRAW_OFFSET
            y = 25
            x_shift = 40
            y_shift = 20
            
            for d,c in defend_duos:
                self.advice.create_image(x, y, anchor=NW, image=self.small_graphics[c])
                self.advice.create_image(x, y+y_shift, anchor=NW, image=self.small_graphics[d])
                x = x + x_shift
                
        else:
            print('Cannot Defend')
            
        # Passing Plays
        if 'pass' in plays.keys():
            pass_list = [ c.short() for c in plays['pass'] ]
            print('Pass with {}'.format(pass_list))

            # Draw
            x = self.X_ADVICE_DRAW_OFFSET
            y = 145
            x_shift = 40
            y_shift = 20

            self.advice.create_text(x+40, y-8, text='Pass Options', fill=self.TEXT_COLOR)
            
            for p in pass_list:
                self.advice.create_image(x, y, anchor=NW, image=self.small_graphics[p])
                x = x + x_shift
        else:
            print('Cannot Pass')

            
    # receive attacking advice
    def set_attack_advice(self,cards):
        self.color_advice_buttons('Attack')
        self._draw_offense_cards(cards)


    # receive fighting advice
    def set_fight_advice(self,cards):
        self.color_advice_buttons('Fight')
        self._draw_offense_cards(cards)

        
    # draw cards, vertically overlapping if a multi-card move
    # cards ->
    # [ [ (card),... ],... ]
    def _draw_offense_cards(self, cards):
        self.clear_advice()

        # uncomment to test canvas drawing
        '''
        cards = [[Card('8', 'S')],[Card('Q', 'C')],[Card('8', 'S'), Card('8', 'H'), Card('8', 'D')],[Card('3', 'H')],[Card('8', 'H')]]
        '''

        if not cards or len(cards) < 1:
            return
        
        cards = [ [c.short() for c in cds] for cds in cards]
        print(cards)
        x = self.X_ADVICE_DRAW_OFFSET
        y = 35
        x_shift = 40
        y_shift = 20
        
        for i,c_gp in enumerate(cards):
            r = i+1
            if r == 1: ranking = '1st'
            elif r == 2: ranking = '2nd'
            elif r == 3: ranking = '3rd'
            else: ranking = '{}th'.format(r)
                
            self.advice.create_text(x+25, y-7, text=ranking, fill=self.TEXT_COLOR)
            y_tmp = y
            for c in c_gp:
                img = self.small_graphics[c]
                self.advice.create_image(x, y_tmp, anchor=NW, image=img)
                y_tmp = y_tmp + y_shift
            x = x + x_shift


    # 'Press' down trump suit button, 'Raise' the others
    def color_trump_buttons(self, trump=None):
        for suit,button in self.trump_buttons.items():
            if not trump:
                button.configure(bg=self.COLOR['grey'], fg=self.SUIT_COLOR[suit])
            else:
                if suit == trump:
                    button.configure(bg=self.COLOR['off_white'], fg=self.SUIT_COLOR[suit])
                else:
                    button.configure(bg=self.COLOR['grey'], fg=self.COLOR['light_grey'])

                    
    # 'Press' down select advice button, 'Raise' the others
    def color_advice_buttons(self, advice=None):
        for name,button in self.advice_buttons.items():
            if advice and name != advice:
                button.configure(bg=self.COLOR['grey'], fg=self.COLOR['light_grey'])
            else:
                button.configure(bg=self.ADVICE_COLOR[name], fg=self.COLOR['black'])

                          
        
if __name__ == '__main__':        
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    
                




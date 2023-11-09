from tkinter import *
from tkinter import messagebox
import random
from is_solvable import is_solvable

class Board:
    def __init__(self, playable=True):
        
        # random init
        self.random_init(playable)
        
        # game board is 2D array of game squares:
        self.bd = []
        i = 0
        for r in range(4):
            row = []
            for c in range(4):
                if self.lot[i] == '0':
                    row.append(Square(r,c,''))
                else:
                    row.append(Square(r,c,self.lot[i]))
                i += 1
            self.bd.append(row)
    
    def random_init(self, playable=True):
        while True:
            # list of text for game squares:
            self.lot = [str(i) for i in range(1,16)] + ['0']
            if not playable:
                break
            # list of text for game squares randomized:
            random.shuffle(self.lot)
            solved = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
            puzzle = []
            for record in self.lot:
                puzzle.append(int(record))
            if is_solvable(tuple(puzzle), solved, size=4):
                break
    
    def get_state(self):
        res = []
        for row in self.bd:
            for record in row:
                tmp = record.get()[1]
                if tmp == '':
                    res.append(0)
                else:
                    res.append(int(tmp))
        return res           
 
    # returns name, text, and button object at row & col:
    def get_item(self, r, c):
        return self.bd[r][c].get()
 
    def get_square(self, r, c):
        return self.bd[r][c]
 
    def game_won(self):
        goal = [str(i) for i in range(1,16)] + ['']
        i = 0
        for r in range(4):
            for c in range(4):
                nm, txt, btn = self.get_item(r,c)
                if txt != goal[i]:
                    return False
                i += 1
        return True

 
class Square:
    def __init__(self, row, col, txt):
        self.row = row
        self.col = col
        self.name = 'btn' + str(row) + str(col)
        self.txt = txt
        self.btn = None
 
    def get(self):
            return [self.name, self.txt, self.btn]
 
    def set_btn(self, btn):
        self.btn = btn
 
    def set_txt(self, txt):
        self.txt = txt
 
 
class Game:
    def __init__(self, gw):
        self.window = gw
 
        # game data:
        self.bd = None
        self.playable = False
 
        # top frame:
        self.top_fr = Frame(gw,
                            width=600,
                            height=100,
                            bg='#0D1917')
        self.top_fr.pack(fill=X)
        
        # new gane btn
        self.play_btn = Button(self.top_fr,
                               text='New \nGame',
                               bd=6,
                               bg='PaleGreen4',
                               fg='White',
                               font='times 16 bold',
                               command=self.new_game)
        self.play_btn.place(relx=0.5, rely=0.5,
                       anchor=CENTER)
 
        # bottom frame:
        self.btm_fr = Frame(gw,
                            width=600,
                            height=500,
                            bg='#0D1917')
        self.btm_fr.pack(fill=X)
 
        # board frame:
        self.bd_fr = Frame(self.btm_fr,
                           width=400+6,
                           height=400+6,
                           relief='solid',
                           highlightthickness=3,
                           highlightbackground ='PaleGreen4',
                           bg='#C0C9D5')
        self.bd_fr.place(relx=0.5, rely=0.5,
                         anchor=CENTER)
 
        self.play_game()
 
 
    def new_game(self):
        
        self.playable = True
        self.play_game()

    def play_game(self):
        # place squares on board:
        if self.playable:
            btn_state = 'normal'
        else:
            btn_state = 'disable'
        self.bd = Board(self.playable)               
        objh = 100  # widget height
        objw = 100  # widget width
        objx = 0    # x-position of widget in frame
        objy = 0    # y-position of widget in frame
        
        for r in range(4):
            for c in range(4):
                nm, txt, btn = self.bd.get_item(r,c)
                bg_color = 'white'
                if txt == '':
                    bg_color = '#C0C9D5'           
                game_btn = Button(self.bd_fr,
                                  text=txt,
                                  relief='solid',
                                  bd=1,
                                  bg=bg_color,
                                  font='times 12 bold',
                                  state=btn_state,
                                  command=lambda x=nm: self.clicked(x))
                game_btn.place(x=objx, y=objy,
                               height=objh, width=objw)
 
                sq = self.bd.get_square(r,c)
                sq.set_btn(game_btn)
 
                objx = objx + objw
            objx = 0
            objy = objy + objh
 
    # processing when a square is clicked:
    def clicked(self, nm):
        r, c = int(nm[3]), int(nm[4])
        nm_fr, txt_fr, btn_fr = self.bd.get_item(r,c)
 
        # cannot move open square to itself:
        if not txt_fr:
            return
 
        # move square to open square if adjacent to it:            
        adjs = [(r-1,c), (r, c-1), (r, c+1), (r+1, c)]
        for x, y in adjs:
            if 0 <= x <= 3 and 0 <= y <= 3:
                nm_to, txt_to, btn_to = self.bd.get_item(x,y)
                if not txt_to:
                    sq = self.bd.get_square(x,y)
                    sq.set_txt(txt_fr)
                    sq = self.bd.get_square(r,c)
                    sq.set_txt(txt_to)
                    btn_to.config(text=txt_fr,
                                  bg='white')
                    btn_fr.config(text=txt_to,
                                  bg='#C0C9D5')
                    # check if game is won:              
                    if self.bd.game_won():
                        ans = messagebox.showinfo(
                            'Result', 'Game Won')
                        self.new_game()
                    return

        return


 
root = Tk()
root.title('15-Puzzle')
root.iconphoto(False, PhotoImage(file='icon.png'))
root.geometry('600x600+100+50')
root.resizable(False, False)
g = Game(root)
root.mainloop()
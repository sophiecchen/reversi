#Sophie Chen
#Mods 3-4
#Reversi / Othello

import tkinter as tk
from tkinter import messagebox

#endings
def done():
    """determins wheter the game is done"""
    global board2d

    for i in range(8):
        for t in range(8):
            if (board2d[i][t] == 0 and legal(i,t,"white")) or (board2d[i][t] == 0 and legal(i,t,"black")):
                return False

    return True

def winner():
    """if done, determins the winner and shows"""
    global board2d
    white_counter = 0
    black_counter = 0
    
    for i in range(8):
        for t in range(8):
            if board2d[i][t] == -1:
                white_counter+=1
            if board2d[i][t] == 1:
                black_counter+=1

    if white_counter > black_counter:
        messagebox.showinfo("Winner","The winner is white! Black: " + str(black_counter) + "\t White: " + str(white_counter))
    elif black_counter > white_counter:
        messagebox.showinfo("Winner","The winner is black! Black: " + str(black_counter) + "\t White: " + str(white_counter))
    else:
        messagebox.showinfo("Winner", "The game is a tie! Black:" + str(black_counter) + "\t White:" + str(white_counter))
                

#2d board change

def immediate_legal(row, column, colour):
    """legal sidekick - tests whether immediate surrondings are occupied"""
    global board2d
    immediate = [[True,True,True],
                 [True,None,True],
                 [True,True,True]]
    
    if colour == "black":
        color = -1
    else:
        color = 1

    if row != 0 and row != 7 and column != 0 and column != 7:
        if board2d[row-1][column-1] == color:
            immediate[0][0] = False
        if board2d[row-1][column] == color:
            immediate[0][1] = False
        if board2d[row-1][column+1] == color:
            immediate[0][2] = False
        if board2d[row][column-1] == color:
            immediate[1][0] = False
        if board2d[row][column+1] == color:
            immediate[1][2] = False
        if board2d[row+1][column-1] == color:
            immediate[2][0] = False
        if board2d[row+1][column] == color:
            immediate[2][1] = False
        if board2d[row+1][column+1] == color:
            immediate[2][2] = False
        
    elif column == 0:
        if board2d[row][column+1] == color:
            immediate[1][2] = False

        (immediate[0][0], immediate[1][0], immediate[2][0]) = False, False, False

        if row != 0 and row!= 7:
            if board2d[row-1][column] == color:
                immediate[0][1] = False
            if board2d[row-1][column+1] == color:
                immediate[0][2] = False
            if board2d[row+1][column] == color:
                immediate[2][1] = False
            if board2d[row+1][column+1] == color:
                immediate[2][2] = False
    
        elif row == 0:
            if board2d[row+1][column] == color:
                immediate[2][1] = False
            if board2d[row+1][column+1] == color:
                immediate[2][2] = False
                
            (immediate[0][1], immediate[0][2]) = False, False
                
        else: #row == 7
            if board2d[row-1][column] == color:
                immediate[0][1] = False
            if board2d[row-1][column+1] == color:
                immediate[0][2] = False
                
            (immediate[2][1], immediate[2][2]) = False, False
        
    elif column == 7:
        if board2d[row][column-1] == color:
            immediate[1][0] = False
            
        (immediate[0][2], immediate[1][2], immediate[2][2]) = False, False, False
        
        if row != 0 and row!= 7:
            if board2d[row-1][column-1] == color:
                immediate[0][0] = False
            if board2d[row-1][column] == color:
                immediate[0][1] = False
            if board2d[row+1][column-1] == color:
                immediate[2][0] = False
            if board2d[row+1][column] == color:
                immediate[2][1] = False

        elif row == 0:
            if board2d[row+1][column-1] == color:
                immediate[2][0] = False
            if board2d[row+1][column] == color:
                immediate[2][1] = False
                
            (immediate[0][0], immediate[0][1]) = False, False
                
        else: #row == 7
            if board2d[row-1][column-1] == color:
                immediate[0][0] = False
            if board2d[row-1][column] == color:
                immediate[0][1] = False
                
            (immediate[2][0], immediate[2][1]) = False, False
            
    elif row == 0:
        (immediate[0][0], immediate[0][1], immediate[0][2]) = False, False, False

        if board2d[row][column-1] == color:
            immediate[1][0] = False
        if board2d[row][column+1] == color:
            immediate[1][2] = False
        if board2d[row+1][column-1] == color:
            immediate[2][0] = False
        if board2d[row+1][column] == color:
            immediate[2][1] = False
        if board2d[row+1][column+1] == color:
            immediate[2][2] = False
        
    else: #row == 7
        (immediate[2][0], immediate[2][1], immediate[2][2]) = False, False, False
        
        if board2d[row-1][column-1] == color:
            immediate[0][0] = False
        if board2d[row-1][column] == color:
            immediate[0][1] = False
        if board2d[row-1][column+1] == color:
            immediate[0][2] = False
        if board2d[row][column-1] == color:
            immediate[1][0] = False
        if board2d[row][column+1] == color:
            immediate[1][2] = False

    global immediate_global
    immediate_global = immediate

    if not immediate[0][0] or not immediate[0][1] or not immediate[0][2] or not immediate[1][0] or not immediate[1][2] or not immediate[2][0] or not immediate[2][1] or not immediate[2][2]:
        return True #returns true if at least one side is good
    else:
        return False


def scan_legal(row, column, color):
    """determins wheter scan is legal"""

    global immediate_global
    global board2d
    global scan_global

    same_color = False
    scan = [[False,False,False],
            [False,None,False],
            [False,False,False]]
    
    if color=="black":
        opposite = -1
        same = 1
    else:
        opposite = 1
        same = -1
        
    if not immediate_global[0][0]:
    
        flip_one = False
        if row >= column:
            ranger = range(1, column+1)
        else:
            ranger = range(1, row+1)
            
        for i in ranger:
            if board2d[row-i][column-i] == 0:
                break
            if board2d[row-i][column-i] == opposite:
                flip_one = True
            if board2d[row-i][column-i] == same and flip_one:
                same_color = True
                scan[0][0] = True
                break

        
    if not immediate_global[0][1]:

        flip_two = False
        for i in range(1, row+1):
            if board2d[row-i][column] == 0:
                break
            if board2d[row-i][column] == opposite:
                flip_two = True
            if board2d[row-i][column] == same and flip_two:
                same_color = True
                scan[0][1] = True
                break

    if not immediate_global[0][2]:
  
        flip_three = False
        if row + column <= 7:
            ranger = range(1, row+1)
        else:
            ranger = range(1, 8-column)
            
        for i in ranger:
            if board2d[row-i][column+i] == 0:
                break
            if board2d[row-i][column+i] == opposite:
                flip_three = True
            if board2d[row-i][column+i] == same and flip_three:
                same_color = True
                scan[0][2] = True
                break

        
    if not immediate_global[1][0]:

        flip_four = False
        for i in range(1, column+1):
            if board2d[row][column-i] == 0:
                break
            if board2d[row][column-i] == opposite:
                flip_four = True
            if board2d[row][column-i] == same and flip_four:
                same_color = True
                scan[1][0] = True
                break
        
    if not immediate_global[1][2]:

        flip_five = False
        for i in range(1, 8-column):
            if board2d[row][column+i] == 0:
                break
            if board2d[row][column+i] == opposite:
                flip_five = True
            if board2d[row][column+i] == same and flip_five:
                same_color = True
                scan[1][2] = True
                break
        
    if not immediate_global[2][0]:
        flip_six = False
        if row + column <= 7:
            ranger = range(1, column+1)
        else:
            ranger = range(1, 8-row)
            
        for i in ranger:
            if board2d[row+i][column-i] == 0:
                break
            if board2d[row+i][column-i] == opposite:
                flip_six = True
            if board2d[row+i][column-i] == same and flip_six:
                same_color = True
                scan[2][0] = True
                break

        
    if not immediate_global[2][1]:

        flip_seven = False
        for i in range(1, 8-row):
            if board2d[row+i][column] == 0:
                break
            if board2d[row+i][column] == opposite:
                flip_seven = True
            if board2d[row+i][column] == same and flip_seven:
                same_color = True
                scan[2][1] = True
                break
                
    if not immediate_global[2][2]:

        flip_eight = False
        if row >= column:
            ranger = range(1, 8-row)
        else:
            ranger = range(1, 8-column)
            
        for i in ranger:
            if board2d[row+i][column+i] == 0:
                break
            if board2d[row+i][column+i] == opposite:
                flip_eight = True
            if board2d[row+i][column+i] == same and flip_eight:
                same_color = True
                scan[2][2] = True
                break
    
                    
    scan_global = scan
    return same_color


def legal(row, column, color):
    """determines whether a move is legal"""

    if not immediate_legal(row, column, color):
        return False
    elif not scan_legal(row, column, color):
        return False
    else:
        return True

def change2d(row, column):
    """changes 2d board, where it is easier to flip right pieces"""

    global black
    global board2d
    global scan_global
    
    if black:
        board2d[row][column] = 1
    else:
        board2d[row][column] = -1

    if scan_global[0][0]:
        if row >= column:
            ranger = range(1, column)
        else:
            ranger = range(1,row)
            
        for i in ranger:
            if (black and board2d[row-i][column-i] == 1) or (not black and board2d[row-i][column-i] == -1):
                break
            else:
                board2d[row-i][column-i] *= -1


    if scan_global[0][1]:
            for i in range(1,row):
                if (black and board2d[row-i][column] == 1) or (not black and board2d[row-i][column] == -1):
                    break
                else:
                    board2d[row-i][column] *= -1

    if scan_global[0][2]:
        if row + column <= 7:
            ranger = range(1, row+1)
        else:
            ranger = range(1, 8-column)
            
        for i in ranger:
            if (black and board2d[row-i][column+i] == 1) or (not black and board2d[row-i][column+i] == -1):
                break
            else:
                board2d[row-i][column+i] *= -1


    if scan_global[1][0]:
            for i in range(1,column):
                if (black and board2d[row][column-i] == 1) or (not black and board2d[row][column-i] == -1):
                    break
                else:
                    board2d[row][column-i] *= -1
                    
    if scan_global[1][2]:
            for i in range(1,8-column):
                if (black and board2d[row][column+i] == 1) or (not black and board2d[row][column+i] == -1):
                    break
                else:
                    board2d[row][column+i] *= -1
                    
    if scan_global[2][0]:
        if row + column <= 7:
            ranger = range(1, column+1)
        else:
            ranger = range(1, 8-row)
                
        for i in ranger:
            if (black and board2d[row+i][column-i] == 1) or (not black and board2d[row+i][column-i] == -1):
                break
            else:
                board2d[row+i][column-i] *= -1
        
    if scan_global[2][1]:
            for i in range(1,8-row):
                if (black and board2d[row+i][column] == 1) or (not black and board2d[row+i][column] == -1):
                    break
                else:
                    board2d[row+i][column] *= -1

    if scan_global[2][2]:
        if row >= column:
            ranger = range(1, 8-row)
        else:
            ranger = range(1, 8-column)
            
        for i in ranger:
            if (black and board2d[row+i][column+i] == 1) or (not black and board2d[row+i][column+i] == -1):
                break
            else:
                board2d[row+i][column+i] *= -1

    
#makes player change
def blackwhite():
    """Changes bottom indication and turn from black player to white"""
    
    person1.config(font="Arial 14")
    person2.config(font="Arial 18 bold")

    global black
    black = False


def whiteblack():
    """Changes bottom indication and turn from white player to black"""
    
    person1.config(font="Arial 18 bold")
    person2.config(font="Arial 14")

    global black
    black = True


#main turn function
def turn(event):
    """this is the start of each turn, after the setup"""

    column = event.x//100
    row = event.y//100

    global black
    global board2d

    if black:
        if legal(row, column, "black"):
            change2d(row, column)
            flip_pieces()
            blackwhite()
            
        # do the for loop check here
        # switch back if it fails
        # and pop up a messagebox

            no_legal = True
            for i in range(8):
                for t in range(8):
                    if board2d[i][t] == 0 and legal(i,t,"white"):
                        no_legal = False
                        break

            if no_legal and not done():
                messagebox.showinfo("No Legal Moves","White has no legal moves! Black goes again.")
                whiteblack()

    else:
        if legal(row, column, "white"):
            change2d(row, column)
            flip_pieces()
            whiteblack()
                      
            no_legal = True
            for i in range(8):
                for t in range(8):
                    if board2d[i][t] == 0 and legal(i,t,"black"):
                        no_legal = False
                        break

            if no_legal and not done():
                messagebox.showinfo("No Legal Moves","Black has no legal moves! White goes again.")
                blackwhite()
             
    if done():
        winner()

def flip_pieces():
    """changes shown board to reflect 2d board"""
    
    global board2d
    for i in range(8):
        for t in range(8):
        
            if board2d[i][t] == -1:
                tk.Label(image=w_piece, borderwidth=0).grid(row=i, column=t)
            if board2d[i][t] == 1:
                tk.Label(image=b_piece, borderwidth=0).grid(row=i, column=t)


#the globals, set and awaiting takeoff

black = True

board2d = [[0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,-1,1,0,0,0],
           [0,0,0,1,-1,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0]]

immediate_global = [[True,True,True],
                    [True,None,True],
                    [True,True,True]]

scan_global = [[False,False,False],
               [False,None,False],
               [False,False,False]]
#the set-ups

#materials
main_window = tk.Tk()
main_window.title("Reversi")

board = tk.PhotoImage(file="gif-board.gif")
b_piece = tk.PhotoImage(file="gif-black.gif")
w_piece = tk.PhotoImage(file="gif-white.gif")


#bottom grid framework
for i in range(8):
    for t in range(8):
        tk.Frame(height=100, width=100).grid(row=i, column=t)


#board overlay
bg_image = tk.Label(main_window, image=board, borderwidth=0)
bg_image.grid(row=0, column=0, rowspan=8, columnspan=8)
bg_image.bind("<Button-1>", turn)

tk.Label(image=w_piece, borderwidth=0).grid(row=3, column=3)
tk.Label(image=b_piece, borderwidth=0).grid(row=3, column=4)
tk.Label(image=b_piece, borderwidth=0).grid(row=4, column=3)
tk.Label(image=w_piece, borderwidth=0).grid(row=4, column=4)


#whose turn?
person1 = tk.Label(main_window, text="Black", height=2, font="Arial 18 bold")
person1.grid(row=8, column=1, columnspan=2)

person2 = tk.Label(main_window, text="White", height=2, font="Arial 14")
person2.grid(row=8, column=5, columnspan=2)

#go!

main_window.mainloop()

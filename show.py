from tkinter import * 
from clear import clear_data
import settings
from constants import *

def show_matrix(x, y, matrix, rows, cols, pax, pay):
    '''Organize in a grid each widget inside the matrix.'''
    reset = y  
    for row in range(rows):
        for col in range(cols):
            matrix[row][col].grid(row=x, column=y, padx=pax, pady=pay)
            y += 1
        y = reset
        x += 1

def result(values, var, frame, res):
    '''Show the result in the screen.'''
    clear_data(res)
    var.set("") 
    
    if settings.canvas != object:
        settings.canvas.get_tk_widget().destroy()

    x, y = 2, 16
    #Determinate what is the value and print in the screen with it's format
    if type(values) is int:
        res.append([Label(frame, text=str(values), font="Consolas 16", fg=WHITE, bg=DARKEST_PURPLE)])
        res[0][0].grid(row=x, column=y, padx=10, pady=10)
        return None
    else:
        #Store the value in version of str for blit like a label on the screen
        for row in values:
            res.append([Label(frame, text=str(col), font="Consolas 16", fg=WHITE, bg=DARKEST_PURPLE)for col in row]) 
        return show_matrix(x, y, res, len(res), len(res[0]), 10, 5)

def warning(error, notice, var, res):
    '''Generate notices when something is wrong with the inputs'''
    clear_data(res)
    var.set(error)
    notice.grid(row=2, column=18, padx=10, pady=10, rowspan=5)

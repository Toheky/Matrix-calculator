from tkinter import * 
from show import * 
from clear import clear_data

def create_box_txt(root, rows, cols, x, y, matrix, values, var):
    '''Create the txt box like a matrix.'''
    clear_data(matrix)
    var.set("")
    values.clear()

    for row in range(rows):
        box, val = [], []
        for col in range(cols):
            a = IntVar()
            box.append(Entry(root, width=3, fg="#fff", bg="#121211", bd=0, font="Consolas 14", relief="ridge", justify="center",highlightthickness=2, textvariable=a))
            val.append(a)
        matrix.append(box)
        values.append(val)

    show_matrix(x, y, matrix, rows, cols, 5, 5)

def create_matrix(root, rows, cols, matrix):
    '''Create the widgets and store in the matrix.'''
    for row in range(rows):
        box = []
        for col in range(cols):
            a = IntVar()
            box.append(Entry(root, width=3, fg="#fff", bg="#121211", bd=0, font="Consolas 14", relief="ridge", justify="center",highlightthickness=2, textvariable=a))
        matrix.append(box)
    return matrix

def create_img(files):
    '''Create photo object for each button'''
    return PhotoImage(file="imgs/"+files)

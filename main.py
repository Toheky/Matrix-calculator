'''
Author: Juan David Jaimes Claros

Matrix calculator

The programn is a matrix calculator for does basic operations as the inverse, determinant, product, sum, subtraction and among others. 

The modules that I used were tkinter for the interface and widgets, some functions of os.path for get the path of the images, pyperclip for have access to the clipboard, matplotlib for representate with a heatmap the data.
'''

from create_widgets import create_img
from matplotlib.figure import Figure 
from os.path import isfile, join
from os.path import dirname
from operations import * 
from settings import * 
from constants import * 
from tkinter import ttk
from os import listdir
from tkinter import * 

def frame_configuration(canvas):
    '''Include all the width of the screen for the horizontal bar.'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def main():
    '''Handle the interface and initializate the operations.'''

    #Initializate global variables
    settings.init()

    #Creation of nested lists
    matrix_a, values_a, matrix_b, values_b, res = [[] for _ in range(5)]

    #Screen settings
    root = Tk()
    root.geometry("1120x500")
    root.title("Matrix calculator")
    root.resizable(False, False)  
    root.configure(bg=DARKEST_PURPLE)

    #Logo
    logo = PhotoImage(file="logo.png")
    root.iconphoto(False, logo)

    #Input variables for the size
    entries_vars = [rows_a, cols_a, rows_b, cols_b] = [IntVar() for _ in range(4)]
    res = []

    #Entry variables
    sca_value_a, sca_value_b = IntVar(), IntVar()

    #Styles for the horizontal bar
    style = ttk.Style()
    style.theme_use('clam')

    style.configure("Horizontal.TScrollbar", 
                    gripcount=0, 
                    background=DARK_PURPLE, 
                    darkcolor=DARK_PURPLE, 
                    lightcolor=DARKEST_PURPLE, 
                    troughcolor=DARKEST_PURPLE, 
                    bordercolor=DARKEST_PURPLE, 
                    arrowcolor=DARKEST_PURPLE)

    #Import imgs from path
    path = dirname(__file__) + "\\imgs\\"
    images = [create_img(f) for f in listdir(path) if isfile(join(path, f))]

    #Decorations results
    bg_result = Canvas(root, highlightthickness=2, highlightbackground=DARKEST_PURPLE, bg=DARKEST_PURPLE, height=452, width=390)
    bg_result.place(x=700 , y=25)
    bg_result.create_image(0, 0, image=images[1], anchor=NW)

    #Organize the result window
    result_frame = Frame(root)
    result_frame.grid(row=1, column=16, columnspan=2, rowspan=7)

    canvas = Canvas(result_frame, bg=DARKEST_PURPLE, highlightthickness=1, highlightbackground=DARKEST_PURPLE)
    frame = Frame(canvas, bg=DARKEST_PURPLE)
    hsb = ttk.Scrollbar(result_frame, orient="horizontal", command=canvas.xview)
    canvas.configure(xscrollcommand=hsb.set)

    hsb.pack(side="top", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0,0), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: frame_configuration(canvas))

    #Notice label and variable for warnings 
    notice_var = StringVar()
    notice = Label(frame, textvariable=notice_var, font="Consolas 16", fg=WHITE , bg=DARKEST_PURPLE, justify="center")

    #Empty labels
    Label(root, text="  ", fg=DARKEST_PURPLE, bg=DARKEST_PURPLE).grid(row=7, column=6, padx=10, pady=10)
    Label(root, text="  ", fg=DARKEST_PURPLE, bg=DARKEST_PURPLE).grid(row=7, column=14, padx=10, pady=10)

    #Decorations matrix A
    bg_matrix_a = Canvas(root, highlightthickness=2, highlightbackground=DARKEST_PURPLE, bg=DARKEST_PURPLE, height=455, width=305)
    bg_matrix_a.place(x=5 , y=25)
    bg_matrix_a.create_image(0, 0, image=images[0], anchor=NW)

    #Decorations matrix B
    bg_matrix_b = Canvas(root, highlightthickness=2, highlightbackground=DARKEST_PURPLE, bg=DARKEST_PURPLE, height=455, width=305)
    bg_matrix_b.place(x=365 , y=25)   
    bg_matrix_b.create_image(0, 0, image=images[0], anchor=NW)

    #Titles
    title_a = Label(root, text="Matrix A", font="Consolas 17 bold", fg=WHITE, bg=DARKEST_PURPLE)
    title_a.grid(row=0, column=0, padx=10, pady=10, columnspan=6)

    title_b = Label(root, text="Matrix B", font="Consolas 17 bold", fg=WHITE, bg=DARKEST_PURPLE)
    title_b.grid(row=0, column=7, padx=10, pady=10, columnspan=6)

    #Entry rows and columns matrix A and entry rows and columns matrix B
    entries = [entry_rows_a, entry_cols_a, entry_rows_b, entry_cols_b] = [Entry(root, width=3, fg=WHITE, bg="#121211", bd=0, font="Consolas 14", relief="ridge", highlightthickness=2, textvariable=entries_vars[i]) for i in range(4)]

    for entry in entries:
        entry.config(highlightbackground=BLUE, highlightcolor=GOLD)
    
    #Position of text box matrix A
    entry_rows_a.grid(row=1, column=0, padx=10, pady=10)
    entry_cols_a.grid(row=1, column=1, padx=10, pady=10)

        #Position of text box matrix B
    entry_rows_b.grid(row=1, column=7, padx=10, pady=10)
    entry_cols_b.grid(row=1, column=8, padx=10, pady=10)

    #Enter, copy and paste buttons
    enter_a = Button(root, width=30, image=images[4], highlightthicknes=0, bd=0, activebackground=PINK, fg=WHITE, command=lambda: enter(root, rows_a, cols_a, entry_rows_a, entry_cols_a, 2, 0, matrix_a, values_a, notice, notice_var, frame, res))
    enter_a.grid(row=1, column=2, padx=10)

    copy_button = Button(root, width=30, image=images[2], highlightthicknes=0, bd=0, activebackground=PINK, fg=WHITE, command=lambda : copy_content(matrix_a))
    copy_button.grid(row=1, column=3, padx=10, pady=10)

    paste_button = Button(root, width=30, image=images[8], highlightthicknes=0, bd=0, activebackground=PINK, fg=WHITE, command=lambda : paste_content(matrix_a, notice, notice_var, res))
    paste_button.grid(row=1, column=4, padx=10, pady=10)

    enter_b = Button(root, width=30, image=images[4], highlightthicknes=0, bd=0, activebackground=PINK, fg=WHITE, command=lambda: enter(root, rows_b, cols_b, entry_rows_b, entry_cols_b, 2, 7, matrix_b, values_b, notice, notice_var, frame, res))
    enter_b.grid(row=1, column=9, padx=10)

    copy_button = Button(root, width=30, image=images[2], highlightthicknes=0, bd=0, activebackground=PINK, fg=WHITE, command=lambda : copy_content(matrix_b))
    copy_button.grid(row=1, column=10, padx=10, pady=10)

    paste_button = Button(root, width=30, image=images[8], highlightthicknes=0, bd=0, activebackground=PINK, fg=WHITE, command=lambda : paste_content(matrix_b, notice, notice_var, res))
    paste_button.grid(row=1, column=11, padx=10, pady=10)

    #Buttons for operations between matrix
    sum_button = Button(root, width=30, image=images[11], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: addition(get_values(matrix_a, values_a, notice, notice_var, res), get_values(matrix_b, values_b, notice, notice_var, res), notice, notice_var, frame, res))
    sum_button.grid(row=2, column=6, padx=10, pady=10)

    multi_button = Button(root, width=30, image=images[7], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: multiplication(get_values(matrix_a, values_a, notice, notice_var, res), get_values(matrix_b, values_b, notice, notice_var, res), notice, notice_var, frame, res))
    multi_button.grid(row=3, column=6, padx=10, pady=10)

    sub_button = Button(root, width=30, image=images[10], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: subtraction(get_values(matrix_a, values_a, notice, notice_var, res), get_values(matrix_b, values_b, notice, notice_var, res), notice, notice_var, frame, res))
    sub_button.grid(row=4, column=6, padx=10, pady=10)

    swap_button = Button(root, width=30, image=images[14], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: swap_matrix(root, entries, entries_vars, matrix_a, matrix_b, values_a, values_b, notice, notice_var, frame, res))
    swap_button.grid(row=5, column=6, padx=10, pady=10)

    equ_sys_button = Button(root, width=30, image=images[5], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: linear_equations(get_values(matrix_a, values_a, notice, notice_var, res), get_values(matrix_b, values_b, notice, notice_var, res), notice, notice_var, frame, res))
    equ_sys_button.grid(row=6, column=6, padx=10, pady=10)

    #Buttons of operations -- Matrix A
    inv_button = Button(root, width=30, image=images[6], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: inverse(get_values(matrix_a, values_a, notice, notice_var, res), get_identity(values_a), notice, notice_var, frame, res))
    inv_button.grid(row=8, column=0, padx=10, pady=10)

    det_button = Button(root, width=30, image=images[3], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: determinant(get_values(matrix_a, values_a, notice, notice_var, res), notice, notice_var, frame, res))
    det_button.grid(row=8, column=1, padx=10, pady=10)

    trans_button = Button(root, width=30, image=images[15], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: tranpose(get_values(matrix_a, values_a, notice, notice_var, res), notice, notice_var, frame, res))
    trans_button.grid(row=8, column=2, padx=10, pady=10)

    sum_row_button = Button(root, width=30, image=images[13], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: add_row(get_values(matrix_a, values_a, notice, notice_var, res), sum_row_input_a, notice, notice_var, frame, res))
    sum_row_button.grid(row=8, column=3, padx=10, pady=10)

    sum_row_input_a = Entry(root, width=3, fg="#fff", bg="#121211", bd=0, font="Consolas", relief="ridge", highlightthickness=2)
    sum_row_input_a.grid(row=9, column=3)

    sum_col_button = Button(root, width=30, image=images[12], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: add_col(get_values(matrix_a, values_a, notice, notice_var, res), sum_col_input_a, notice, notice_var, frame, res))
    sum_col_button.grid(row=8, column=4, padx=10, pady=10)

    sum_col_input_a = Entry(root, width=3, fg="#fff", bg="#121211", bd=0, font="Consolas", relief="ridge", highlightthickness=2)
    sum_col_input_a.grid(row=9, column=4)

    sca_button = Button(root, width=30, image=images[9], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: scalar(get_values(matrix_a, values_a, notice, notice_var, res), sca_value_a, sca_input_a, notice, notice_var, frame, res))
    sca_button.grid(row=8, column=5, padx=10, pady=10)

    sca_input_a = Entry(root, width=3, fg="#fff", bg="#121211", bd=0, font="Consolas", relief="ridge", highlightthickness=2)
    sca_input_a.insert(END, 1)
    sca_input_a.grid(row=9, column=5)

    #Buttons of operations -- Matrix B
    inv_button = Button(root, width=30, image=images[6], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: inverse(get_values(matrix_b, values_b, notice, notice_var, res), get_identity(values_b), notice, notice_var, frame, res))
    inv_button.grid(row=8, column=7, padx=10, pady=10)

    det_button = Button(root, width=30, image=images[3], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: determinant(get_values(matrix_b, values_b, notice, notice_var, res), notice, notice_var, frame, res))
    det_button.grid(row=8, column=8, padx=10, pady=10)

    trans_button = Button(root, width=30, image=images[15], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: tranpose(get_values(matrix_b, values_b, notice, notice_var, res), notice, notice_var, frame, res))
    trans_button.grid(row=8, column=9, padx=10, pady=10)

    sum_row_button = Button(root, width=30, image=images[13], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: add_row(get_values(matrix_b, values_b, notice, notice_var, res), sum_row_input_b, notice, notice_var, frame, res))
    sum_row_button.grid(row=8, column=10, padx=10, pady=10)

    sum_row_input_b = Entry(root, width=3, fg="#fff", bg="#121211", bd=0, font="Consolas", relief="ridge", highlightthickness=2)
    sum_row_input_b.grid(row=9, column=10)

    sum_col_button = Button(root, width=30, image=images[12], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: add_col(get_values(matrix_b, values_b, values_b, notice, notice_var, res), sum_col_input_b, notice, notice_var, frame, res))
    sum_col_button.grid(row=8, column=11, padx=10, pady=10)

    sum_col_input_b = Entry(root, width=3, fg="#fff", bg="#121211", bd=0, font="Consolas", relief="ridge", highlightthickness=2)
    sum_col_input_b.grid(row=9, column=11)

    sca_button = Button(root, width=30, image=images[9], highlightthicknes=0, bd=0, activebackground=BLUE, fg=WHITE, command=lambda: scalar(get_values(matrix_b, values_b, notice, notice_var, res), sca_value_b, sca_input_b, notice, notice_var, frame, res))
    sca_button.grid(row=8, column=12, padx=10, pady=10)

    sca_input_b = Entry(root, width=3, fg="#fff", bg="#121211", bd=0, font="Consolas", relief="ridge", highlightthickness=2)
    sca_input_b.insert(END, 1)
    sca_input_b.grid(row=9, column=12)

    #Buttons result
    copy_button = Button(root, width=30, image=images[2], highlightthicknes=0, bd=0, activebackground=PINK, fg=WHITE, command=lambda: copy_content(res))
    copy_button.grid(row=8, column=16, padx=20, pady=10)

    heatmap_button = Button(root, width=30, image=images[-1], highlightthicknes=0, bd=0, activebackground=PINK, fg=WHITE, command=lambda: graph(res, notice, notice_var))
    heatmap_button.grid(row=8, column=17, padx=20, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()

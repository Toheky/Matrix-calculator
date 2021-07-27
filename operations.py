from create_widgets import create_box_txt 
from show import result, warning
from clear import clear_data
from tkinter import Entry 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure 
from constants import DARKEST_PURPLE
import settings
import matplotlib
import pyperclip

def enter(root, rows, cols, entry_rows, entry_cols, x, y, matrix, values, notice, var, frame, res):
    '''Take the size of the matrix.'''
    try:
        rows, cols = int(entry_rows.get()), int(entry_cols.get())
    except:
        return warning("The entry have to be\nonly a number", notice, var, res)
    if rows not in [1,2,3,4,5,6] or cols not in [1,2,3,4,5,6]:
        return warning("Entry is not in\nthe range of numbers\n[1,2,3,4,5,6]", notice, var, res)
    return create_box_txt(root, rows, cols, x, y, matrix, values, var)

##### OPERATIONS BETWEEN MATRIX ######

def addition(values_a, values_b, notice, var, frame, res):
    '''Addition operation between matrix.'''
    try:
        if (len(values_a) != len(values_b)) or (len(values_a[0]) != len(values_b[0])):
            warning("Please insert two\nmatrix with the same\nnumber of rows and\ncolumns", notice, var, res)
        else:
            outcome = []
            for row in range(len(values_a)):
                temp = []
                for col in range(len(values_a[row])):
                    temp.append(values_a[row][col] + values_b[row][col])
                outcome.append(temp)
            return result(outcome, var, frame, res)
    except:
        return warning("Please insert two\nmatrix for does\n the operation.", notice, var, res)

def multiplication(values_a, values_b, notice, var, frame, res):
    '''Product operation between matrix.'''
    try:
        if len(values_a) != len(values_b[0]):
            warning("Please insert the same\nnumber of rows for the\nfirst matrix and the\nsame number of columns\nfor the second matrix.", notice, frame)
        else:
            outcome = [[0]*len(values_b) for row in values_a]
            for i in range(len(values_a)):
                for j in range(len(values_b[0])):
                    for k in range(len(values_b)):
                        outcome[i][j] = values_a[i][k] * values_b[k][j]
            return result(outcome, var, frame, res)
    except:
        return warning("Please insert two\nmatrix for does\n the operation.", notice, var, res)

def subtraction(values_a, values_b, notice, var, frame, res):
    '''Substraction operation between matrix.'''
    try:
        for row in range(len(values_b)):
            for col in range(len(values_b[row])):
                values_b[row][col] = -values_b[row][col]
        return addition(values_a, values_b, notice, var, frame, res)
    except:
        return warning("Please insert two\nmatrix for does\n the operation.", notice, var, res)

def swap(a, b):
    '''Exchange the entrys widgets'''
    temp = a.get()
    a.delete(0,"end")
    a.insert(0,b.get()) 
    b.delete(0,"end")
    b.insert(0,temp)

def swap_matrix(root, entries, entries_vars, matrix_a, matrix_b, values_a, values_b, notice, notice_var, frame, res):
    '''Swap the matrix in size, widgets and values'''

    #Exchange numbers of rows and cols
    swap(entries[0],entries[2])
    swap(entries[1],entries[3])

    #Get values
    entries_vars[0], entries_vars[1] = int(entries[0].get()), int(entries[1].get())
    entries_vars[2], entries_vars[3] = int(entries[2].get()), int(entries[3].get())

    clear_data(matrix_a)
    clear_data(matrix_b)

    #Create matrix
    enter(root, entries_vars[2], entries_vars[3], entries[2], entries[3], 2, 7, matrix_b, values_b, notice, notice_var, frame, res)
    enter(root, entries_vars[0], entries_vars[1], entries[0], entries[1], 2, 0, matrix_a, values_a, notice, notice_var, frame, res)
    
def triangle(a, start, end, add):
    '''Get upper and lower triangle in the matrix'''
    for i in range(start, end):
        pivot = a[i][i]
        start2, end2 = i+add, end+add
        if add == 0:
            end2,start2 = start2, 0 
        for row in range(start2, end2):
            x = -(a[row][i])/pivot
            sub = [a[i][col]*x for col in range(len(a[i]))]
            for col in range(len(a[row])):
                a[row][col] = a[row][col] + sub[col]
    return a

def linear_equations(values_a, values_b, notice, var, frame, res):
    '''Solve system of equations through matrix.'''
    try:
        a = values_a.copy()

        if len(values_b[0]) > 1:
            return warning("Please insert a\ncorrect vector", notice, var, res)

        vec = [num[0] for num in values_b]
        for row in range(len(a)):
            a[row].append(vec[row])

        a = triangle(a, 0, len(a)-1, 1)
        
        for row in range(len(a)):
            for col in range(len(a[row])): 
                if col != row:
                    a[row][col] = a[row][col] / a[row][row]
            a[row][row] = 1.0

        a = triangle(a, 1, len(a), 0)

        outcome = [[a[row][-1]] for row in range(len(a))]
        return result(outcome, var, frame, res)
    except:
        warning("Please insert one\nmatrix and one vector \nfor does the\noperation.", notice, var, res)

##### INDIVIDUAL OPERATIONS #####

def get_identity(values):
    '''Get the identity matrix of a matrix.'''
    identity = [[0 for i in values] for row in values]
    for row in range(len(identity)):
        identity[row][row] = 1
    return identity

def inverse(values, identity, notice, var, frame, res):
    '''Inverse operation.'''
    try:
        matrix = values.copy()

        if determinant(matrix, notice, var, frame, res) == 0:
            return warning("Is a singular matrix", notice, var, res)

        if len(matrix) != len(matrix[0]):
            return warning("Have to be a square\nmatrix", notice, var, res)

        for row in range(len(matrix)):
            matrix[row] = matrix[row] + identity[row]

        matrix = triangle(matrix, 0, len(matrix)-1, 1)

        for row in range(len(matrix)):
            for col in range(len(matrix[row])): 
                if col != row:
                    matrix[row][col] = matrix[row][col] / matrix[row][row]
            matrix[row][row] = 1.0

        matrix = triangle(matrix, 1, len(matrix), 0)

        #Get only the inverse values
        outcome = [matrix[row][1+(len(matrix)//2):] for row in range(len(matrix))]
        return result(outcome, var, frame, res)
    except:
        return warning("Please insert one\nmatrix", notice, var, res)

def determinant(matrix, notice, var, frame, res):
    '''Determinan operation.'''
    try:
        if len(matrix) != len(matrix[0]):
            return warning("Have to be a square\nmatrix", notice, var, res)
        if len(matrix) == 1:
            return matrix[0][0]
        outcome = 0
        for col in range(len(matrix[0])):
            det = []
            for row in range(1, len(matrix)):
                temp = []
                for col2 in range(len(matrix[row])):
                    if col2 != col:
                        temp.append(matrix[row][col2])
                det.append(temp)
            s = -1 if col % 2 == 1 else 1
            outcome += s* matrix[0][col] * determinant(det, notice, var, frame, res)
        result(outcome, var, frame, res)
        return outcome
    except:
        return warning("Please insert one\nmatrix", notice, var, res)

def scalar(values, sca_value, sca_input, notice, var, frame, res):
    '''Scalar operation.'''
    try:
        sca_value = float(sca_input.get())
        for row in range(len(values)):
            for col in range(len(values[row])):
                values[row][col] = float("{0:.2f}".format(values[row][col] * sca_value))
        return result(values, var, frame, res)
    except:
        return warning("Please insert one\nvalue as a number", notice, var, res)

def add_row(values, row_input, notice, var, frame, res):
    '''Sum a row through it's index.'''
    try:
        n = int(row_input.get())
        if n not in [i for i in range(len(values[0]))]:
            return warning(f"The row is not\nin the range\n {[i for i in range(len(values[0]))]}", notice, var, res)
        cnt = 0
        for i in values[n]:
            cnt += i
        return result(cnt, var, frame, res)
    except:
        return warning("Please insert one\nmatrix", notice, var, res)

def add_col(values, col_input, notice, var, frame, res):
    '''Sum a column through it's index.'''
    try:
        n = int(col_input.get())
        if n not in [i for i in range(len(values[0]))]:
            return warning(f"The column is not\nin the range\n {[i for i in range(len(values[0]))]}", notice, var, res)
        cnt = 0
        for i in range(len(values)):
            cnt += values[i][n]
        return result(cnt, var, frame, res)
    except:
        return warning("Please insert one\nmatrix", notice, var, res)

def tranpose(values, notice, var, frame, res):
    '''Tranpose operation.'''
    try:
        values = [[row[col] for row in values] for col in range(len(values[0]))]
        return result(values, var, frame, res)
    except:
        return warning("Please insert one\nmatrix", notice, var, res) 

def copy_content(matrix):
    '''Copy the matrix content in the clipboard.'''
    txt = ""
    for row in matrix:
        for wid in row:
            if isinstance(wid, Entry):
                txt += wid.get()+" "
            else:
                txt += wid.cget("text")+" "
        txt += "\n"
    pyperclip.copy(txt)

def paste_content(matrix, notice, var, res):
    '''Paste to the matrix the content in the clipboard.'''
    paste = [i for i in pyperclip.paste().split()]
    values = [[num for num in paste[row*len(matrix[0]):(row+1)*len(matrix[0])]] for row in range(len(matrix))]

    #Delete default values in the entries and assign the old swap values 
    for row in range(len(matrix)):
        for entry in range(len(values[row])):
            matrix[row][entry].delete(0,"end")
            if values[row][entry].isdigit():
                matrix[row][entry].insert(0, values[row][entry])
            else:
                return warning("The entry have to be\na number", notice, var, res)

def graph(res, notice, var):
    '''Generate a heatmap on the screen.'''
    if not res: 
        return warning("Not result for\nshow", notice, var, res)

    values = [[float(col.cget("text")) for col in row] for row in res]

    fig = Figure(figsize=(3.7,2.5), dpi=100, facecolor=DARKEST_PURPLE, edgecolor=DARKEST_PURPLE)
    a = fig.add_subplot(1, 1 ,1)
    a.tick_params(axis='x', colors='white')
    a.tick_params(axis='y', colors='white')
    a.matshow(values)

    settings.canvas = FigureCanvasTkAgg(fig)
    settings.canvas.draw
    settings.canvas.get_tk_widget().grid(row=1, column=16, columnspan=2, rowspan=7)

def get_values(matrix, values, notice, var, res):
    '''Extract the values of each txt box input.'''
    for row in range(len(matrix)):
        for box in range(len(matrix[row])):
            try:
                values[row][box] = int(matrix[row][box].get())
            except:
                return warning("The entry have to be\nonly a number", notice, var, res)
    return values

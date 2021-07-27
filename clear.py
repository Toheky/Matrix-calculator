def clear_data(matrix):
    '''Remove the remains widgets in the screen and clear matrix.'''
    [[box.destroy() for box in row] for row in matrix] 
    matrix.clear()
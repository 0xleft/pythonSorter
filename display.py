import numpy as np
import random
import tkinter.messagebox
from tkinter import *


lenghtOfArray = 30 # define how long you want your array to be
arr = np.arange(lenghtOfArray) # arr = np.arange(lenghtOfArray+1 if you want to include last number)
n = len(arr)


# shuffle the numbers in the array
# (i didnt want to used random.shuffle())

def shuffler (arr, n):
     
    # We will Start from the last element
    # and swap one by one.
    for i in range(n-1,0,-1):
         
        # Pick a random index from 0 to i
        j = random.randint(0,i+1)
         
        # Swap arr[i] with the element at random index
        arr[i],arr[j] = arr[j],arr[i]
    return arr


shuffledArray = shuffler(arr, n) # first argument for array and second for array length

win=tkinter.Tk()
win.title("Shuffler")
win.geometry("400x400")


can=Canvas(win, width=3000, height=3000) # canvas size
can.configure(bg="Grey")


width = 50 #width of the collumn
rectLastX = 0
# for every number in array make a rectangle the height of the number in the array * 10
for i in range(n):
    case = shuffledArray[i]
   
    if case !=0: # zeroes will have a height of 0 so i dont want to display them
        rectangle=can.create_rectangle(rectLastX+width, 0, rectLastX, case*10,fill='green')
        rectLastX += width
        can.create_text(rectLastX-width/2, case*10,text=case, fill="Black")
        can.pack()
# can.create_text(300, 500,text=shuffledArray, fill="Black") <--- displays array on the canvas for trouble shooting     

win.mainloop()
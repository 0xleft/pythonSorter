from turtle import width
import numpy as np
import random
import tkinter.messagebox
from tkinter import *


arr = np.arange(20)
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


#shuffledArray = shuffler(arr, n)

win=tkinter.Tk()
win.title("Shuffler")
win.geometry("400x400")


can=Canvas(win, width=3000, height=3000)

#width of the collum
width = 50
rectLastX = 0
#usedNumbers = []
# for every number in array make a rectangle the height of the number in the array * 10
for i in (arr):
    i = random.choice(arr)
    #i.append(usedNumbers)
        #if i not in usedNumbers:

    if i !=0:
        rectangle=can.create_rectangle(rectLastX+width, 0, rectLastX, i*10,fill='green')
        rectLastX += width
        can.create_text(rectLastX-width/2, i*10,text=i, fill="Black")
        can.pack()

win.mainloop()
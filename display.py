from array import array
import numpy as np
import random
import tkinter.messagebox
from tkinter import *
import time
import math

lenghtOfArray = 31 # define how long you want your array to be
startOfArray = 0
arr = np.arange(startOfArray,lenghtOfArray,dtype=None) # arr = np.arange(lenghtOfArray+1 if you want to include last number)
n = len(arr)
print(arr)

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
win.geometry("2000x1000")


can=Canvas(win, width=3000, height=3000) # canvas size
can.configure(bg="Grey")


# find the sum of the array (used it for debugging)
def sum(array):
    sum=0
    for i in array:
        sum = sum + i
         
    return(sum)

# find minimum value of the array
def minim(array):
    p = len(array)
    min = p
    for j in range(p):
        if(min > array[j] and array[j] != 0): # leave out zeroes because we dont draw them
            min = array[j]
    return (min)
    
# find number by its index
def findIndexByNumber(array, number):
    NumberIndex = -1
    for i in range(array.size):
            if array[i] == number:
                NumberIndex = i
                break
    return(NumberIndex)


def drawingGraph(arr):
    rectangles = []
    width = 50 #width of the collumn
    rectLastX = width # distance from left top edge
    # for every number in array make a rectangle the height of the number in the array * 10
    for i in range(n):
        case = arr[i]
    
        if case !=0: # zeroes will have a height of 0 so i dont want to display them
            rectangle=can.create_rectangle(rectLastX+width, 0, rectLastX, case*10,fill='green')
            
            rectLastX += width
            can.create_text(rectLastX-width/2, case*10,text=case, fill="Black")
            can.pack()
    # can.create_text(300, 500,text=shuffledArray, fill="Black") <--- displays array on the canvas for troubleshooting

def selectionSort(shuffledArray):
    n=len(shuffledArray)
    for i in range(n):

        minNumber = minim(shuffledArray)+i
        minNumberIndex = findIndexByNumber(shuffledArray, minNumber)

        #minNumberIndex = np.where(shuffledArray == minNumber) <- couldnt make this work (help needded)
        

        print("switching index:", i, "with:", minNumber)
        shuffledArray[minNumberIndex],shuffledArray[i] = shuffledArray[i],shuffledArray[minNumberIndex]
        print(shuffledArray)
        
        #rectangle=can.create_rectangle(minNumberIndex * rectLastX+width+ rectLastX, 0, minNumberIndex * rectLastX+rectLastX, minNumber*10,fill='red')
        #can.create_text(minNumberIndex * rectLastX-width/2+ rectLastX, minNumber*10,text=minNumberIndex, fill="Black")
        #can.pack()

        

        #can.after(20, sortingAnimation)

drawingGraph(shuffledArray)
selectionSort(shuffledArray)
win.mainloop()

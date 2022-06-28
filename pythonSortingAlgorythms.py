from copy import copy
import numpy as np
import random
import tkinter
from tkinter import *
import time
import os


def selectionSortForTest(array):
    for index in range(0,array.size):
        minNumber = array[index]
        minIndex = index
        for i in range(index+1, array.size):
            if minNumber > array[i]:
                minNumber = array[i]
                minIndex = i
        array[minIndex],array[index] = array[index],array[minIndex]
    
    #print(array, "test")
    return array

#https://www.geeksforgeeks.org/shuffle-an-array-in-python/
# shuffle the numbers in the array
# (i didnt want to used random.shuffle())
def shuffler (arr):
    n = len(arr)
    # We will Start from the last element
    # and swap one by one.
    for i in range(n-1):
        # Pick a random index frozm 0 to i
        j = random.randint(0,i+1)
        # Swap arr[i] with the element at random index
        arr[i],arr[j] = arr[j],arr[i]
    #print(arr, "shuffle")
    return arr


def create_animation_window():
    win = tkinter.Tk()
    win.title("Shuffled")
    return win


def create_animation_canvas(window):
    canvas = tkinter.Canvas(window)
    canvas.configure(bg="grey")
    canvas.pack(fill="both", expand=True)
    window.geometry("2500x1000")
    return canvas


# find the sum of the array (used it for debugging)
def sum(array):
    sum=0
    for i in array:
        sum = sum + i
         
    return(sum)


def flipbool(bool):
    if bool is not True:
        bool = True
    else:
        bool = False
    return bool

#generate new array in the same array
def generateNewArray():
    generatedArray = ([])
    generatedArray = np.random.randint(1, 200, size = getCurrentValue())
    return generatedArray


# find minimum value of the array
def minim(array):
    min = len(array)
    for j in range(array.size):
        if(min > array[j] and array[j]): # leave out zeroes because we dont draw them
            min = array[j]
    return min


def getCurrentValue():
    return round(currentValue.get())


def sliderChanged(event):
    global change
    change = True
    return change


# find number by its index
def findIndexByNumber(array, number):
    if number in array:
        NumberIndex = minim(array)-1
        for i in range(np.max(array)):
                if array[i] == number:
                    NumberIndex = i
                    break
        return(NumberIndex)


def drawingGraph(array,canvas):
    width = 50
    rectLastX = 50
    canvas.delete("all")
    for i in range(array.size):
        case = array[i]
        canvas.create_rectangle(rectLastX+width, 0, rectLastX+10, case*4,fill='green')
        rectLastX += width
        canvas.create_text(rectLastX-width/2, case*4,text=case, fill="Black")
        canvas.pack()


def partition(array, low, high):
 
    # Choose the rightmost element as pivot
    pivot = array[high]

    # Pointer for greater element
    i = low - 1
    # Traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j] <= pivot:
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1

            # Swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])
        # Swap the pivot element with the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    drawingGraph(array,animation_canvas)
    animation_window.update()
    time.sleep(animation_refresh_seconds)
    
    # Return the position from where partition is done
    return i + 1

 
# Function to perform quicksort
def quickSort(array, low, high):
    if low < high:
 
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partition(array, low, high)

        # Recursive call on the left of pivot
        quickSort(array, low, pi - 1)

        # Recursive call on the right of pivot
        quickSort(array, pi + 1, high)
        return array


def animateQuickSort(window,canvas,array):
    for j in range(array.size):
        arraycopy = copy(array)
        array = quickSort(array,0,len(array)-1)
        if np.array_equal(array, arraycopy):
            break


def selectionSort(array,index):
    #print(array, "selection sorter")
    minNumber = array[index]
    minIndex = index
    for i in range(index+1, array.size):
        if minNumber > array[i]:
            minNumber = array[i]
            minIndex = i
    array[minIndex],array[index] = array[index],array[minIndex]
    return array


def bubbleSort(array):
        for i in range(array.size-1):
            if array[i] > array[i+1]:
                array[i],array[i+1] = array[i+1],array[i]
        return array


def animateBubbleSort(window,canvas, array):
    for j in range(array.size):
        arraycopy = copy(array)
        array = bubbleSort(array)
        drawingGraph(array,canvas)
        if np.array_equal(array, arraycopy):
            break
        window.update()
        time.sleep(animation_refresh_seconds)


def animateSelectionSort(window,canvas,array):
    width = 50 #width of the collumn
    rectLastX = 50 # distance from left top edge
    for i in range(array.size):
        array = selectionSort(array, i)
        drawingGraph(array,canvas)
        canvas.create_line(2*width+width*i, 0, 2*width+i*width, len(array)*15, width=4) #<---- I want to implement a barrier between sorted and unsorted numbers
        canvas.create_text(2*width+width*i, len(array)*15,text="After this line everything is sorted",fill="black")
        window.update()
        time.sleep(animation_refresh_seconds)
            
#***main code***#

def animateSorting(window,canvas):
    

    selectionSort = tkinter.Button(canvas, text="selection Sort", command=lambda: animateSelectionSort(window, canvas, generatedArray))
    bubbleSort = tkinter.Button(canvas, text="buble sort", command=lambda: animateBubbleSort(window, canvas, generatedArray)) #using lambda allows to pass arguments to function
    quickSort = tkinter.Button(canvas, text="quick sort", command=lambda: animateQuickSort(window, canvas, generatedArray))

    selectionSort.pack()
    bubbleSort.pack()
    quickSort.pack()

    slider = tkinter.Scale(canvas,from_=20,to=40,orient='horizontal',command=sliderChanged, variable=currentValue)
    slider.pack()
    generatedArray = np.array([])
    generatedArray = generateNewArray()
    global change
    while True:
        if change == True:
            generatedArray = generateNewArray()
            drawingGraph(generatedArray,canvas)
            change = False
        window.update()


animation_refresh_seconds = 0.05


animation_window = create_animation_window()
animation_canvas = create_animation_canvas(animation_window)
animation_window.protocol('WM_DELETE_WINDOW', animation_window.destroy)
currentValue = tkinter.DoubleVar()
change = False
animateSorting(animation_window,animation_canvas)
from copy import copy
from logging import PlaceHolder
from matplotlib.pyplot import draw
import numpy as np
import random
import tkinter
from tkinter import *
import time
import os
import matplotlib
import winsound
import threading

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
    return arr


def create_animation_window():
    win = tkinter.Tk()
    win.title("Python Sorting Algorythms")
    win.attributes('-fullscreen',True)
    global length
    global height

    length = win.winfo_screenwidth()
    height = win.winfo_screenheight()
    #geometrya = [length, "x", height]
    #geometrya = ''.join([str(elem) for elem in geometrya])
    #win.geometry(geometrya)
    return win


def create_animation_canvas(window):
    canvas = tkinter.Canvas(window)
    canvas.configure(bg="black")
    canvas.pack(fill="both", expand=True)
    return canvas


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
    global drawingCounter
    start = time.perf_counter()
    width = 30
    rectLastX = 20
    canvas.delete("all")
    indicator = canvas.create_rectangle(0,0,100,100, fill="white", tags="indicator")
    if sortingInProgress == False:
        slider.configure(state="active")
        canvas.delete(indicator)
    if sortingInProgress == True:
        slider.configure(state="disabled")
    for i in range(array.size):
        case = array[i]
        canvas.create_rectangle(rectLastX+width, height-case*4, rectLastX+10, height,fill=matplotlib.colors.to_hex([case/255,case/255,case/255]),tags="graph")
        rectLastX += width
        canvas.create_text(rectLastX-width/2, height-case*4-20,text=case, fill=matplotlib.colors.to_hex([1-case/255,1-case/255,1-case/255]),tags="graph")
        canvas.pack()
    time.sleep(animation_refresh_seconds)
    animation_window.update()
    finish = time.perf_counter()
    drawingCounter += finish - start


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


def animateStupidSort(array):
    global drawingCounter
    drawingCounter = 0.0
    start = time.perf_counter()
    index = 0
    global sortingInProgress
    sortingInProgress = True
    while index < len(array):
        if index == 0:
            index = index+1
        if array[index] >= array[index-1]:
            index = index+1
        else:
            array[index], array[index-1] = array[index-1], array[index]
            index = index-1
        drawingGraph(array,animation_canvas)
    sortingInProgress = False
    drawingGraph(array,animation_canvas)
    finish = time.perf_counter()
    print(f"Finished sorting using Stupidsort in: {(finish - start - drawingCounter)*1000000}ns Animation took:{drawingCounter}s")
  


def animateQuickSort(array, canvas):
    global drawingCounter
    drawingCounter = 0.0
    start = time.perf_counter()
    global sortingInProgress
    sortingInProgress = True
    arraycopy = copy(array)
    array = quickSort(array,0,array.size-1)
    sortingInProgress = False   
    drawingGraph(array,canvas)
    finish = time.perf_counter()
    print(f"Finished sorting using Quicksort in: {(finish - start - drawingCounter)*1000000}ns Animation took:{drawingCounter}s")


def animateBubbleSort(canvas, array):
    global drawingCounter
    drawingCounter = 0.0
    start = time.perf_counter()
    global sortingInProgress
    sortingInProgress = True
    for j in range(array.size):
        array = bubbleSort(array)
        drawingGraph(array,canvas)
    sortingInProgress = False
    drawingGraph(array,canvas)
    finish = time.perf_counter()
    print(f"Finished sorting using Bubblesort in: {(finish - start - drawingCounter)*1000000}ns Animation took:{drawingCounter}s")


def animateSelectionSort(canvas,array):
    global drawingCounter
    drawingCounter = 0.0
    start = time.perf_counter()
    global sortingInProgress
    sortingInProgress = True
    for i in range(array.size):
        array = selectionSort(array, i)
        drawingGraph(array,canvas)
    sortingInProgress = False
    drawingGraph(array,canvas)
    finish = time.perf_counter()
    print(f"Finished sorting using Selectionsort in: {(finish - start - drawingCounter)*1000000}ns Animation took:{drawingCounter}s")
            
#***main code***#

def animateSorting(window,canvas):
    global sortingInProgress
    sortingInProgress = False
    global change
    change = False
    global drawingCounter
    drawingCounter = 0.0  

    exitButton = tkinter.Button(canvas, text="exit", command=animation_window.destroy, activebackground="red",activeforeground="white",bd=0, bg="white")
    placeholder = tkinter.Button(canvas, text="placeholder", activebackground="blue",activeforeground="white",bd=0, bg="white")

    selectionSort = tkinter.Button(canvas, text="selection Sort", command=lambda: animateSelectionSort(canvas, generatedArray),bd=0)
    bubbleSort = tkinter.Button(canvas, text="buble sort", command=lambda: animateBubbleSort(canvas, generatedArray),bd=0) #using lambda allows to pass arguments to function
    quickSort = tkinter.Button(canvas, text="quick sort", command=lambda: animateQuickSort(generatedArray, canvas),bd=0)
    #stupidSort = tkinter.Button(canvas, text="stupid sort", command=lambda: animateStupidSort(generatedArray))  <<-- its working but very slow animation

    exitButton.place_configure(x=length-29,y=0)
    placeholder.place_configure(x=length-50,y=20)
    #stupidSort.pack()
    selectionSort.pack()
    bubbleSort.pack()
    quickSort.pack()

    global slider
    slider = tkinter.Scale(canvas,from_=5,to=60,orient='horizontal',command=sliderChanged, variable=currentValue, label="Array size",bd=0,sliderlength=30)
    slider.pack()


    while True:
        if change == True:
            generatedArray = generateNewArray()
            drawingGraph(generatedArray,canvas)
            change = False
        window.update()


animation_refresh_seconds = 0


animation_window = create_animation_window()
animation_canvas = create_animation_canvas(animation_window)
#animation_window.protocol('WM_DELETE_WINDOW', animation_window.destroy)
currentValue = tkinter.DoubleVar()
width = 50
rectLastX = 50
generatedArray = np.array([])
generatedArray = generateNewArray()
animateSorting(animation_window,animation_canvas)
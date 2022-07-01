import random
import threading
import time
import tkinter
from copy import copy
from tkinter import *

#https://stackoverflow.com/questions/63681382/how-to-add-hover-feature-for-text-description-on-a-tkinter-button <- very good example
from widgets import ToolTip
import tkinter.ttk
import matplotlib
import numpy as np
import tkinter_page
from PIL import Image, ImageTk


#https://stackoverflow.com/questions/63017238/how-to-switch-between-different-tkinter-canvases-from-a-start-up-page-and-return <- mostly based on this stack
class Main(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        global window
        window = self
        global length
        global height
        self.attributes('-fullscreen',True)
        length = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.configure(bg="black")
        self._mainCanvas= None
        # The dictionary to hold the class type to switch to
        # Each new class passed here, will only have instance or object associated with it (i.e the result of the Key)
        self._allCanvases = dict()
        # Switch (and create) the single instance of StartUpPage
        self.switch_Canvas(StartUpPage)

    def switch_Canvas(self, Canvas_class):

        # Unless the dictionary is empty, hide the current Frame (_mainCanvas is a frame)
        if self._mainCanvas:
            self._mainCanvas.pack_forget()

        # is the Class type passed one we have seen before?
        canvas = self._allCanvases.get(Canvas_class, False)

        # if Canvas_class is a new class type, canvas is False
        if not canvas:
            # Instantiate the new class
            canvas = Canvas_class(self)
            # Store it's type in the dictionary
            self._allCanvases[Canvas_class] = canvas

        # Pack the canvas or self._mainCanvas (these are all frames)
        canvas.pack(fill="both", expand=True)
        # and make it the 'default' or current one.
        self._mainCanvas = canvas


class StartUpPage(tkinter.Tk, tkinter.Canvas):
    def __init__(self, master, *args, **kwargs):
        tkinter.Canvas.__init__(self, master, *args, **kwargs)
        tkinter.Frame(self) # Here the parent of the frame is the self instance of type tk.Canvas
        global length
        global height
        img = ImageTk.PhotoImage(Image.open('bg.png').resize((length, height), Image.ANTIALIAS))
        lbl = tkinter.Label(self, image=img)
        lbl.img = img  # Keep a reference in case this code put is in a function.
        lbl.place(relx=0.5, rely=0.5, anchor='center')  # Place label in center of parent.
        #self.configure(bg=matplotlib.colors.to_hex((145/255,255/255,247/255)))
        tkinter.Button(self, text="Simple", font=f"Century {round(height/7.2)}",
              command=lambda: master.switch_Canvas(PageOne), 
              #height=round(height/100), width=round(length/20)
              activebackground="green",activeforeground="white"
              ).place(relx=0.5,rely=0.25, anchor="center")
        tkinter.Button(self, text="Advanced", font=f"Century {round(height/7.2)}",
              command=lambda: master.switch_Canvas(PageTwo),
              #height=round(height/100), width=round(length/20)
              activebackground="red",activeforeground="white"
              ).place(relx=0.5,rely=0.75, anchor="center")
        exitButton = tkinter.Button(master, text="exit", command=master.destroy, activebackground="red",activeforeground="white", bg="white",font="20")
        placeholder = tkinter.Button(master, text="placeholder", activebackground="blue",activeforeground="white",bd=0, bg="white")
        exitButton.place_configure(x=length-40,y=0)
        #placeholder.place_configure(x=length-50,y=20)



class PageOne(tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        tkinter.Frame.__init__(self,master, *args, **kwargs) 
        global comparasons
        comparasons = 0
        self.configure(bg=matplotlib.colors.to_hex((145/255,255/255,247/255)))
        global sortingInProgress
        sortingInProgress = False
        global drawingTimer
        drawingTimer = 0.0
        global timer
        timer = ""
        global currentWidth
        currentWidth = tkinter.DoubleVar()
        global currentValue
        currentValue = tkinter.DoubleVar()
        global animation_refresh_seconds
        animation_refresh_seconds = 1
        global length
        global height
        global generatedArray
        generatedArray = generateNewArray()
        global swaps
        swaps = 0
        self.canvas = tkinter.Canvas(self, bg='black', height=height, width=length)
        global selfOne
        selfOne = self.canvas
        global width
        width = 15
        pageBack = tkinter.Button(self.canvas, text="Back",command=lambda: master.switch_Canvas(StartUpPage), activebackground="blue", activeforeground="white")
        

        selectionSort = tkinter.Button(self.canvas, text="selection Sort", command=lambda: animateSelectionSort(self.canvas, generatedArray),bd=1, font=f"{round(height/72)}")
        bubbleSort = tkinter.Button(self.canvas, text="buble sort", command=lambda: animateBubbleSort(self.canvas, generatedArray),bd=1,font=f"{round(height/72)}") #using lambda allows to pass arguments to function
        quickSort = tkinter.Button(self.canvas, text="quick sort", command=lambda: animateQuickSort(generatedArray, self.canvas),bd=1,font=f"{round(height/72)}")
        shellSort = tkinter.Button(self.canvas, text="shell sort", command=lambda: animateShellSort(generatedArray, self.canvas),bd=1,font=f"{round(height/72)}")
        heapSort = tkinter.Button(self.canvas, text="heap sort", command=lambda: animateHeapSort(generatedArray),bd=1,font=f"{round(height/72)}")
        gnomeSort = tkinter.Button(self.canvas, text="gnome sort", command=lambda: animateGnomeSort(generatedArray, self.canvas), bd=1, font=f"{round(height/60)}")  #<<-- its working but very slow animation
        
        
        global slider
        slider = tkinter.Scale(self.canvas,from_=1,to=round(length/width),orient='horizontal',command=sliderChanged, variable=currentValue, label="Array size",bd=1,sliderlength=30,font=f"{round(height/72)}", length=500)
        widthOfTheBars = tkinter.Scale(self.canvas,from_=2,to=20,orient='horizontal',command=widthOfTheBarsChanged, variable=currentWidth, label="Column width",bd=1,sliderlength=30,font=f"{round(height/72)}", length=200, tickinterval=4)

        pageBack.place_configure(x=length-40,y=0)
        slider.place_configure(x=length/2, y=100, anchor="center")
        widthOfTheBars.place_configure(x=length/2, y=50, anchor="center")

        selectionSort.place_configure(x=length/2-round(height/15.15789473684211), y=height/4-round(height/36), anchor="center")
        bubbleSort.place_configure(x=length/2, y=height/4-round(height/36), anchor="center")
        quickSort.place_configure(x=length/2+round(height/18), y=height/4-round(height/36), anchor="center")
        shellSort.place_configure(x=length/2+round(height/9.171974522292994), y=height/4-round(height/36), anchor="center")
        heapSort.place_configure(x=length/2-round(height/7.659574468085106), y=height/4-round(height/36), anchor="center")
        gnomeSort.place_configure(x=length/2, y=height/4-round(height/20.28169014084507), anchor="center")

        self.canvas.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True)



#describing


        tt = ToolTip(selfOne)
        tt.bind(selectionSort, "selection")
        tt.bind(bubbleSort, "bubble")
        tt.bind(quickSort, "quick")
        tt.bind(slider, "slider")
        tt.bind(widthOfTheBars, "widthOfTheBars")
        tt.bind(shellSort, "shell")
        tt.bind(heapSort, "heap")
        tt.bind(gnomeSort, "gnome")


class PageTwo(tkinter.Frame): # Sub-lcassing tk.Frame
    def __init__(self, master, *args, **kwargs):
        # self is now an istance of tk.Frame
        tkinter.Frame.__init__(self,master, *args, **kwargs)
        # make a new Canvas whose parent is self.
        self.canvas = tkinter.Canvas(self,bg='yellow')
        self.label = tkinter.Label(self, text="Second Canvas").pack(side="top", fill="x", pady=5)
        self.button = tkinter.Button(self, text="Menu",
              command=lambda: master.switch_Canvas(StartUpPage))

        self.button.pack()
        # pack the canvas inside the self (frame).
        self.canvas.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True)
        #print('is instance',isinstance(self,tk.Frame))


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


def flipbool(bool):
    if bool is not True:
        bool = True
    else:
        bool = False
    return bool


#generate new array in the same array
def generateNewArray():
    global generatedArray
    generatedArray = ([])
    generatedArray = np.random.randint(1, 255, size = getCurrentValue())
    return generatedArray


# find minimum value of the array
def minim(array):
    min = len(array)
    for j in range(array.size):
        if(min > array[j] and array[j]): # leave out zeroes because we dont draw them
            min = array[j]
    return min


def getCurrentValue():
    global currentValue
    return round(currentValue.get())

def getCurrentWidth():
    global currentWidth
    return round(currentWidth.get())

def widthOfTheBarsChanged(event):
    global currentWidth
    global generatedArray
    global width
    width = getCurrentWidth()
    generatedArray = generateNewArray()
    slider.configure(from_=1, to=round(length/width))
    drawingGraph(generatedArray,selfOne, -1)


def sliderChanged(event):
    global currentValue
    global generatedArray
    global timer
    generatedArray = generateNewArray()
    drawingGraph(generatedArray,selfOne, -1)


# find number by its index
def findIndexByNumber(array, number):
    if number in array:
        NumberIndex = minim(array)-1
        for i in range(np.max(array)):
                if array[i] == number:
                    NumberIndex = i
                    break
        return(NumberIndex)


def drawingGraph(array,canvas, marker):
    global drawingTimer
    global timer
    global sortingInProgress
    global width
    global swaps
    global comparasons
    start = time.perf_counter()
    rectLastX = 0
    canvas.delete("all")
    indicator = canvas.create_rectangle(0,0,100,20, fill="white")
    indicatorText = canvas.create_text(50,10, text="In progress")
    timerText = canvas.create_text(length/2,height/4, text=f"Sorting itself took: {timer}   Animation took: {drawingTimer}s", fill="white", font=("20"))

    swapsText = canvas.create_text(length/2, height/4+20, text=f"swaps: {swaps}   comparasons: {comparasons}", fill="white", font=("20"))

    if sortingInProgress == False:
        canvas.delete(indicator)
        canvas.delete(indicatorText)
    for i in range(array.size):
        case = array[i]
        canvas.create_rectangle(rectLastX, height-case*(height/360), rectLastX+width, height,fill=matplotlib.colors.to_hex([case/255,case/255,case/255]), outline="white")
        rectLastX += width
        canvas.pack()
    #time.sleep(animation_refresh_seconds)
    if marker != -1:
        placeHolder = canvas.create_rectangle(width*marker, height-array[marker]*4, width*marker+width, height,fill="green", outline=None)
    window.update()
    finish = time.perf_counter()
    drawingTimer += finish - start

#optimization
#def graphUpdate(switchFrom, switchTo):
#    canvas = selfOne
#    canvas.delete(graph[switchFrom])
#    canvas.delete(graph[switchTo])
#
#    graph[switchTo], graph[switchFrom] = graph[switchFrom], graph[switchTo]
#
#    window.update()



def partition(array, low, high):
    global swaps
    global comparasons
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        comparasons += 1
        if array[j] <= pivot:
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])
            swaps += 1
    (array[i + 1], array[high]) = (array[high], array[i + 1])

    drawingGraph(array, selfOne, i)

    return i+1


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
        quickSort(array, pi+1, high)
    return array


def selectionSort(array,index):
    global selectionSortPlaceHolder
    global comparasons
    #print(array, "selection sorter")
    global swaps
    minNumber = array[index]
    minIndex = index
    for i in range(index+1, array.size):
        comparasons += 1
        if minNumber > array[i]:
            minNumber = array[i]
            minIndex = i
            swaps += 1
            selectionSortPlaceHolder = minIndex
    array[minIndex],array[index] = array[index],array[minIndex]

    return array


def bubbleSort(array):
    global changes
    changes = 0
    global comparasons
    global swaps
    for i in range(array.size-1):
        comparasons += 1
        if array[i] > array[i+1]:
            array[i],array[i+1] = array[i+1],array[i]
            changes += 1
            swaps +=1
        drawingGraph(array, selfOne, i+1)

    return array


def animateGnomeSort(array, canvas):
    global drawingTimer
    global swaps
    global comparasons
    comparasons = 0
    swaps = 0
    drawingTimer = 0.0
    start = time.perf_counter()
    index = 0
    global sortingInProgress
    global width
    slider.configure(state="disabled")
    sortingInProgress = True
    while index < len(array):
        comparasons += 1
        if index == 0:
            index = index+1
        if array[index] >= array[index-1]:
            index = index+1
        else:
            array[index], array[index-1] = array[index-1], array[index]
            index = index-1
            swaps += 1
        if index == len(array):
            break
        drawingGraph(array,canvas, index)
    finish = time.perf_counter()
    sortingInProgress = False
    global timer
    timer = f"{finish - start - drawingTimer}s"
    drawingGraph(array,canvas, -1)
    slider.configure(state="active")
    #print(f"Finished sorting using Stupidsort in: {(finish - start - drawingTimer)*1000000}ns Animation took:{drawingTimer}s")



def animateQuickSort(array, canvas):
    global comparasons
    comparasons = 0
    global swaps
    swaps = 0
    global drawingTimer
    drawingTimer = 0.0
    start = time.perf_counter()
    global sortingInProgress
    slider.configure(state="disabled")
    sortingInProgress = True
    array = quickSort(array,0,array.size-1)
    sortingInProgress = False   
    finish = time.perf_counter()
    global timer
    timer = f"{finish - start - drawingTimer}s"
    drawingGraph(array,canvas, -1)
    slider.configure(state="active")
    #print(f"Finished sorting using Quicksort in: {(finish - start - drawingTimer)*1000000}ns Animation took:{drawingTimer}s")


def animateBubbleSort(canvas, array):
    global timer
    global comparasons
    comparasons = 0
    global bubbleSortPlaceHolder
    bubbleSortPlaceHolder = -1
    global drawingTimer
    drawingTimer = 0.0
    global swaps
    swaps = 0
    start = time.perf_counter()
    global sortingInProgress
    slider.configure(state="disabled")
    sortingInProgress = True
    while True:
        array = bubbleSort(array)
        if changes == 0:
            break
    sortingInProgress = False
    drawingGraph(array,canvas, -1)
    finish = time.perf_counter()

    timer = f"{finish - start - drawingTimer}s"
    drawingGraph(array,canvas, -1)
    slider.configure(state="active")
    #print(f"Finished sorting using Bubblesort in: {(finish - start - drawingTimer)*1000000}ns Animation took:{drawingTimer}s")

def animateShellSort(array,canvas):
    global timer
    global comparasons
    comparasons = 0
    slider.configure(state="disabled")
    start = time.perf_counter()
    global swaps
    swaps = 0
    global drawingTimer
    drawingTimer = 0
    # code here
    gap=len(array)//2
      
      
    while gap>0:
        j=gap
        # Check the array in from left to right
        # Till the last possible index of j
        while j<len(array):
            i=j-gap # This will keep help in maintain gap value
              
            while i>=0:
                # If value on right side is already greater than left side value
                # We don't do swap else we swap
                comparasons += 1
                if array[i+gap]>array[i]:
  
                    break
                else:
                    array[i+gap],array[i]=array[i],array[i+gap]
                    swaps += 1
  
                i=i-gap # To check left side also
                            # If the element present is greater than current element 
            j+=1
            drawingGraph(array, canvas, i)
        gap=gap//2
    finish = time.perf_counter()

    timer = f"{finish - start - drawingTimer}s"
    drawingGraph(array, selfOne, -1)
    slider.configure(state="active")
  

def heapify(arr, n, i):
    global swaps
    global comparasons
    largest = i  # Initialize largest as root
    l = 2 * i + 1     # left = 2*i + 1
    r = 2 * i + 2     # right = 2*i + 2
  
    # See if left child of root exists and is
    # greater than root
    comparasons += 1
    if l < n and arr[largest] < arr[l]:
        largest = l
    # See if right child of root exists and is
    # greater than root
    comparasons += 1
    if r < n and arr[largest] < arr[r]:
        largest = r
  
    # Change root, if needed
    if largest != i:
        swaps += 1
        arr[i], arr[largest] = arr[largest], arr[i]  # swap
  
        # Heapify the root.
        heapify(arr, n, largest)
    
    
    drawingGraph(arr,selfOne,largest)
  
# The main function to sort an array of given size
  
  
def animateHeapSort(array):
    global comparasons
    comparasons = 0
    slider.configure(state="disabled")
    start = time.perf_counter()
    global swaps
    swaps = 0
    global drawingTimer
    drawingTimer = 0
    n = len(array)
  
    # Build a maxheap.
    for i in range(n//2 - 1, -1, -1):
        heapify(array, n, i)
  
    # One by one extract elements
    for i in range(n-1, 0, -1):
        swaps += 1
        array[i], array[0] = array[0], array[i]  # swap
        heapify(array, i, 0)
    finish = time.perf_counter()
    global timer
    timer = f"{finish - start - drawingTimer}s"
    drawingGraph(array, selfOne, -1)
    slider.configure(state="active")




def animateSelectionSort(canvas,array):
    global comparasons
    comparasons = 0
    global swaps
    swaps = 0
    global drawingTimer
    drawingTimer = 0.0
    start = time.perf_counter()
    global sortingInProgress
    global selectionSortPlaceHolder
    selectionSortPlaceHolder = -1
    slider.configure(state="disabled")
    sortingInProgress = True
    for i in range(array.size):
        drawingGraph(array,canvas, selectionSortPlaceHolder)
        array = selectionSort(array, i)

    sortingInProgress = False
    drawingGraph(array,canvas, -1)
    finish = time.perf_counter()
    global timer
    timer = f"{finish - start - drawingTimer}s"
    drawingGraph(array,canvas, -1)
    slider.configure(state="active")
    #print(f"Finished sorting using Selectionsort in: {(finish - start - drawingTimer)*1000000}ns Animation took:{drawingTimer}s")
            

if __name__ == "__main__":
    app = Main()
    app.mainloop()
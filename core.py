import pandas as pd
import tkinter.filedialog as fd
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import os
import math
import tkinter.messagebox

sourceDirectory,sourceFile ='',''
inputData = pd.DataFrame()
outputData = pd.DataFrame()


def updateTBox(output,over=False):
    if over:
        tBox.delete("1.0", END)
        tBox.insert(INSERT, output+"\n")
    else:
        tBox.insert(INSERT, output+"\n")
    window.update()

def exportData():
    updateTBox("Checking fields...",over=True)
    try:
        updateTBox("Selecting File...")
        f = tk.filedialog.asksaveasfile(mode='w', defaultextension=".csv")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            updateTBox("No file selected...")
            return
        if buildPreview(False):
            #text2save = str(text.get(1.0, END)) # starts from `1.0`, not `0.0`
            updateTBox(("File selected :" + f.name))
            fNAME, fEXT = os.path.splitext(f.name)
            #print(fNAME, fEXT)

            limit = 999999
            breakDown = math.ceil(len(outputData) / limit)
            addition = limit
            start=0

            if len(outputData)>limit:

                updateString = ("File is greater than "+str(limit)+" records... ")

                updateTBox(updateString)
                updateTBox("Creating supplementary split files...")
                for i in range(breakDown):
                    bName=fNAME+" "+str(i+1)+" of "+str(breakDown)+fEXT
                    if(limit<len(outputData)):
                        #print(start,limit)
                        #print(outputData.iloc[start:limit])
                        outputData.iloc[start:limit].to_csv(bName, index=False)
                        start=limit
                        limit = limit+addition
                    else:
                        outputData.iloc[start:len(outputData)].to_csv(bName, index=False)
                        start = limit
                        limit = limit + addition

                    updateTBox("File "+str(i+1)+" of "+str(breakDown)+" Saved...")

            outputData.to_csv(f.name, index=False)
            tk.messagebox.showinfo("Save Status", "All files saved successfully!")
            updateTBox("Master File saved...")
            #f.close() # `()` was missing.
    except:
        updateTBox("Something went wrong...",True)
    return

def buildData(keyList,fillTable):
    global inputData
    global outputData
    updateTBox("Building output...")
    #print("start of this biz")
    print("Converting Data...")
    #for i in keyList:
     #   print(i)

    #vertical Logic

    updateTBox("Converting data to Vertical Format...")

    dfLen = len(inputData)

    limit = math.ceil(dfLen/10)
    addition = limit
    breakDown = math.ceil(dfLen / limit)

    print("Data record count: ",dfLen)
    print("Processing records in batches of: ",limit)

    start=0
    #print(inputData.iloc[0:len(inputData)])
    #print(keyList)

    tempheaderList = []
    for i in keyList:
        tempheaderList.append(i)
    tempheaderList.append('Code')
    tempheaderList.append('Values')
    #print(tempheaderList)
    outputData = pd.DataFrame(columns=tempheaderList)
    #print(outputData)
    tempDF = pd.DataFrame()

    while(start<dfLen):
        if(limit<len(inputData)):
            print("Processing Records ",start, " - ",limit)
            #print(inputData.iloc[start:limit])
            tempDF = pd.melt(inputData.iloc[start:limit], id_vars=keyList, var_name='Code', value_name='Values')
            tempDF= removeValues(tempDF)

            print(tempDF)
            start = limit
            limit = limit + addition
            #print(start,limit,len(inputData))

        else:
            #print(inputData.iloc[start:len(inputData)])
            print("Processing Records ", start, " - ", len(inputData))
            tempDF = pd.melt(inputData.iloc[start:len(inputData)], id_vars=keyList, var_name='Code', value_name='Values')
            tempDF = removeValues(tempDF)

            print(tempDF)
            start = limit
            limit = limit + addition
        outputData= outputData.append(tempDF,ignore_index=True)
            #print(start,limit,len(inputData))

    #print(dfLen,limit,breakDown)
    #print("printing output data")
    #print(outputData)

    #outputData = pd.melt(inputData, id_vars=keyList, var_name='Code', value_name='Values')

    updateTBox("Cleaning data output...")


    if dupeDrop.get() > 0:
        outputData = outputData.drop_duplicates()

    #outputData = outputData.drop(indexNames, inplace = True)
    outputData= outputData.sort_values(keyList)
    outputData =outputData.reset_index(drop=True)

    print(outputData)
    print("Processing complete...")
    if fillTable:
        for i in outputTree.get_children():
            outputTree.delete(i)
        outputTree["columns"] = []
        buildTables(outputData,outputTree)

    return

def buildPreview(fillTable = True):
    updateTBox("Checking fields...",True)
    keyList=[]
    for i in headerListBox.curselection():
        keyList.append(headerListBox.get(i))

    #print(len(keyList), outputFormat.get())
    if (len(keyList)==0):
        tk.messagebox.showinfo("Key Field Error", "Please select at least one Key field...")
        updateTBox("Error: No headers selected...")

    if (len(keyList)>0):

        buildData(keyList,fillTable)
        return True
    else:
        return False

def loadFile():
    # select file source location
    global sourceFile
    global inputData
    global outputData
    sourceFile=''
    updateTBox("Please select file:...",True)
    sourceFile =fd.askopenfilename()
    if sourceFile =='':
        updateTBox("No File Selected...",True)
    else:
        try:
            #sourceFile = r'C:/Users/dylewskc/Desktop/Source Files/Balance Conversion/DL_ 2015_ Check_ FIle_ ADP2.csv'

            updateTBox("File selected: "+os.path.basename(sourceFile))
            #print(sourceFile, inputData)

            for i in inputTree.get_children():
                inputTree.delete(i)
            inputTree["columns"] = []
            for i in outputTree.get_children():
                outputTree.delete(i)
            outputTree["columns"] = []

            headerListBox.delete(0, END)

            # print(sourceDirectory)
            #print(sourceFile)

            name, ext = os.path.splitext(sourceFile)
            #print("Name = ", name, 'EXT = ', ext)
            if (ext == '.csv'):
                #print('CSV')
                inputData = pd.read_csv(sourceFile, dtype= str, low_memory=False)

            if (ext == '.xlsx'):
                #print('XLSX')
                inputData = pd.read_excel(sourceFile, dtype= str)

                #data['SUM'] = data[data.columns.values.tolist()[13:len(data.columns.values.tolist())]].sum(axis=1)
            outputData = pd.DataFrame()
            #print(len(outputData))
            buildTables(inputData,inputTree,True)

        except:
            updateTBox("something went wrong...")
    return

def buildTables(df,tree,updateHeaderlist = False):
    try:

        headerlist = df.columns.values.tolist()
        tree["columns"] = (headerlist)

        for j in tree["columns"]:
            # print(j)
            tree.column(j, width=len(j) * 10, anchor='center')
            tree.heading(j, text=j)

        dRange=len(df)
        if (100 < dRange):
            outputRange = 100
        else:
            outputRange = dRange

        for j in range(outputRange):
            tree.insert("", 'end', text=j, values=df.iloc[j].values.tolist())

        tree.column("#0", width=50)

        if updateHeaderlist:
            for item in df.columns.values.tolist():
                headerListBox.insert(END, item)

        if len(outputData)==0:
            updateTBox("Output complete...")
            updateTBox("Records found:" + str(len(df)))
            updateTBox("Records displayed:" + str(outputRange))
            updateTBox("Memory utilization: " + str(round(df.memory_usage(index = False).sum() / 1024 / 1024, 2)) + "MB")
            updateTBox("Headers Found:" + str(len(headerlist)))
        else:
            updateTBox("Output complete...")
            updateTBox("Old Data record length:" + str(len(inputData)))
            updateTBox("Old Memory utilization: " + str(round(inputData.memory_usage(index = False).sum() / 1024 / 1024, 2)) + "MB")
            updateTBox("New Data record length:" + str(len(outputData)))
            updateTBox("New Memory utilization: " + str(round(outputData.memory_usage(index = False).sum() / 1024 / 1024, 2)) + "MB")


    except:
        updateTBox("something went wrong...")

def zeroCheck(val):
    if (type(val) == str):
        if (val.isdigit()):
            if(int(val)==0):
                return 0
            else:
                return val
        else:
            return val
    else:
        return val

def removeValues(df):
    if nullDrop.get() > 0:
        df = df[pd.notnull(df['Values'])]
    if zeroDrop.get() > 0:
        df['Values'] = df['Values'].apply(zeroCheck)
        df = df[df['Values'] != 0]
    if starDrop.get() > 0:
        df = df[df['Values'] != '*']
    if hashDrop.get() > 0:
        df = df[df['Values'] != '-']
    df = df[df['Values'] != entryV.get()]
    return df

def buildWindow():
    global outputFormat

    for y in range(10):
        for x in range(10):
            window.rowconfigure(y, weight = 1)
            window.columnconfigure(x, weight = 1)

    #buttonFrame = tk.Frame(window, highlightbackground="green", highlightcolor="green", highlightthickness=1,bd=0)
    #headerFrame = tk.Frame(window, highlightbackground="green", highlightcolor="green", highlightthickness=1,bd=0)
    #inputFrame = tk.Frame(window, highlightbackground="green", highlightcolor="green", highlightthickness=1,bd=0)
    #outputFrame = tk.Frame(window, highlightbackground="green", highlightcolor="green", highlightthickness=1,bd=0)

    buttonFrame = tk.Frame(window, highlightbackground="black", highlightcolor="black", highlightthickness=1, bd=0)
    headerFrame = tk.Frame(window,highlightbackground="black", highlightcolor="black", highlightthickness=1, bd=0)
    inputFrame = tk.Frame(window,highlightbackground="black", highlightcolor="black", highlightthickness=1, bd=0)
    outputFrame = tk.Frame(window,highlightbackground="black", highlightcolor="black", highlightthickness=1, bd=0)

    buttonFrame.propagate(False)
    headerFrame.grid_propagate(False)
    inputFrame.grid_propagate(False)
    outputFrame.grid_propagate(False)

    #print(window.grid_size())

    for y in range(2):
        for x in range(1):
            buttonFrame.rowconfigure(y, weight = 1)
            buttonFrame.columnconfigure(x, weight = 1)
    for y in range(100):
        for x in range(60):
            headerFrame.rowconfigure(y, weight = 1)
            headerFrame.columnconfigure(x, weight = 1)
    for y in range(100):
        for x in range(100):
            inputFrame.rowconfigure(y, weight = 1)
            inputFrame.columnconfigure(x, weight = 1)
    for y in range(100):
        for x in range(100):
            outputFrame.rowconfigure(y, weight = 1)
            outputFrame.columnconfigure(x, weight = 1)
    #print(buttonFrame.grid_size())

    buttonFrame.grid(row=0,column=0,rowspan=2,columnspan = 2,sticky = N+S+W+E)
    headerFrame.grid(row=2,column=0,rowspan=8,columnspan = 2,sticky = N+S+W+E)
    inputFrame.grid(row=0,column=2,rowspan=5,columnspan = 8,sticky = N+S+W+E)
    outputFrame.grid(row=5,column=2,rowspan=5,columnspan = 8,sticky = N+S+W+E)

    buttonFrame.propagate(0)
    headerFrame.propagate(0)
    inputFrame.propagate(0)
    outputFrame.propagate(0)

    inputTreeFrame = tk.Frame(inputFrame, highlightbackground="green", highlightcolor="green", highlightthickness=1,bd=0)
    inputHScrollBar = Scrollbar(inputFrame, orient=HORIZONTAL)
    inputVScrollBar = Scrollbar(inputFrame, orient=VERTICAL)

    inputTree = Treeview(inputTreeFrame, xscrollcommand=inputHScrollBar.set,yscrollcommand=inputVScrollBar.set)
    inputHScrollBar.config(command=inputTree.xview)
    inputVScrollBar.config(command=inputTree.xview)
    #
    inputHScrollBar.grid(row = 100, column = 0, columnspan = 100, sticky = N+W+S+E)
    #inputVScrollBar.grid(row=1, column=0, rowspan=99, sticky=N + W + S + E)
    inputTreeFrame.grid(row = 0, column = 0,rowspan = 99,columnspan = 100, sticky = N+W+S+E)
    inputTreeFrame.grid_propagate(False)
    inputTree.pack(expand = True, fill = BOTH)

    outputTreeFrame = tk.Frame(outputFrame, highlightbackground="green", highlightcolor="green", highlightthickness=1,bd=0)
    outputHScrollBar = Scrollbar(outputFrame, orient=HORIZONTAL)
    outputVScrollBar = Scrollbar(outputFrame, orient=VERTICAL)

    outputTree = Treeview(outputTreeFrame, xscrollcommand=outputHScrollBar.set,yscrollcommand=outputVScrollBar.set)
    outputHScrollBar.config(command=outputTree.xview)
    outputVScrollBar.config(command=outputTree.xview)
    #
    outputHScrollBar.grid(row = 100, column = 0, columnspan = 100, sticky = N+W+S+E)
    #outputVScrollBar.grid(row=1, column=0, rowspan=99, sticky=N + W + S + E)
    outputTreeFrame.grid(row = 0, column = 0,rowspan = 99,columnspan = 100, sticky = N+W+S+E)
    outputTreeFrame.grid_propagate(False)
    outputTree.pack(expand = True, fill = BOTH)

    hX,hY = headerFrame.grid_size()
    headerScrollBar = Scrollbar(headerFrame)
    headerListBox = Listbox(headerFrame, selectmode=EXTENDED, yscrollcommand=headerScrollBar.set, relief = RAISED)
    headerScrollBar.config(command=headerListBox.yview)
    progress = Progressbar(headerFrame, orient=VERTICAL)

    headerLabel = Label(headerFrame,text="Key Fields:")
    headerLabel.grid(row =1, column = 0,columnspan =hX, sticky = N+W+S+E)
    headerScrollBar.grid(row =2, column = 0,rowspan = hY-1,columnspan =1, sticky = N+W+S+E)
    headerListBox.grid(row = 2, column = 1, rowspan = hY-1,columnspan = hX-1 ,sticky = N+S+E+W)

    removeLabel = Label(headerFrame,text="Remove:")
    removeLabel.grid(row=hY,column=0,columnspan = 10, sticky = N+W+E+S )
    entryBox = tk.Entry(headerFrame,exportselection=0,textvariable = entryV)
    entryBox.grid(row=hY,column=10,columnspan = 40, sticky = N+W+E+S)
    zeroDropCheck = tk.Checkbutton(headerFrame,variable = zeroDrop,text = ': 0')
    nullDropCheck = tk.Checkbutton(headerFrame,variable=nullDrop, text = ': NULL')
    hashDropCheck = tk.Checkbutton(headerFrame,variable=hashDrop,text = ': -')
    starDropCheck = tk.Checkbutton(headerFrame,variable=starDrop,text = ': *')
    dupeDropCheck = tk.Checkbutton(headerFrame, variable=dupeDrop, text=':Duplicates')

    zeroDropCheck.grid(row = hY+1, column = 0,sticky = N+S+E+W)
    nullDropCheck.grid(row = hY+1, column = 10,sticky = N+S+E+W)
    hashDropCheck.grid(row = hY+1, column = 20,sticky = N+S+E+W)
    starDropCheck.grid(row = hY+1, column = 30,sticky = N+S+E+W)
    dupeDropCheck.grid(row=hY + 1, column=40, sticky=N + S + E + W)

    tBox = tk.Text(buttonFrame, width = int(window.winfo_width()*0.001),height = int(window.winfo_height()*0.001), bg = "black",fg = "white")
    tBox.grid(row = 0, column = 0,rowspan = 10, columnspan = 50, sticky = N+S+W+E)
    tBox.insert(END,"Hello..")

    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Load", command=lambda:loadFile())
    filemenu.add_command(label="Preview", command=lambda:buildPreview())
    filemenu.add_command(label="Extract", command=lambda: exportData())

    filemenu.add_separator()

    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    window.config(menu=menubar)

    return headerListBox,inputTree, outputTree,tBox

window = Tk()
window.title("Horizontal to Vertical Conversion Tool v1.2")
window.geometry("1200x600")

nullDrop = tk.IntVar()
zeroDrop = tk.IntVar()
hashDrop = tk.IntVar()
starDrop = tk.IntVar()
dupeDrop = tk.IntVar()


textV = tk.StringVar()
entryV = tk.StringVar()
headerListBox,inputTree, outputTree,tBox = buildWindow()

window.mainloop()
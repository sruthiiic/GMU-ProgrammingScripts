#all of the imports to create and execute funcionality within the GUI
import os.path
import subprocess   
import time
import sys
import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
from tkinter import StringVar, filedialog
from typing import Text
from ScrollableNotebook import *
import threading
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from PIL import Image, ImageTk
from pandastable import Table, TableModel
import sqlite3
import pandas as pd
import csv
import shutil



#Name of the current user
cmd=subprocess.run("whoami",stdout=subprocess.PIPE)
user_name=cmd.stdout.decode("utf-8").strip()

#Change the following as necessary
desktop_path="/home/{user}/Desktop".format(user=user_name)

#import directory path
import_path=desktop_path+"/imports"

#defines the window
root = tk.Tk()
root.title('Access D3niers')
#set background color
root['background']='#003478'
root.geometry('1280x720')

#defines the notebook widget
tabControl = ScrollableNotebook(root, wheelscroll=True, tabmenu=True)


#screen layout
def tabLayout():
    #destroy the start button
    btn0.destroy()
    #makes uploadedFiles a list
    orderedUploads = list(uploadedFiles)
    #sort by alphabetical order
    orderedUploads.sort(key = lambda x: x.lower())

    #for each file in ordered uploads
    for name in orderedUploads:
        print(name)
        #checking if the filename ends with any of the following extensions
        if name.lower().endswith(('.txt', '.png', '.jpg', 'jpeg', '.db', '.csv')):#'.db',
            if name not in previousUploads:
                #add name to used list
                previousUploads.add(name)
                tab = ttk.Frame(tabControl)

                #text files
                if name.lower().endswith('.txt'):
                    #put a scrolled text box onto the tab and have it fill the area
                    content = st.ScrolledText(tab, wrap = tk.WORD)
                    content.pack(expand = True, fill = "both")
                    #open the file and read it
                    with open(name, 'r', encoding='ISO-8859-1') as f:
                        #reads the data
                        data = f.read()
                        #inserts data into the content window
                        content.insert(tk.END, data)
                    tab_name = name
                #checking if the extension indicates that it is a database file
                elif name.lower().endswith('.db') or name.lower().endswith('.sqlite'):
                    #executes to database to csv file conversion bash script
                    os.system("./DB2CSV.sh")
                    continue

               #checking if the extension is .csv
                elif name.lower().endswith('.csv'):
                    tab_name = name
                    #calls the csvDisplay function to display csv format in the GUI
                    csvDisplay(name, tab)
                else:
                    # open the picture to resize
                    img = Image.open(name)
                    # resize the image
                    imgrs = img.resize((img.width, img.height), Image.ANTIALIAS)
                    # set the picture
                    pic = ImageTk.PhotoImage(imgrs)
                    # set the label to display the picture
                    content = tkinter.Label(tab, image=pic)
                    # keep a reference to the tkinter object so that the picture shows: "Why do my Tkinter images not appear?"
                    content.image = pic
                    # place the image
                    content.pack(expand=True, fill="both")
                    tab_name = name

                # give tab the current file name
                tabControl.add(tab, text=tab_name)
                # organize the tabs
                tabControl.pack(expand=True, fill="both")


# set for uploadedFiles
uploadedFiles = set()
# set for previous uploads to compare to
previousUploads = set()


#display the csv
def csvDisplay(filepath, tab):
    #sets the table
    table = Table(tab, showstatusbar=True, showtoolbar=True)

    #open the csv file
    table.importCSV(filepath)
    
    #show the csv file on the table
    table.show()


# scans the current directory for
def fileUpdate():
    # set path as current directory
    path = os.getcwd()
    # os.chdir('./ScriptFiles')

    # iterate through each file in the directory
    for entry in os.scandir(path):
        if entry.path.lower().endswith(('.txt', '.png', '.jpg', 'jpeg', '.db','.csv')) or entry.name == "signalBackup":#'.db', 
            # sleep timer for databases to load and convert
            time.sleep(.1)
            # adds the file to the set
            uploadedFiles.add(entry.name)

#getting the database files from the imported chat application database folders                
def getFiles():
    try:
        #list of database files to copy to current directory
        srcFileLst = ["{desk_p}/com.whatsapp/databases/msgstore.db".format(desk_p=import_path), 
        "{desk_p}/com.nandbox.nandbox/databases/courgette.db".format(desk_p=import_path),
        "{desk_p}/com.microsoft.teams/databases/SkypeTeams.db".format(desk_p=import_path),
        "{desk_p}/kik.android/databases/51c54d5d-cfda-4355-8ac2-9470dcecd5b2.kikDatabase.db".format(desk_p=import_path),
        "{desk_p}/com.wire/databases/af7b1f93-b00c-433f-93da-ac19cbebd308".format(desk_p=import_path),
        "{desk_p}/com.skype.raider/databases/s4l-live:.cid.3e619d490d75ed0c.db".format(desk_p=import_path)]
         
        #list of filenames corresponding to the database files in srcFileLst
        dstFileLst = ["./msgstore.db",
        "./courgette.db",
        "./SkypeTeams.db",
        "./kikDatabase.db",
        "./wire.db",
        "./skype.db"]

        #for each index in srcFileLst
        for i in range(len(srcFileLst)):
            try:

                #if the file exists 
                if os.path.isfile(srcFileLst[i]):
                    print(srcFileLst[i],dstFileLst[i])
                    #copy the file into the destination filename so it can reside in the current directory
                    shutil.copy2(srcFileLst[i], dstFileLst[i])
            except:
                pass
    except:
        pass

class Event(LoggingEventHandler):
    #executes this functions when dispatch() is called
    def dispatch(self, event):
        fileUpdate()
        getFiles()
        tabLayout()
   

# automatically update the tabs
def fileWatch():
    # set the format for logging info
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # set format for displaying path
    path = os.getcwd()
    path2 = import_path
   # with open('watchdogOuput.txt', 'w') as f:
    #    sys.stdout = f# initialize logging event
    event_handler = Event()
    # initialize logging event handler to print actions
    event_log = LoggingEventHandler()


    # initialize Observer
    observer = Observer()
    #observing current directory (path)
    observer.schedule(event_handler, path, recursive=True)
    #observing the directory which the chat application databases are in
    observer.schedule(event_handler, path2, recursive=True)
    observer.schedule(event_log, path, recursive=True)

    # start the observer
    observer.start()
    try:
        while True:
            # set the thread sleep time
            time.sleep(.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def file_pull():
    os.system('x-terminal-emulator -e "python3 -u test.py; read" &')

#button to pull the database files by executing test.py
B=tkinter.Button(root,text="Pull Database",command= file_pull)
B.place(x=25, y=3000)
B.pack()

# initial start button
btn0 = tk.Button(text='Start', width=10, fg='black', highlightbackground='#003478',command=lambda: [fileUpdate(), tabLayout(), getFiles()])
btn0.place(relx=0.5, rely=0.5, anchor='center')

# start another thread for fileWatch, set to daemon so that it stops when the window closes
fileWatchThread = threading.Thread(target=fileWatch, daemon=True)
fileWatchThread.start()

# spawns the window
root.mainloop()
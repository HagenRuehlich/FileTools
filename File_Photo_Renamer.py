# -*- coding: utf-8 -*-


from FileUtilities import *
from FileTraverser import *
from tkinter import filedialog
from tkinter import *

c_BASE_PHOTO_FOLDER = "K:\\Datenbereich\\Fotos"

def renamePhotos ():
    sFolderToRename = selectFolder ()
    if sFolderToRename != "":
        oRename =  CFileTraverserPhotoRenamer (sFolderToRename)
        oRename.travers ()
        
    
    
    

def selectFolder ():
    sReturnFolder = ""
    Tk().withdraw()
    print("Initializing Dialogue...\nBitte Ordner mit Fotos zum umbenennen auswählen")
    sReturnFolder = filedialog.askdirectory(initialdir = c_BASE_PHOTO_FOLDER, title='Ordner mit Fotos zum umbenennen auswählen')
    if len(sReturnFolder) > 0:
        print ("You chose %s" % sReturnFolder)
    return sReturnFolder



if __name__ == "__main__":
    renamePhotos ()
    
 

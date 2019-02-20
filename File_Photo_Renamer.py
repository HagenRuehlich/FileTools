# -*- coding: utf-8 -*-


from FileUtilities import *
from FileTraverser import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *

c_BASE_PHOTO_FOLDER = "K:\\Datenbereich\\Fotos\\Fotos 2019"

def renamePhotos ():
    sFolderToRename = selectFolder ()
    if sFolderToRename != "":
##        bFileAlreadyRenamed =  areFilesAleadyRenamed (sFolderToRename)
##        if bFileAlreadyRenamed :
##            ask the user if to go in case the files in selected folder seem to be renamed already
            
        oRename =  CFileTraverserPhotoRenamer (sFolderToRename)
        oRename.travers ()
        
    
def areFilesAleadyRenamed (psFoldertoCheck):
    bFilesAlreadyRenamed = False
    verifyPath (psFoldertoCheck)
    #Go on here...
    return bFilesAlreadyRenamed
    

def selectFolder ():
    sReturnFolder = ""
    Tk().withdraw()
    print("Initializing Dialogue...\nBitte Ordner mit Fotos zum umbenennen auswählen")
    sReturnFolder = filedialog.askdirectory(initialdir = c_BASE_PHOTO_FOLDER, title='Ordner mit Fotos zum umbenennen auswählen')
    if len(sReturnFolder) > 0:
        print ("You chose %s" % sReturnFolder)
    else:
        print ("Kein Ornder gewählt. Abbruch")
    return sReturnFolder



if __name__ == "__main__":
    renamePhotos ()
    
 

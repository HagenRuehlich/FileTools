# -*- coding: utf-8 -*-
import os
import shutil

PHOTO_FILE_EXT = ".jpg"
PHOTO_RAW_EXT = ".nef"

cFOLDER = 0
cFILE = 1




def verifyPath (psPath):
    assert type (psPath) == str
    assert psPath != ""
    
def testPathWritability (psPath):
    verifyPath (psPath)
    if not os.access (psPath, os.W_OK):
        raise OSError ("Keine Schreibrechte im Verzeichnis " + psPath)

def joinToAbsPath (psPath1, psPath2):
    verifyPath (psPath1)
    verifyPath (psPath2)
    sReturnPath = os.path.join (psPath1, psPath2)
    sReturnPath = os.path.abspath (sReturnPath)
    return sReturnPath

def assertFolder (psFolderPath):
    verifyPath (psFolderPath)
    assert os.path.isdir (psFolderPath)

def assertFile (psAbsFile):
    verifyPath (psAbsFile)
    assert os.path.isfile (psAbsFile)
    


def isExtentionMatching (psExtension, psFile):
    verifyPath (psFile)
    bReturn = False
    sExtend = getFileExtention (psFile)
    sExtend = sExtend.lower()
    if sExtend == psExtension :
        bReturn = True
    return bReturn

def getPartOfAbsPath (psPath, piPart):
    """returns either folder part (piPart == 0) or file part (piPart ==1) of psPath"""
    assert ((piPart == cFILE) or (piPart == cFOLDER))
    return os.path.split (psPath)[piPart]
    
    


def getFolderFromAbsPath (psAbsPath):
    verifyPath (psAbsPath)
    return getPartOfAbsPath (psAbsPath, cFOLDER)

def getFileFromAbsPath (psAbsPath):
    verifyPath (psAbsPath)
    return getPartOfAbsPath (psAbsPath, cFILE)

def getInnerFolderFromAbsFile (psAbsFile):
    """Return the sub folder were the file is in, e.g. for n"c:\data\photos\dcim32.jpg" it returns "photos"""
    verifyPath (psAbsFile)
    assert os.path.isfile (psAbsFile)
    
    sFolderComplete = getFolderFromAbsPath (psAbsFile)
    sFolders = sFolderComplete.rsplit ("\\")
    iLen = len (sFolders)
    assert iLen > 0
    sReturn = sFolders [iLen - 1]
    return sReturn
    
def getFileExtention (psFile):
    verifyPath (psFile)
    return os.path.splitext (psFile)[1]


def getFileNameWithoutExention (psFile):
    verifyPath (psFile)
    sFileWithExt = getFileFromAbsPath (psFile)
    sReturn = os.path.splitext (sFileWithExt)[0]
    return sReturn

def createFile (psAbsFolder, psFile):
    verifyPath (psAbsFolder)
    verifyPath (psFile)
    """create the psFile in psAbsFolder"""
    f = open (psAbsFolder + "\\" + psFile , "w")
    f.close ()

def createFolder (psAbsFolder):
    verifyPath (psAbsFolder)
    os.mkdir (psAbsFolder)

def isJoinedAbsPathFolder (psAbsFolder, psFolderItem):
    """Joines psAbsFolder and psFolderItem to an absolute path and returns True is the reuslt is folder, else False"""
    sAbsPath = joinToAbsPath (psAbsFolder, psFolderItem)
    return os.path.isdir (sAbsPath)

def removeFolderStructureComplete (psAbsFolder) :
    verifyPath (psAbsFolder)
    shutil.rmtree (psAbsFolder)
    
    

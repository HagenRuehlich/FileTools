# -*- coding: utf-8 -*-


import os

PHOTO_FILE_EXT = ".jpg"
PHOTO_RAW_EXT = ".nef"



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
    

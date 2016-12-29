# -*- coding: utf-8 -*-
import os
import enum
import shutil
from   tkinter import filedialog
from fileUtilities import *  

PHOTO_RAW_EXT = ".nef"


class CFileIterator ():
    """This classe allows process files in sub folders (like simply delete), objects of this class get constructed by
       the folder to start in, the file types to considered and the operation to do"""
    def __init__ (self, psBaseFolder, pFileOperation, pExtend):
        assert type (psBaseFolder) == str
        assert psBaseFolder != ""
        self._BaseFolder = psBaseFolder
        assert type (pFileOperation) == CFileOperation
        self._FileOperation = pFileOperation
        assert type (pExtend) == str
        self._Extend = pExtend
        self._NumberOfProcessedFiles = 0

    def run (self):
        """ this method performs the via _FileOperation defined operation file. It starts in folder _BaseFolder and considers
               all sub folders in unlimited depth. It returns the number of processed files """
        self.checkMember ()
        self._NumberOfProcessedFiles = 0
        iProcessedFile = 0
        self.processFolder (self._BaseFolder)
        ProcessedFile = self._NumberOfProcessedFiles
        self._NumberOfProcessedFiles = 0
        return iProcessedFile


    def checkMember (self):
        validateStringValue (self._BaseFolder)
        validateStringValue (self._Extend)
        assert type (self._FileOperation) == CFileOperation
        
    def processFolder (self, psFolder):
        """Processes psFolder in an recursive way..."""
        validateStringValue (psFolder)
        #Read content of psFolder....
        baseFolderContent = os.listdir (psFolder)
        for aFolderItem in baseFolderContent:
            sAbsPath = joinToAbsPath (psFolder,aFolderItem)
            if os.path.isfile (sAbsPath):
                if isExtentMatching (PHOTO_RAW_EXT,sAbsPath):
                    if (self.performFileOperation (sAbsPath)):
                        self._NumberOfProcessedFiles += 1
            else:
                self.processFolder (sAbsPath)
                                        

    def performFileOperation (self, psFile):
        bReturn = False
        if (self._FileOperation == CFileOperation.eDELETE):
            bReturn = deleteFile (psFile)
        else:
            raise ValueError ("Unkown file operation detected")
        return bReturn
       


class CFileOperation (enum.Enum):
    """This enum represents some file opertations"""
    eDELETE = 1
    


if __name__ == "__main__":
    #selectedFolder = filedialog.askdirectory()    
    #selectedFolder = os.path.abspath (selectedFolder)
    selectedFolder = "C:\\Datenbereich\\Fotos"
    if selectedFolder != "":
        deleter = CFileIterator (selectedFolder, CFileOperation.eDELETE,  PHOTO_RAW_EXT)
        iNumberOfDeletedFiles = deleter.run()

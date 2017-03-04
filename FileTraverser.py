# -*- coding: utf-8 -*-
import os
import enum
from FileUtilities import *

cMAXFOLDERITEMS = 10000
cNUMBER_SEPERATOR = "_"


class CFileTraverser ():
    """An abstract class for traversing and file operations..."""
    def __init__ (self, psBaseFolder, psExtention):
        assertFolder (psBaseFolder)
        verifyPath (psExtention)
        self._sBaseFolder = psBaseFolder
        self._sExtention = psExtention
        self._iExecuteOperations = 0
        self._iSkippedOperations = 0
         
    def travers (self):
         """this methode traveres the file structure start at self._sBaseFolder level and rerturns the number of executed operations"""
         self._iExecuteOperations = 0
         self._iSkippedOperations = 0
         self.processFolder (self._sBaseFolder)
         self.logHintProcessedFiles ()
         self.logHintSkippedFiles ()
         return self._iExecuteOperations

    def getFileType (self):
        """ Retruns the Type of file to be process as captial letter string without leading "." """
        sFileType = self._sExtention.lstrip (".")
        sFileType = sFileType.upper()
        return sFileType

    def bIsExcludeFolder (self, psPath):
        """This provides sub classes the possibility to supress the processing of a folder, for whatever reason..."""
        return False
        
         

    def processFolder (self, psPath):
        """this method processes a folder: the defined file operation will be applied the files in this folder, sub folder
        will processed recursily"""
        # Check folder needs to be excluded from processing
        if not self.bIsExcludeFolder (psPath):
            self.logHint ("Processing folder " + psPath)
            verifyPath (psPath)
            self.preProcessFolder (psPath)
            #Read the content of the folder....
            baseFolderContent = os.listdir (psPath)
            for aFolderItem in baseFolderContent:
                #Analyse the item... folder or file?
                sAbsPath = joinToAbsPath(psPath, aFolderItem)
                if os.path.isdir (sAbsPath):
                    self.processFolder (sAbsPath)
                elif os.path.isfile (sAbsPath):
                    self.processFile (sAbsPath)
                else:                      
                    #This should never happen, item is neither file nor folder...
                    raise TypeError ("Folder item neither file nor sub folder")
            self.postProcessFolder (psPath)    
            
    def preProcessFolder (self, psPath):
        """this provides sub classes the possiblity to do some preparation before the folder gets processed..."""
        pass

    def postProcessFolder (self, psPath):
        """this provides sub classes the possiblity to do some clean up after the folder gets processed..."""
        pass

    def processFile (self, psPath):
                      
        """this method processes a single file, psFile has to be a file including it's absolute path, the method has
           to be implemented in sub classes"""
        raise NotImplementedError


    def logHint (self, psHint):                      
        print (psHint)


    def logHintProcessedFiles (self):                      
        self.logHint (str (self._iExecuteOperations) + self.getFileType() + " files processed.")

    def logHintSkippedFiles (self):                      
        self.logHint (str (self._iSkippedOperations) + self.getFileType() + " files skipped.")




class CFileTraverserDeleter (CFileTraverser):
    """This traverser walks over the file structure starting at _BaseFolder and deletes all files matching"""
    def __init__ (self, psBaseFolder, psExtention):
        CFileTraverser.__init__(self, psBaseFolder, psExtention)
        

    def processFile (self, psFile):
        """This method expects a file including its abstract path, checkes if its extention matches and deletes it, given the
        case"""
        assert os.path.isfile (psFile)
        if isExtentionMatching (self._sExtention, psFile):
            try:
                testPathWritability (psFile)
                os.remove (psFile)
                self._iExecuteOperations+=1
            except OSError:
                self._iSkippedOperations+=1
                
                
    def logHintProcessedFiles (self):
        sFileType = self._sExtention.lstrip (".")
        sFileType = sFileType.upper()
        self.logHint (str (self._iExecuteOperations) + " " + self.getFileType() +  " files deleted.")

    def logHintSkippedFiles (self):
        self.logHint (str (self._iSkippedOperations) + " " + self.getFileType() + " files were write protected and could not be deleted.")            

class CFileTraverserPhotoRenames (CFileTraverser):
    """This classe provides a traverser which renames photo files (JPG) this way:
       first part of the new name comes from the sub folder the file is in, the seconnd and last one is a running number,
       e.g: "Dezember_2016_Weihnachten_0004.jpg"""
    _TMP_FOLDER = "\\TMP_RENAME"
    def __init__ (self, psBaseFolder):
        CFileTraverser.__init__(self, psBaseFolder, PHOTO_FILE_EXT)
        self._lNextNumbersToUse = []

    def bIsExcludeFolder (self, psPath):
        bReturn = False
        #check if this a temporary folder which needs to supressed from processing...
        if psPath.find (self._TMP_FOLDER) > -1 :
            bReturn = True
        return bReturn
        
        

    def preProcessFolder (self, psPath):
        assertFolder (psPath)
        createFolder (psPath + self._TMP_FOLDER)
        self._lNextNumbersToUse.append (cNUMBER_SEPERATOR + "0001")

    def postProcessFolder (self, psPath):
        #move Photo file from temporary sub folder back to folder
        folderContent = os.listdir (psPath + self._TMP_FOLDER)
        for aFolderItem in folderContent:
            sFileOld = joinToAbsPath (psPath + self._TMP_FOLDER, aFolderItem)
            assertFile (sFileOld)
            assert (isExtentionMatching (self._sExtention, sFileOld))
            sFileNew = joinToAbsPath (psPath, aFolderItem)
            try:
                testPathWritability (psPath)
                testPathWritability (psPath + self._TMP_FOLDER)
                os.rename (sFileOld, sFileNew)
                self._iExecuteOperations+=1
            except OSError:
                self._iSkippedOperations+=1
            
        
        removeFolderStructureComplete (psPath + self._TMP_FOLDER)        
        """remove the last sub list after folder processing is done"""
        iLen = len (self._lNextNumbersToUse)
        assert iLen > 0
        del self._lNextNumbersToUse [iLen - 1] 
 
    
    def processFile (self, psFile):
        """This method does this renaming itself..."""
        assert os.path.isfile (psFile)
        if isExtentionMatching (self._sExtention, psFile):
            #Extract the folder
            sFolderComplete = getFolderFromAbsPath (psFile)
            sFileName = getFileNameWithoutExention (psFile)
            sInnerFolder = getInnerFolderFromAbsFile (psFile)
            #Check if this file has been renamed already...
            #if (sFileName.find (sInnerFolder) == -1):
            # get the sub string representing the number in order to generate a not exisiting file name
            psNumber = self.getNextNumberToUse ()
            # Generate new file name: folder name plus number...
            sNewFileName = sInnerFolder + psNumber + self._sExtention
            sAbsFile = joinToAbsPath (sFolderComplete + self._TMP_FOLDER, sNewFileName)
            #Rename the file...
            try:
                testPathWritability (psFile)
                os.rename (psFile, sAbsFile)
                self.setNextNumberToUse (self.increaseNumberStr (psNumber))
            except OSError:
                print ("Problems creating file in tmp folder:" +  sAbsFile)
                
                
                
                
    def getNumberStr (self,psFile) :
        """analyses the folder where psFile is in and returns a string like "001".  The number is the lowest one
           not included in any file name within this folder """
        assert os.path.isfile (psFile)
        sNumberStr = self.getNextNumberToUse ()
        sFolderPath = getFolderFromAbsPath (psFile)
        folderContent = os.listdir (sFolderPath)
        bIsCurrentNumberOk = False
        while (bIsCurrentNumberOk == False):
            iCurrentNumber  = 0
            bMachtingNameFound = False
            for aFolderItem in folderContent:
                #Analyse the item... folder or file?
                sAbsPath = joinToAbsPath (sFolderPath, aFolderItem)
                if os.path.isfile (sAbsPath):
                    if isExtentionMatching (PHOTO_FILE_EXT, sAbsPath):
                        iCurrentNumber += 1
                        assert (iCurrentNumber < cMAXFOLDERITEMS) 
                        if (self.doesFileNameEndWithNumberStr (aFolderItem, sNumberStr) == True):
                            sNumberStr = self.increaseNumberStr (sNumberStr)
                            bMachtingNameFound = True
                            break
                #if all file in the folder were negattivly tested against the current number string, this string is fine..
            if (bMachtingNameFound == False):
                bIsCurrentNumberOk = True
        return sNumberStr

    def increaseNumberStr (self, psNumberStr)  :
        """This function increase the number in psNumberString, so "0001" will be increased to "0002"""
        assert type (psNumberStr) == str
        sReturnStr = ""
        sWorkStr = psNumberStr.strip (cNUMBER_SEPERATOR)
        iNewNumber = int (sWorkStr) + 1
        sReturnStr = str (iNewNumber)
        if (iNewNumber < 10):
            sReturnStr = "000" + sReturnStr
        if ((iNewNumber > 9) and (iNewNumber < 100))  :
            sReturnStr = "00" + sReturnStr
        if ((iNewNumber > 99) and (iNewNumber < 1000))  :
            sReturnStr = "0" + sReturnStr
        self.setNextNumberToUse (cNUMBER_SEPERATOR + sReturnStr)
        return cNUMBER_SEPERATOR + sReturnStr
        
    def doesFileNameEndWithNumberStr (self, psAbsFile, psNumber):
        bReturn = False
        sFileName = getFileNameWithoutExention (psAbsFile)
        iLenFile = len (sFileName)
        iLenNumber = len (psNumber)
        iPosRelevant = iLenFile - iLenNumber
        if (iPosRelevant > -1):
            iPosFound = sFileName.rfind (psNumber)
            if (iPosFound == iPosRelevant):
                bReturn = True
        return bReturn


    def setNextNumberToUse (self, psNumber):
        """set the number string tried to be used next in the current folder"""
        assert type (psNumber) == str
        assert psNumber.find (cNUMBER_SEPERATOR) != -1
        iLen = len (self._lNextNumbersToUse)
        assert iLen > 0
        self._lNextNumbersToUse [iLen - 1] = psNumber

    def getNextNumberToUse (self):
        """returns the number string tried to be used next in the current folder"""
        iLen = len (self._lNextNumbersToUse)
        assert iLen > 0
        return self._lNextNumbersToUse [iLen - 1]
        
        

if __name__ == "__main__":
    renamer = CFileTraverserPhotoRenames ("C:\\Datenbereich\\Fotos\\Fotos 2017\\Februar_2017_Theresa_Julia_Fasching\\")
    renamer.travers ()
    
                      
    

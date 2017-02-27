# -*- coding: utf-8 -*-
import os
from tkinter import filedialog
from FileUtilities import *
import datetime
import shutil


class CPhotoFileSubFolderSorter ():
    """Klasse stellt einen Sortierer für Dateien bereit: 
       alle Dateien eines Verzeichnisses werden in Unterverzeichnisse einsortiert
       für jeden Tag, an dem eine der Dateien erstellt wurde, wird ein Unterverzeichnis
       egeneriert und alle entsprechenden Dateien dort einsortiert"""
    def __init__ (self, psBaseFolder):
        verifyPath (psBaseFolder)
        self._BaseFolder = psBaseFolder
        


        
    def run (self):
        """ führt die Sortierung durch"""
        verifyPath (self._BaseFolder)
        testPathWritability (self._BaseFolder)
        #Read the content of the base folder....
        baseFolderContent = os.listdir (self._BaseFolder)
        for aLocalFile in baseFolderContent:
            if self.isExtentionMatching (aLocalFile):
                self.prepareMovePhotoFileToSubFolder (aLocalFile)

    def isExtentionMatching (self, psFile):
        bReturn = False
        if ((isExtentionMatching (PHOTO_FILE_EXT, psFile) or (isExtentionMatching (PHOTO_RAW_EXT, psFile)):
            bReturn = True
        return bReturn
        

    def validateUserRights (self):
        """ Prüft ob im Verzeichnis _BaseFolder ausreichende Rechte gegeben sind  """
        if not os.access (self._BaseFolder, os.W_OK):
            raise OSError ("Keine Schreibrechte im Verzeichnis " + self._BaseFolder)

    def prepareMovePhotoFileToSubFolder (self, paLocalFile):
        """paLocalFile:  eine lokale Datei in _BaseFolder, die Methode prüft das Erstellungsdatum der Datei
           generiert, falls noch nicht vorhanden  folgende Subfolder Struktur Jahr, Monat, Tag und verschiebt die Datei
           dann entsprechend"""
        verifyPath (paLocalFile)
        subFolder = self.prepareSubFolder (paLocalFile)
        self.movePhotoFileToSubFolder (paLocalFile, subFolder)


    def prepareSubFolder (self, psLocalFile):
        verifyPath (psLocalFile)
        subFolder = ""
        subFolderYear = self.prepareSubFolderYear (psLocalFile)
        verifyPath (subFolderYear)
        subFolderMonth = self.prepareSubFolderMonth (psLocalFile,subFolderYear)
        subFolderDay = self.prepareSubFolderDay (psLocalFile,subFolderMonth)
        subFolder = subFolderDay
        return subFolder

    def prepareSubFolderYear (self, psLocalFile):
        subFolderYear = ""
        verifyPath (psLocalFile)
        fileCreationDate = self.getLocalFileCreationDate (psLocalFile)
        sYear = str (fileCreationDate.year)
        subFolderYear = self.joinToAbsPath (self._BaseFolder, sYear)
        self.ensureFolderExists (subFolderYear)     
        return subFolderYear

    def prepareSubFolderMonth (self, psLocalFile, psSubFolderYear):
        sSubFolderMonth = ""
        verifyPath (psLocalFile)
        verifyPath (psSubFolderYear)
        fileCreationDate = self.getLocalFileCreationDate (psLocalFile)
        assert fileCreationDate.month in dMonthsStr.keys ()
        sSubFolderMonth = self.joinToAbsPath (psSubFolderYear, dMonthsStr [fileCreationDate.month])
        self.ensureFolderExists (sSubFolderMonth)
        return sSubFolderMonth
        
    def prepareSubFolderDay (self, psLocalFile, psSubFolderMonth):
        sSubFolderDay = ""
        verifyPath (psLocalFile)
        verifyPath (psSubFolderMonth)
        fileCreationDate = self.getLocalFileCreationDate (psLocalFile)
        sSubFolderDay = self.joinToAbsPath (psSubFolderMonth, str (fileCreationDate.day))
        self.ensureFolderExists (sSubFolderDay)
        return sSubFolderDay

        

    def movePhotoFileToSubFolder (self, psLocalFile, psSubFolder):
        verifyPath (psLocalFile)
        verifyPath (psSubFolder)
        verifyPath (self._BaseFolder)
        shutil.move (self.joinToAbsPath (self._BaseFolder, psLocalFile), self.joinToAbsPath (psSubFolder, psLocalFile))

    def getLocalFileCreationDate(self, psLocalFile):
        absoluteFile = self.joinToAbsPath (self._BaseFolder, psLocalFile)
        t = os.path.getmtime(absoluteFile)
        return datetime.datetime.fromtimestamp(t)

    def joinToAbsPath (self, sPath1, sPath2):
        return joinToAbsPath(sPath1, sPath2)
    

    def ensureFolderExists (self, psFolder):
        verifyPath (psFolder)
        if not os.path.exists (psFolder):
            os.mkdir (psFolder)
            
        


#Dictionary zur Konvertierung der Monate in Strings...
dMonthsStr = {1 : "Januar", 2: "Februar", 3: "März", 4 : "Arpil", 5: "Mai", 6: "Juni",7: "Juli", 8: "August",
              9: "September", 10: "Oktober", 11: "November", 12: "Dezember"}    


    
if __name__ == "__main__":
    selectedFolder = filedialog.askdirectory()    
    selectedFolder = os.path.abspath (selectedFolder)
    if selectedFolder != "":
        sorter = CPhotoFileSubFolderSorter (selectedFolder)
        sorter.run()

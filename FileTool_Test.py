# -*- coding: utf-8 -*-

import unittest
from FileUtilities import *
from FileTraverser import *

c_BASE_FOLDER_FOR_TEST = "K:\\Datenbereich\\hagen\\Entwicklung\\Python\\Test"

# Ableitung von unittest.TestCase temprorär entfernt
class CPhotoRenameTest (unittest.TestCase):
    def setUp (self):
        self._bReadyForTest = False
        self._sPhotoFolder1 = c_BASE_FOLDER_FOR_TEST + "\\" +  "Januar_2019_Ausflug_Marssee"
        self._sPhotoFolder2 = c_BASE_FOLDER_FOR_TEST + "\\" +  "Februar_2019_Besuch_Siegfried"
        self._sPhotoFolder3 = c_BASE_FOLDER_FOR_TEST + "\\" +  "Oktober_2019_Urlaub"
        self.prepareTestData ()

    def tearDown (self):
        self.removeTestData ()

    def removeTestData (self):
        try:
            removeFolderStructureComplete (self._sPhotoFolder1)
            removeFolderStructureComplete (self._sPhotoFolder2)
            removeFolderStructureComplete (self._sPhotoFolder3)
            self._bReadyForTest = False
        except:
            print ("Testen konnten nicht entfernt werden")
                

                

    def testPhotoRenaming (self):
        self.runTest ()
        self.analyseResults ()

    def prepareTestData (self):
        self.removeTestData ()
        sDriveTestData =  getDriveFromAbsPath (c_BASE_FOLDER_FOR_TEST)
        if doesDriveExist (sDriveTestData) :
            try:
                createFolderStructure (self._sPhotoFolder1 + "\\" + "Photodata")
                createFolderStructure (self._sPhotoFolder1 + "\\" + "tmp")
                createFolderStructure (self._sPhotoFolder2 + "\\" + "tmp")
                createFolderStructure (self._sPhotoFolder3)
                self._bReadyForTest =  True
            except:
                print ("Ordner für Test der Fotoumbenennung konnten nicht anlegt werden. Abbruch des Tests")
                
        try:
            #Prepare test folder 1
            createFile (self._sPhotoFolder1, "list.txt")
            createFile (self._sPhotoFolder1, "CMI.jpg")
            createFile (self._sPhotoFolder1, "CMI567.jpg")
            createFile (self._sPhotoFolder1, "CMI043.jpg")
            createFile (self._sPhotoFolder1, "567.jpg")
            #Prepare test folder 2
            createFile (self._sPhotoFolder2, "list.dwh")
            createFile (self._sPhotoFolder2, "_34.jpg")
            createFile (self._sPhotoFolder2, "rte_34.jpg")
            createFile (self._sPhotoFolder2, "fgt_45.jpd")
            createFile (self._sPhotoFolder2, "545.jpg")
            #Prepare test folder 3
            createFile (self._sPhotoFolder3, "list.dwh")
            createFile (self._sPhotoFolder3, "_34.jpg")
            createFile (self._sPhotoFolder3, "rte_34.jpg")
            createFile (self._sPhotoFolder3, "fgt_45.jpd")
            createFile (self._sPhotoFolder3, "545.jpg")
        except:
            print ("Testdateien konnten nicht vollständig erzeugt werden")
        
    def runTest (self):
        oRename =  CFileTraverserPhotoRenamer (self._sPhotoFolder1)
        oRename.travers ()
        oRename =  CFileTraverserPhotoRenamer (self._sPhotoFolder2)
        oRename.travers()
        oRename =  CFileTraverserPhotoRenamer (self._sPhotoFolder3)
        oRename.travers()
        
    def analyseResults (self):
        #-----------------------------
        folder1Content = os.listdir (self._sPhotoFolder1)
        iNumberItemsFolder1 = len (folder1Content)
        self.assertEqual (iNumberItemsFolder1, 7)
        #------------------------------------
        folder2Content = os.listdir (self._sPhotoFolder2)
        iNumberItemsFolder2 = len (folder2Content)
        self.assertEqual (iNumberItemsFolder2, 6)
        #-------------------------------------
        folder3Content = os.listdir (self._sPhotoFolder3)
        iNumberItemsFolder3 = len (folder3Content)
        self.assertEqual (iNumberItemsFolder3, 5)
        self.analyseTestFolderContent(self._sPhotoFolder1)
        self.analyseTestFolderContent(self._sPhotoFolder2)
        self.analyseTestFolderContent(self._sPhotoFolder3)
        
        

    def analyseTestFolderContent(self, psAbsFolder):
        verifyPath (psAbsFolder)
        folderContent = os.listdir (psAbsFolder)
        for aFolderItem in folderContent:
            sAbsPath = joinToAbsPath(psAbsFolder, aFolderItem)
            if os.path.isfile (sAbsPath):
                if isExtentionMatching (PHOTO_FILE_EXT, sAbsPath):
                    self.verifyPhotoFileName (sAbsPath)

                
    def verifyPhotoFileName (self, psAbsPathFile):
        assertFile (psAbsPathFile)
        assert (isExtentionMatching (PHOTO_FILE_EXT, psAbsPathFile))
        sFileNameWithoutExention = getFileNameWithoutExention (psAbsPathFile)
        sInnerFolder = getInnerFolderFromAbsFile (psAbsPathFile)
        self.assertTrue (sInnerFolder in sFileNameWithoutExention)
        self.assertTrue ('_' in sFileNameWithoutExention)
        self.assertTrue (any (s in sFileNameWithoutExention for s in ['0' , '1', '2', '3', '4', '5', '6', '7', '8', '9']))
        
        
        
        
        

if __name__ == "__main__":
    unittest.main()
    
    


 

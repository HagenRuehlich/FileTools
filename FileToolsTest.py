# -*- coding: utf-8 -*-
import os
import unittest
from FileTraverser import *
from FileUtilities import *


class CRawFileDeleteTest (unittest.TestCase):
    _TEST_FOLDER = "C:\\Datenbereich\\hagen\\testfolder"
    _TEST_FOLDER_LEVEL2 = _TEST_FOLDER + "\\TestFolderLevel2"
    _TEST_FOLDER_LEVEL3 = _TEST_FOLDER_LEVEL2 + "\\TestFolderLevel3"
    def testRawFileDeleting (self):
        #prepare a temporary strturce for testing
        self.prepapreTestStructure ()
        #run the RAW deleter
        deleter = CFileTraverserDeleter (self._TEST_FOLDER, PHOTO_RAW_EXT)
        deleter.travers ()
        #Analye the results of the process
        self.analyseResults ()
        #Remove the tempory strucure
        self.removeTestStructure ()
        

    def prepapreTestStructure (self):
        createFolder (self._TEST_FOLDER)
        #create some files in this folder..
        createFile (self._TEST_FOLDER, "test1.txt")
        createFile (self._TEST_FOLDER, "test2" +  PHOTO_FILE_EXT)
        createFile (self._TEST_FOLDER, "test3" +  PHOTO_RAW_EXT)
        createFolder (self._TEST_FOLDER_LEVEL2)
        #create some files in this folder..
        createFile (self._TEST_FOLDER_LEVEL2, "test4" + PHOTO_RAW_EXT)
        createFile (self._TEST_FOLDER_LEVEL2, "test5" +  PHOTO_RAW_EXT)   
        createFile (self._TEST_FOLDER_LEVEL2, "test6" +  PHOTO_RAW_EXT)
        createFolder (self._TEST_FOLDER_LEVEL3)
        #create some files in this folder..
        createFile (self._TEST_FOLDER_LEVEL3, "test7.txt")
        createFile (self._TEST_FOLDER_LEVEL3, "test8" +  PHOTO_RAW_EXT)
        createFile (self._TEST_FOLDER_LEVEL3, "test9" +  PHOTO_FILE_EXT)  
        
        
    def analyseResults (self):
        #Analye the results of the process, Level 1
        self.analyseTestFolder (self._TEST_FOLDER, 3)
        self.analyseTestFolder (self._TEST_FOLDER_LEVEL2, 1)
        self.analyseTestFolder (self._TEST_FOLDER_LEVEL3, 2)
        
        
    def analyseTestFolder (self, psFolder, piCheckNum):
        testFolderContent = os.listdir (psFolder)
        iNumFiles = len (testFolderContent)
        self.assertEqual (iNumFiles, piCheckNum)
        for aFolderItem in testFolderContent:
            fileAbsPath = joinToAbsPath (psFolder, aFolderItem)
            sExt = getFileExtention (fileAbsPath)
            bMatch = isExtentionMatching (PHOTO_RAW_EXT, fileAbsPath)
            self.assertEqual (bMatch, False)
            
    def removeTestStructure (self):
        removeFolderStructureComplete (self._TEST_FOLDER)


class CPhotoFileRenameTest (unittest.TestCase):
    _TEST_FOLDER = "C:\\Datenbereich\\hagen\\testPhotos"
    _TEST_FOLDER_LEVEL2_NAME = "testPhotoLevel2"
    _TEST_FOLDER_LEVEL2 = _TEST_FOLDER + "\\" + _TEST_FOLDER_LEVEL2_NAME
    _TEST_FOLDER_LEVEL31_NAME = "testPhoto_Topic1"
    _TEST_FOLDER_LEVEL31 = _TEST_FOLDER_LEVEL2 + "\\" + _TEST_FOLDER_LEVEL31_NAME
    _TEST_FOLDER_LEVEL32_NAME = "testPhoto_Topic2"
    _TEST_FOLDER_LEVEL32 = _TEST_FOLDER_LEVEL2 + "\\" + _TEST_FOLDER_LEVEL32_NAME

    def testPhotoFileRenaming (self):
        self.removeTestStructure ()
        #prepare a temporary struturce for testing
        self.prepapreTestStructure ()
        #run the Renamer
        renamer = CFileTraverserPhotoRenames (self._TEST_FOLDER)
        renamer.travers ()
        #Analye the results of the process
        self.analyseResults ()
        #Remove the tempory strucure
        self.removeTestStructure ()
        
    def prepapreTestStructure (self):
        createFolder (self._TEST_FOLDER)
        createFolder (self._TEST_FOLDER_LEVEL2)
        createFile (self._TEST_FOLDER_LEVEL2, "Photo1" + PHOTO_FILE_EXT)
        createFile (self._TEST_FOLDER_LEVEL2, "Photo1_0003" + PHOTO_FILE_EXT)
        sInnerFolder = getInnerFolderFromAbsFile (self._TEST_FOLDER_LEVEL2 + "\\Photo1_0003" + PHOTO_FILE_EXT)
        createFile (self._TEST_FOLDER_LEVEL2, sInnerFolder + "_0002" + PHOTO_FILE_EXT)
        #----------------------------------------------------------------------------------------------------
        createFolder (self._TEST_FOLDER_LEVEL31)
        createFile (self._TEST_FOLDER_LEVEL31, "0001" + PHOTO_FILE_EXT)
        createFile (self._TEST_FOLDER_LEVEL31, "Photo1_0001" + PHOTO_FILE_EXT)
        sInnerFolder = getInnerFolderFromAbsFile (self._TEST_FOLDER_LEVEL31 + "\\Photo1_0001" + PHOTO_FILE_EXT)
        createFile (self._TEST_FOLDER_LEVEL31, sInnerFolder + "_0002" + PHOTO_FILE_EXT)
        #------------------------------------------------------------------------------------------------------
        createFolder (self._TEST_FOLDER_LEVEL32)
        createFile (self._TEST_FOLDER_LEVEL32, "0001" + PHOTO_FILE_EXT)
        createFile (self._TEST_FOLDER_LEVEL32, "Photo1_0001" + PHOTO_FILE_EXT)
        sInnerFolder = getInnerFolderFromAbsFile (self._TEST_FOLDER_LEVEL32 + "\\Photo1_0001" + PHOTO_FILE_EXT)
        createFile (self._TEST_FOLDER_LEVEL32, sInnerFolder + "_0002.txt")
                     
    def analyseResults (self):
        self.analyseTestFolder ()
        self.analyseTestFolderLevel2 ()
        self.analyseTestFolderLevel31 ()
        self.analyseTestFolderLevel32 ()

    def analyseTestFolder (self):
        bExists = os.path.exists (self._TEST_FOLDER)
        self.assertEqual (bExists, True)
        testFolderContent = os.listdir (self._TEST_FOLDER)
        iNumItems = len (testFolderContent)
        self.assertEqual (iNumItems, 1)
        for aFolderItem in testFolderContent:
            self.assertEqual (aFolderItem, self._TEST_FOLDER_LEVEL2_NAME)
            bIsFolder =  isJoinedAbsPathFolder (self._TEST_FOLDER, aFolderItem)
            self.assertEqual (bIsFolder, True)
            sAbsPath = joinToAbsPath (self._TEST_FOLDER, aFolderItem)
            iFindIndex = sAbsPath.find (self._TEST_FOLDER_LEVEL2)
            self.assertGreater (iFindIndex, -1)
             
        
    def analyseTestFolderLevel2 (self) :
        bExists = os.path.exists (self._TEST_FOLDER_LEVEL2)
        self.assertEqual (bExists, True)
        testFolderContent = os.listdir (self._TEST_FOLDER_LEVEL2)
        iNumItems = len (testFolderContent)
        self.assertEqual (iNumItems, 5)
        tResult = (self._TEST_FOLDER_LEVEL31_NAME, self._TEST_FOLDER_LEVEL32_NAME, self._TEST_FOLDER_LEVEL2_NAME + "_0001" + PHOTO_FILE_EXT, self._TEST_FOLDER_LEVEL2_NAME + "_0002" + PHOTO_FILE_EXT, self._TEST_FOLDER_LEVEL2_NAME + "_0003" + PHOTO_FILE_EXT)
        for aFolderItem in testFolderContent:
            bIsIn = aFolderItem in tResult
            self.assertEqual (True, bIsIn)
        
        
        
        

    def analyseTestFolderLevel31 (self) :
        bExists = os.path.exists (self._TEST_FOLDER_LEVEL31)
        self.assertEqual (bExists, True)
        testFolderContent = os.listdir (self._TEST_FOLDER_LEVEL31)
        iNumItems = len (testFolderContent)
        self.assertEqual (iNumItems, 3)
        tResult = (self._TEST_FOLDER_LEVEL31_NAME + "_0001" + PHOTO_FILE_EXT, self._TEST_FOLDER_LEVEL31_NAME + "_0002" + PHOTO_FILE_EXT, self._TEST_FOLDER_LEVEL31_NAME + "_0003" + PHOTO_FILE_EXT)
        for aFolderItem in testFolderContent:
            bIsIn = aFolderItem in tResult
            self.assertEqual (True, bIsIn)
       
    

    def analyseTestFolderLevel32 (self) :
        bExists = os.path.exists (self._TEST_FOLDER_LEVEL32)
        self.assertEqual (bExists, True)
        testFolderContent = os.listdir (self._TEST_FOLDER_LEVEL32)
        iNumItems = len (testFolderContent)
        self.assertEqual (iNumItems, 3)
        tResult = (self._TEST_FOLDER_LEVEL32_NAME + "_0001" + PHOTO_FILE_EXT, self._TEST_FOLDER_LEVEL32_NAME + "_0002" + PHOTO_FILE_EXT, self._TEST_FOLDER_LEVEL32_NAME + "_0002.txt")
        for aFolderItem in testFolderContent:
            self.assertEqual (True, aFolderItem in tResult)
    

    def removeTestStructure (self):
        #Check if the test data structure already exists, if so, remove it
        if os.path.exists (self._TEST_FOLDER):
            removeFolderStructureComplete (self._TEST_FOLDER)
        
                                              
                                              



if __name__ == "__main__":
    unittest.main()        

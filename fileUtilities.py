# -*- coding: utf-8 -*-
import os

def validateStringValue (psValue):
        assert type (psValue) == str
        assert psValue != ""

        
def isExtentMatching (psExtend, psFile):
        validateStringValue (psFile)
        validateStringValue (psExtend)
        bReturn = False
        sExtend = os.path.splitext (psFile)[1]
        sExtend = sExtend.lower()
        if (sExtend == psExtend):
                bReturn = True
        return bReturn

def validateUserRights (psPath):
        """ checkes if psPath is writeable """
        if not os.access (psPath, os.W_OK):
            raise OSError ("No writing access to " + psPath)


def deleteFile (psFile):
        validateStringValue (psFile)
        try:
                validateUserRights (psFile)
        except OSError:
                return False;
        os.remove (psFile)
        return True
        
def joinToAbsPath (psPath1, psPath2):
        """joins the two paramter to one absolute path and returns it"""
        validateStringValue (psPath1)
        validateStringValue (psPath2)
        sReturnPath = os.path.join (psPath1, psPath2)
        sReturnPath = os.path.abspath (sReturnPath)
        return sReturnPath        
        
        

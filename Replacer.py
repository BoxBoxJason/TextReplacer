# -*- coding: utf-8 -*-
'''
Created on 21 juil. 2023

@author: BoxBoxJason
'''
import logging
import os
import re


def replaceText(filePath,regexDict):
    """
    Replaces text in file according to the regexDict given
    :param (path) filePath : (absolute) path to file that needs to be edited
    :param (dict) regexDict : dictionary of all regex that need to be replaced {regex to replace:replacing value}
    """
    try:
        # Getting text from template file
        with open(filePath,'r',encoding="utf-8") as originalFile:
            rawText = originalFile.read()
    
        # Replacing text in raw template text
        for regex,value in regexDict.items():
            rawText,count = re.subn(regex,str(value),rawText)
            logging.info(f"Replaced {count} occurences of {regex} in {filePath}")
    
        # Writing text in destination file
        with open(filePath,'w',encoding="utf-8") as destinationFile:
            destinationFile.write(rawText)
        logging.debug(f"End of generation, result script in {filePath}")

    except UnicodeDecodeError:
        logging.fatal(f"Invalid encoding for file {filePath}, please convert to utf-8")


def exploreDir(dirPath,regexDict):
    """
    Explores directory, launches a text replacement if child is a file,
    explores if child is a directory
    :param (path) dirPath : (absolute) path to the directory to explore
    :param (dict) regexDict : dictionary of all regex that need to be replaced {regex to replace:replacing value}
    """
    for childName in os.listdir(dirPath):
        childPath = os.path.join(dirPath,childName)
        if os.path.isdir(childPath):
            if os.access(childPath,os.R_OK):
                exploreDir(childPath,regexDict)
            else:
                logging.error(f"Access denied to {childPath}")
        else:
            if os.access(childPath,os.R_OK) and os.access(childPath,os.W_OK):
                replaceText(dirPath,regexDict)
            else:
                logging.error(f"Read or write access denied to {childPath}")

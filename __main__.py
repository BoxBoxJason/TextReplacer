# -*- coding: utf-8 -*-
"""
Created on 21 juil. 2023

User friendly tool to replace certain text patterns in your project folders / files

Replaces regular text or text pattern (regex) of your project.
You can input as many patterns / words / phrases / letters to change as you wish
Replacements have to be specified in a .json file, the format should be:
        { "[Regex pattern to replace]" : "New Text",
          "Text to replace" : "New Text 2"
        }

Requires at least one argument: source folder/file path (absolute or relative)
As second argument, you can specify another path for replacement .json file, the default value is replaceDict.json

Be careful, there will be no confirmation message and changes cannot be undone

@author: BoxBoxJason
"""

import json
from json.decoder import JSONDecodeError
import logging
import os
import sys
import re


##---------- Replacer Functions ----------##

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


##---------- Logging setup ----------##
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__),"logging.log")),
        logging.StreamHandler(sys.stdout)
    ]
)

# Unpacking arguments given
if len(sys.argv) < 2:
    logging.fatal("Incorrect number of arguments, please give at least the path to source")
    sys.exit(1)

elif len(sys.argv) > 3:
    logging.fatal("Incorrect number of arguments, please give at most path to source and path to replacement configuration .json file")
    sys.exit(1)

elif len(sys.argv) == 3:
    replaceDictPath = sys.argv[2]

else:
    replaceDictPath = os.path.join(os.path.dirname(__file__),"replaceDict.json")

rootFilePath = sys.argv[1]


if not os.path.exists(rootFilePath) or not os.access(rootFilePath,os.R_OK):
    logging.fatal(f"File or directory access denied or not found at {rootFilePath}")
    sys.exit(1)
if not os.path.exists(replaceDictPath) or not os.access(replaceDictPath,os.R_OK):
    logging.fatal(f"Replacement config .json file access denied or not found at {replaceDictPath}")
    sys.exit(1)

try:
    with open(replaceDictPath,'r',encoding="utf-8") as jsonFile:
        regexDict = json.load(jsonFile)
except (JSONDecodeError,TypeError):
    logging.fatal(f"Could not parse file {replaceDictPath} into dict, please check its format")
    sys.exit(1)

logging.debug("Starting replacement")
if os.path.isdir(rootFilePath):
    exploreDir(rootFilePath,regexDict)
else:
    replaceText(rootFilePath,regexDict)

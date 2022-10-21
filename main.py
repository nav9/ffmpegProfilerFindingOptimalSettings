'''
FFMPEG Profiler. To help with finding the optimal settings for encoding videos, using minimal resources.
Created on 21-Oct-2022
@author: Navin
'''

import sys
sys.dont_write_bytecode = True #Prevents the creation of some annoying cache files and folders. This line has to be present before all the 
import logging
from logging.handlers import RotatingFileHandler
from programConstants import constants as const
from fileAndFolder import fileFolderOperations, reports

#TODO: shift log file config to file
logFileName = 'logs_ffmpeg.log'
loggingLevel = logging.INFO
logging.basicConfig(level=loggingLevel, format='%(levelname)s %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S') #outputs to console
#log = logging.getLogger(__name__)
handler = RotatingFileHandler(logFileName, maxBytes=2000000, backupCount=2)#TODO: Shift to config file
handler.formatter = logging.Formatter(fmt='%(levelname)s %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S') #setting this was necessary to get it to write the format to file. Without this, only the message part of the log would get written to the file
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(loggingLevel)

if __name__ == '__main__':
    fileOps = fileFolderOperations.FileOperations()
    report = reports.Reports(const.GlobalConstants.reportFolder, fileOps)
    profilers = []
    videoFilesToProcess = fileOps.getNamesOfVideoFilesToProcess(const.GlobalConstants.originalVideoFilesFolder, const.GlobalConstants.supportedFormats)
    report.add("Processing: " + str(videoFilesToProcess))
    for video in videoFilesToProcess:
        pass
    
    report.generateReport(True)
    
    
    
    

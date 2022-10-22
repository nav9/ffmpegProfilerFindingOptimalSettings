import os
import time
import shlex
import psutil
import subprocess
import logging
from logging.handlers import RotatingFileHandler
from programConstants import constants as const

#TODO: shift log file config to file
logFileName = 'logs_ffmpeg.log'
loggingLevel = logging.INFO
logging.basicConfig(level=loggingLevel, format='%(levelname)s %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S') #outputs to console
#log = logging.getLogger(__name__)
handler = RotatingFileHandler(logFileName, maxBytes=2000000, backupCount=2)#TODO: Shift to config file
handler.formatter = logging.Formatter(fmt='%(levelname)s %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S') #setting this was necessary to get it to write the format to file. Without this, only the message part of the log would get written to the file
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(loggingLevel)

class Parameter:
    def __init__(self, parameterName, parameterValues):
        self.name = parameterName
        if not parameterValues:#list is empty
            raise IndexError(f"{parameterName} has no corresponding values supplied")
        self.values = parameterValues
        self.temp = self.values[:] #copying values
        self.index = None
    
    def getNewParameterValue(self, previousResultWasGood):#This function should not be called without a reset, once exhaustedOptions is True
        exhaustedOptions = False
        if previousResultWasGood == None: #being called the first time since a reset or initialization
            self._moveIndexToMiddleOfList()
            parameterValue = self.temp[self.index]            
        else:
            if len(self.temp) == 1:#the only parameter left. No more to bisect
                parameterValue = self.temp[const.GlobalConstants.FIRST_POSITION_IN_LIST]
                exhaustedOptions = True
            else:#the list has more than one parameters remaining
                if previousResultWasGood:#the previous parameter returned, resulted in a good quality video
                    self.temp = self.temp[self.index:] #slice list from the previous index to the end of the list to try out a worse parameter
                else:
                    self.temp = self.temp[:self.index] #slice list from the start to just before the previous index to try out a better parameter
                self._moveIndexToMiddleOfList() #move the index to the middle of the newly sliced smaller list
                parameterValue = self.temp[self.index] #new parameter value
        if len(self.temp) <= 2:#if there are 2 or less items in the list
            exhaustedOptions = True                
        return parameterValue, exhaustedOptions          

    def _moveIndexToMiddleOfList(self): #if list is empty (which it shouldn't ever be, this function will throw an error)
        self.index = int(len(self.temp) / 2)
    
    def reset(self):
        self.temp = self.values[:]
        self.index = None
        
    def getParameterName(self):
        return self.name
    
#-------------------------------------------------------
#--- Selectors. Helps with selecting encoding parameters
#-------------------------------------------------------
class BinarySearchSelector:
    def __init__(self):        
        self.parameters = [] 
        self.parameters.append(Parameter(const.EncodingParameters.PRESET, const.EncodingParameters.preset_values))
        self.parameters.append(Parameter(const.EncodingParameters.CRF, const.EncodingParameters.CRF_values))
        self.selectedParameters = dict() #From Python 3.6 onwards, the standard dict type maintains insertion order by default.
    
    def getParameters(self):#should return an empty dict if no more parameters are there to process
        previousResultWasGood = None
        for parameter in self.parameters:#TODO: needs to be more elaborate
            parameterValue, areOptionsExhausted = parameter.getNewParameterValue(previousResultWasGood)
            self.selectedParameters[parameter.getParameterName()] = str(parameterValue)
        return self.selectedParameters


class EvolutionarySearchSelector: #another way of selecting parameters
    def __init__(self):
        pass
        

#-------------------------------------------------------
#--- Profiling engine. Starts and monitors encoding
#-------------------------------------------------------    
class Profiler:
    def __init__(self, fileOps, report):        
        self.fileOps = fileOps
        self.report = report
        self.parameterSelector = BinarySearchSelector() #TODO: could pass this as a parameter to decouple
        self.currentParameters = None
        self.bestParametersSoFar = None #parameters approved by the User or video quality evaluation function
        
    def startTrials(self, videoFile):
        logging.info(f"\n\nStarting trials for video: {videoFile}")
        self.currentParameters = self.parameterSelector.getParameters() #will return an empty string if no more parameters are generated
        while self.currentParameters:
            self._beginEncoding(videoFile)
            self.currentParameters = self.parameterSelector.getParameters()
    
    def _beginEncoding(self, originalFile):
        self.fileOps.createDirectoryIfNotExisting(const.GlobalConstants.encodedVideoFilesFolder)
        #---create a folder to store various encoded videos of this video
        videoName, extension = self.fileOps.getFilenameAndExtension(originalFile)
        folderForThisVideo = os.path.join(const.GlobalConstants.encodedVideoFilesFolder, videoName, "")#the quotes in the end add a folder slash
        self.fileOps.createDirectoryIfNotExisting(folderForThisVideo)        
        #---create the command for encoding
        parameters = ""
        outputFilename = ""
        for name, value in self.currentParameters.items(): #From Python 3.6 onwards, the standard dict type maintains insertion order by default.
            outputFilename += f"{name}{value}_"
            parameters += f" {name} {value} " #Note: the spaces are important
        
        outputFilename += ".mp4" #TODO: add proper extension
        outputFilename = os.path.join(folderForThisVideo, outputFilename)
        command = shlex.split(f"ffmpeg -y -i {originalFile} -c:a copy -c:v libx264 {parameters} {outputFilename}")       
        #---Run command https://stackoverflow.com/questions/4256107/running-bash-commands-in-python
        logging.info("\n---------------------\n--- NEW RUN\n---------------------")
        logging.info(f"Running: {command}")
        try:
            #process = subprocess.run(command, stdout = subprocess.PIPE) #https://docs.python.org/3/library/subprocess.html#module-subprocess
            ffmpegProcess = subprocess.Popen(command) #https://stackoverflow.com/questions/636561/how-can-i-run-an-external-command-asynchronously-from-python
            logging.info(f"Process id: {ffmpegProcess.pid}")            
            #---Keep polling to check if the ffmpegProcess completed and perform profiling too
            ffmpegProcessRepresentation = psutil.Process(pid = ffmpegProcess.pid) #https://psutil.readthedocs.io/en/latest/index.html?highlight=oneshot#processes
            processStartTime = ffmpegProcessRepresentation.create_time(); processEndTime = processStartTime
            logging.info(f"Process start time: {processStartTime}")
            while True:
                returnCode = ffmpegProcess.poll()
                if returnCode == None: #process still running
                    try:
                        self._performProfiling(ffmpegProcessRepresentation)
                    except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
                        logging.error(f"Unable to profile this process: {e}")
                else: #process completed
                    processEndTime = int(time.time())
                    logging.info(f"Finished encoding {videoName}")
                    break
        except subprocess.CalledProcessError as e:
            logging.error(f"The encoding ran into some errors: {e}") #TODO: handle this elegantly
        
        
    def _performProfiling(self, processRepresentation): #https://stackoverflow.com/questions/70724655/how-to-get-ram-and-cpu-time-consumption-python-app-on-linux
        with processRepresentation.oneshot():
            while processRepresentation.status() == 'running':
                print(f"Name: {processRepresentation.name()}")  # execute internal routine once collecting multiple info
                print(f"CPU Time:{processRepresentation.cpu_times()}")  # return cached value
                print(f"Memory: {processRepresentation.memory_info().vms}")  # return cached value
                print(f"CPU Percent: {processRepresentation.cpu_percent()}")  # return cached value
                print(f"Creation time: {processRepresentation.create_time()}")  # return cached value
                print(f"ppid: {processRepresentation.ppid()}")  # return cached value
                print(f"status: {processRepresentation.status()}")  # return cached value
        time.sleep(10)
        
    
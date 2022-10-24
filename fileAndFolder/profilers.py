import os
import time
import shlex #useful for recognizing quotes inside a command to be split
import numpy
import psutil
import subprocess
from collections import deque
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
    def __init__(self, nextParameter, parameterName, parameterValues):
        self.nextParameter = nextParameter #the next parameter in the chain of parameters. This will be None at the end of the chain
        self.name = parameterName
        if not parameterValues:#list is empty
            raise IndexError(f"{parameterName} has no corresponding values supplied")
        self.values = parameterValues
        self.optionsExhausted = False #becomes true when no more bisection is possible
        self.leftIndex = None        
        self.rightIndex = None
        self.midIndex = None
        self.resetIndices()
        
    def getParameterValue(self):#used in the test cases
        return self.values[self.midIndex]
    
    def isThisParameterExhausted(self):#used in the test cases
        return self.optionsExhausted
        
    def createNewParameterValue(self, previousResultWasGood):#This function should not be called without a reset, once exhaustedOptions is True
        if self.deepExhaustionCheck(self.name):
            if previousResultWasGood:                
                self._moveLeftIndexToMid()
                print(f"{self.name} Moved left index. mid index is now {self.midIndex} for {self.values}")
            else:
                self._moveRightIndexToMid()
                print(f"{self.name} Moved right index. mid index is now {self.midIndex} for {self.values}")
            if self.nextParameter:
                print(f"initiating deep reset at {self.name} {self.values}")                
                self.deepReset(self.name)#reset all child Parameters in the chain
        else:
            print(f"Going deeper from {self.name}")
            self.nextParameter.createNewParameterValue(previousResultWasGood)
    
    def _recalculateMidIndex(self):
        if len(self.values) == 1:#single element
            self.midIndex = const.GlobalConstants.FIRST_POSITION_IN_LIST
            self.optionsExhausted = True
        else:
            self.midIndex = self.leftIndex + int((self.rightIndex - self.leftIndex) / 2)
            if self.midIndex == self.leftIndex or self.midIndex == self.rightIndex:
                print(f"Marking options exhausted in {self.name}")
                self.optionsExhausted = True

    def _moveLeftIndexToMid(self):#when result is good
        print(f"Moving left index to mid for {self.name}")
        self.leftIndex = self.midIndex        
        self._recalculateMidIndex()
        print(f"left {self.leftIndex}, mid {self.midIndex}, right {self.rightIndex}")
        if self.leftIndex == self.midIndex: #if even mid recalculation caused mid not to move, it's because the options are down to 2
            self.midIndex += 1 #since mid index didn't move during recalculateMidIndex, manually move it to the only remaining option
            self.optionsExhausted = True
            print(f"Marking options exhausted in {self.name}")
        
    def _moveRightIndexToMid(self):#when result is bad
        print(f"Moving right index to mid for {self.name}")
        self.rightIndex = self.midIndex
        self._recalculateMidIndex()        
        print(f"left {self.leftIndex}, mid {self.midIndex}, right {self.rightIndex}")
        if self.rightIndex == self.midIndex: #if even mid recalculation caused mid not to move, it's because the options are down to 2
            self.midIndex -= 1 #since mid index didn't move during recalculateMidIndex, manually move it to the only remaining option
            self.optionsExhausted = True
            print(f"Marking options exhausted in {self.name}")
    
    def retrieveAllParameterNamesAndValues(self, dictReference):
        dictReference[self.name] = self.values[self.midIndex]
        if self.nextParameter:
            self.nextParameter.retrieveAllParameterNamesAndValues(dictReference)
        
    def resetIndices(self):        
        self.leftIndex = const.GlobalConstants.FIRST_POSITION_IN_LIST        
        self.rightIndex = len(self.values) - 1 
        self._recalculateMidIndex() 
        self.optionsExhausted = False  
        if self.midIndex == self.leftIndex or self.midIndex == self.rightIndex:
            self.optionsExhausted = True           
        
    def deepReset(self, invoker): #resets this and all lower elements in the chain
        print(f"Resetting everything below {self.name}")
        if self.name != invoker:
            self.resetIndices()
        if self.nextParameter:#reset all next parameters in the chain
            self.nextParameter.deepReset(invoker)
    
    def deepExhaustionCheck(self, invokerName): #returns True if all lower elements in the chain have options exhausted. When invoked with invokerName==None, it considers even the current optioinsExhausted state      
        if self.nextParameter:#proceed only if there's a next element and if current value is True (because even a single False should return False)
            allDeeperElementsOptionsExhausted = self.nextParameter.deepExhaustionCheck(invokerName)        
        else:
            allDeeperElementsOptionsExhausted = True #default, for the case where there is no nextParameter
        if invokerName == self.name:#don't consider self exhaustion. The objective is to check for exhaustion of all lower elements
            pass
        else:#this condition will happen when inside the chain or for example, when the highest calling function checks if all Parameters are exhausted. invokerName will be None
            if self.optionsExhausted == False or allDeeperElementsOptionsExhausted == False:#if there's a even a single False detected along the chain, the end result given to the caller has to be False
                allDeeperElementsOptionsExhausted = False
        return allDeeperElementsOptionsExhausted

#-------------------------------------------------------
#--- Selectors. Helps with selecting encoding parameters
#-------------------------------------------------------
class BinarySearchSelector:
    def __init__(self, parameterChain):        
        #---Using Decorator Design Pattern to chain Parameter objects
        self.param = parameterChain
        self.selectedParameters = dict() #From Python 3.6 onwards, the standard dict type maintains insertion order by default.
        self.nothingMoreToProcess = False
        self.param.retrieveAllParameterNamesAndValues(self.selectedParameters) #retrieve first chain of parameters. When Parameter is initialized, all indexes of parameter values will be at mid position
    
    def setNewParameters(self, previousResultWasGood):#should return an empty dict if no more parameters are there to process
        self.nothingMoreToProcess = self.param.deepExhaustionCheck(None)
        print("nothingMoreToProcess: ", self.nothingMoreToProcess, "previousResultSupplied: ", previousResultWasGood)
        if self.nothingMoreToProcess:
            self.selectedParameters = None
        else:
            self.param.createNewParameterValue(previousResultWasGood)            
            #---collect the generated parameters (it goes through the chain of Parameter objects, adding name, value pairs to the dict)
            self.param.retrieveAllParameterNamesAndValues(self.selectedParameters)

    def getParameters(self):
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
        param = None
        param = Parameter(param, const.EncodingParameters.CRF, const.EncodingParameters.CRF_values)
        param = Parameter(param, const.EncodingParameters.PRESET, const.EncodingParameters.preset_values)        
        self.parameterSelector = BinarySearchSelector(param) #TODO: could pass this as a parameter to decouple
        self.currentParameters = None
        self.bestParametersSoFar = None #parameters approved by the User or video quality evaluation function
        self.capturedData = dict() #could also have this as a class     
        self.numberOfCPUs = psutil.cpu_count(logical = True) #os.cpu_count() 
        self.originalFileSize = None  
        self.earlierEncodingTrialResultWasGood = None #The User was satisfied with the previous trial of a video's encoding
        
    def startTrials(self, videoFile): #tries various FFMPEG parameters for this video 
        logging.info(f"\n\nStarting trials for video: {videoFile}")
        self.currentParameters = self.parameterSelector.getParameters() #will return None if no more parameters are there to try
        while self.currentParameters: #while it is not None (all options are not exhausted yet)
            logging.info(f"Current parameters: {self.currentParameters}")
            self._beginEncoding(videoFile)
            self.parameterSelector.setNewParameters(self.earlierEncodingTrialResultWasGood)
            self.currentParameters = self.parameterSelector.getParameters()
    
    def _beginEncoding(self, originalFile):
        self.originalFileSize = self.fileOps.getFileSize(originalFile)
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
        #---Run encoding command https://stackoverflow.com/questions/4256107/running-bash-commands-in-python
        logging.info("\n---------------------\n--- NEW RUN\n---------------------")
        logging.info(f"Running: {command}")
        try:
            #process = subprocess.run(command, stdout = subprocess.PIPE) #https://docs.python.org/3/library/subprocess.html#module-subprocess
            ffmpegProcess = subprocess.Popen(command) #https://stackoverflow.com/questions/636561/how-can-i-run-an-external-command-asynchronously-from-python
            self._resetCapturedData(originalFile, outputFilename, command, time.time()) #TODO: psutil can give a more accurate process start time
            logging.info(f"Process id: {ffmpegProcess.pid}")                       
            #---Keep polling to check if the ffmpegProcess completed and perform profiling too
            ffmpegProcessRepresentation = psutil.Process(pid = ffmpegProcess.pid) #https://psutil.readthedocs.io/en/latest/index.html?highlight=oneshot#processes
            processStartTime = ffmpegProcessRepresentation.create_time()
            processEndTime = processStartTime
            logging.info(f"Process start time: {processStartTime}")
            #---keep polling and profiling
            while True: 
                returnCode = ffmpegProcess.poll() #checking if process ended (could also use psutil to check)
                if returnCode == None: #process still running
                    try:
                        self._performProfiling(ffmpegProcessRepresentation)
                    except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
                        logging.error(f"Unable to profile this process: {e}")
                else: #process completed
                    processEndTime = time.time()
                    logging.info(f"Finished encoding {videoName}")
                    self._recordFinalProfilingMetadata(processEndTime)
                    self.report.addDictDataToReport(self.capturedData)
                    break
        except subprocess.CalledProcessError as e:
            logging.error(f"The encoding for {videoName} ran into some errors: {e}") #TODO: handle this more elegantly
        

    def _performProfiling(self, processRepresentation): #https://stackoverflow.com/questions/70724655/how-to-get-ram-and-cpu-time-consumption-python-app-on-linux
        with processRepresentation.oneshot():
            if processRepresentation.is_running():
                self._recordProfiledData(processRepresentation.cpu_times(), processRepresentation.memory_info().vms)
                #logging.info(f"Name: {processRepresentation.name()}, CPU Time: {processRepresentation.cpu_times()}, Memory: {processRepresentation.memory_info().vms}, CPU Percent: {processRepresentation.cpu_percent()}, num cores: {self.numberOfCPUs}") 
                #logging.info(f"Creation time: {processRepresentation.create_time()}")  # return cached value
                #logging.info(f"status: {processRepresentation.status()}")  # return cached value
        time.sleep(const.ProfiledData.PROFILING_SLEEP_INTERVAL_SECONDS)

    def _resetCapturedData(self, originalName, videoName, encodingCommand, encodingStartTime):
        self.capturedData = dict()        
        self.capturedData[const.ProfiledData.ORIGINAL_VIDEO_NAME_WITH_PATH] = originalName
        self.capturedData[const.ProfiledData.VIDEO_NAME_WITH_PATH] = videoName
        self.capturedData[const.ProfiledData.ENCODING_COMMAND] = encodingCommand
        self.capturedData[const.ProfiledData.ENCODING_START_TIME] = encodingStartTime
        self.capturedData[const.ProfiledData.CPU_TIME] = deque()
        self.capturedData[const.ProfiledData.MEMORY_CONSUMED] = deque()
        
    def _recordProfiledData(self, cpuTimes, memory):
        self.capturedData[const.ProfiledData.CPU_TIME].append(cpuTimes.user) #TODO: check if other cpuTimes need to be captured
        self.capturedData[const.ProfiledData.MEMORY_CONSUMED].append(memory)
        
    #TODO: take care of condition when there is some encoding error
    def _recordFinalProfilingMetadata(self, encodingEndTime):
        self.capturedData[const.ProfiledData.ENCODING_END_TIME] = encodingEndTime
        self.capturedData[const.ProfiledData.ENCODING_TIME] = encodingEndTime - self.capturedData[const.ProfiledData.ENCODING_START_TIME]        
        self.capturedData[const.ProfiledData.VIDEO_DURATION] = self.getVideoDuration(self.capturedData[const.ProfiledData.VIDEO_NAME_WITH_PATH])
        self.capturedData[const.ProfiledData.GENERATED_FILE_SIZE] = self.fileOps.getFileSize(self.capturedData[const.ProfiledData.VIDEO_NAME_WITH_PATH])
        self.capturedData[const.ProfiledData.CPU_TIME] = sum(self.capturedData[const.ProfiledData.CPU_TIME])
        self.capturedData[const.ProfiledData.MEMORY_CONSUMED] = numpy.mean(self.capturedData[const.ProfiledData.MEMORY_CONSUMED])
        #---Determine if video quality is acceptable
        self.earlierEncodingTrialResultWasGood = self._isEncodedVideoGoodEnough()
        self.capturedData[const.ProfiledData.VIDEO_QUALITY] = self.earlierEncodingTrialResultWasGood
        
    #TODO: Replace this function with an automated video quality and filesize Pareto assessment
    def _isEncodedVideoGoodEnough(self):
        print(f"\n\n\nOriginal video: {self.capturedData[const.ProfiledData.ORIGINAL_VIDEO_NAME_WITH_PATH]}")
        print(f"File size: {self.originalFileSize}")
        print(f"Encoded video: {self.capturedData[const.ProfiledData.VIDEO_NAME_WITH_PATH]}")
        print(f"File size: {self.capturedData[const.ProfiledData.GENERATED_FILE_SIZE]}")
        print("Please view the encoded video. Are you happy with the quality and file size?")
        print("Selecting 'y' will try another encoding with worse parameters. Selecting 'n' will try encoding with better parameters.")
        self._notifyUserUsingSound()
        videoIsGood = None
        while videoIsGood == None:
            videoIsGood = input("Are you happy with the video? [y/n] (simply press Enter for 'y') ")
            if videoIsGood.lower() == 'y' or videoIsGood == '': #User pressed 'y' or Enter
                videoIsGood = True
                break
            if videoIsGood.lower() == 'n':
                videoIsGood = False
            else:
                videoIsGood = None #to loop back and ask the User again for a proper response
        return videoIsGood
    
    def getVideoDuration(self, filenameWithPath): #TODO: Could also use `pip install ffprobe-python`
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filenameWithPath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return float(result.stdout)
    
    def _notifyUserUsingSound(self):
        pass #TODO: play sound
    
    
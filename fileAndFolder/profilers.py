import os
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
            raise IndexError(parameterName + " has no corresponding values supplied")
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
        self.selectedParameters = ""
    
    def getParameters(self):#should return an empty dict if no more parameters are there to process
        previousResultWasGood = None
        for parameter in self.parameters:#TODO: needs to be more elaborate
            parameterValue, areOptionsExhausted = parameter.getNewParameterValue(previousResultWasGood)
            self.selectedParameters += parameter.getParameterName() + str(parameterValue)
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
        self.bestParametersSoFar = None #parameters approved by the User or video quality evaluation function
        
    def startTrials(self, videoFile):
        logging.info(f"\n\nStarting trials for video: {videoFile}")
        parameters = self.parameterSelector.getParameters() #will return an empty string if no more parameters are generated
        while parameters:
            self._beginEncoding(parameters, videoFile)
            parameters = self.parameterSelector.getParameters()
    
    def _beginEncoding(self, parameters, originalFile):
        self.fileOps.createDirectoryIfNotExisting(const.GlobalConstants.encodedVideoFilesFolder)
        outputFilename = os.path.join(const.GlobalConstants.encodedVideoFilesFolder, f"{}")
        command = f"ffmpeg -i {originalFile} -c:a copy -c:v libx264 -crf '$crf' -preset '$preset' '$outfile'"
        
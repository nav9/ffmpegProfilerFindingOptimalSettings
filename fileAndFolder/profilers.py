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
    
    def getNewParameterValue(self, previousResultWasGood):
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
        return parameterValue, exhaustedOptions          

    def _moveIndexToMiddleOfList(self):
        self.index = const.GlobalConstants.FIRST_POSITION_IN_LIST #if length of list is 1, index position will be 0
        if len(self.temp) > 1:
            self.index = int(len(self.temp) / 2)
    
    def reset(self):
        self.temp = self.values[:]
        self.index = None
    
#-------------------------------------------------------
#--- Selectors. Helps with selecting encoding parameters
#-------------------------------------------------------
class BinarySearchSelector:
    def __init__(self):        
        self.parameters = [] 
        self.parameters.append(Parameter(const.EncodingParameters.PRESET, const.EncodingParameters.preset_values))
        self.parameters.append(Parameter(const.EncodingParameters.CRF, const.EncodingParameters.CRF_values))
        self.selectedParameters = []
    
    def getParameters(self):
        
        return self.selectedParameters
    

class EvolutionarySearchSelector:
    def __init__(self):
        self.parameters = dict()
        

#-------------------------------------------------------
#--- Profiling engine. Starts and monitors encoding
#-------------------------------------------------------    
class Profiler:
    def __init__(self, fileOps, report):        
        self.fileOps = fileOps
        self.report = report
        self.parameterSelector = BinarySearchSelector()
        
    def startTrials(self, videoFile):
        parameters = self.parameterSelector.getParameters() #will return None if no more parameters are generated
        while parameters:
            pass
            parameters = self.parameterSelector.getParameters()
    
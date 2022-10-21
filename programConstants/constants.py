import os

class GlobalConstants:
    originalVideoFilesFolder = os.path.join("originals", "") #The quotes at the end add an OS-specific folder slash
    FIRST_POSITION_IN_LIST = 0
    supportedFormats = ['.mkv']
    reportFolder = "reports"

class EncodingParameters:
    #MINIMUM_CRF = 0 # 0 is lossless (for 8 bit only, for 10 bit use -qp 0). 23 is the default
    #MAXIMUM_CRF = 51
    #CRF = range(MINIMUM_CRF, MAXIMUM_CRF+1)
    CRF = "crf"
    PRESET = "preset"
    #Note: These values need to be in the order of best to worst
    CRF_values = range(17, 29) #a subjectively sane range
    preset_values = ["veryslow", "slower", "slow", "medium", "fast", "faster", "veryfast", "superfast", "ultrafast"]
    
import os

class GlobalConstants:
    originalVideoFilesFolder = os.path.join("originals", "") #The quotes at the end add an OS-specific folder slash
    encodedVideoFilesFolder = os.path.join("encoded", "") #The quotes at the end add an OS-specific folder slash
    FIRST_POSITION_IN_LIST = 0
    supportedFormats = ['.mkv']
    reportFolder = "reports"
    

class EncodingParameters:
    #MINIMUM_CRF = 0 # 0 is lossless (for 8 bit only, for 10 bit use -qp 0). 23 is the default
    #MAXIMUM_CRF = 51
    #CRF = range(MINIMUM_CRF, MAXIMUM_CRF+1)
    CRF = "-crf"
    PRESET = "-preset"
    #Note: These values need to be in the order of best to worst
    CRF_values = range(17, 29) #a subjectively sane range
    preset_values = ["veryslow", "slower", "slow", "medium", "fast", "faster", "veryfast", "superfast", "ultrafast"]
    
class ProfiledData: #TODO: Find the units of these
    PROFILING_SLEEP_INTERVAL_SECONDS = 1
    ORIGINAL_VIDEO_NAME_WITH_PATH = "original name"
    VIDEO_NAME_WITH_PATH = "encoded name"
    ENCODING_COMMAND = "command"
    CPU_TIME = "cpu"
    MEMORY_CONSUMED = "memory"
    ENCODING_TIME = "encode duration"
    GENERATED_FILE_SIZE = "filesize"
    ORIGINAL_FILE_SIZE = "original filesize"
    VIDEO_DURATION = "video duration"
    VIDEO_QUALITY = "video quality"
    ENCODING_START_TIME = "start time"
    ENCODING_END_TIME = "end time"
    
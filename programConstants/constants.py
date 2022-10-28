import os

class GlobalConstants:
    originalVideoFilesFolder = os.path.join("originals", "") #The quotes at the end add an OS-specific folder slash
    encodedVideoFilesFolder = os.path.join("encoded", "") #The quotes at the end add an OS-specific folder slash
    summaryFilename = "summary.txt"
    FIRST_POSITION_IN_LIST = 0
    SECOND_POSITION_IN_LIST = 1
    supportedFormats = ['.mkv', '.mp4']
    reportFolder = "reports"    

class EncodingParameters:
    CRF = "-crf"
    PRESET = "-preset"
    #Note: These values need to be in the order of best to worst (what generates a good quality video with small file size and less CPU processing is 'best')
    #CRF_values = range(10, 51) #Actual range should be 0 to 51, where 0 is lossless (for 8 bit only, for 10 bit use -qp 0). 23 is the default
    #CRF_values = range(25, 35) #Ocean
    CRF_values = range(32, 51) #Text
    #preset_values = ["veryslow", "slower", "slow", "medium", "fast", "faster", "veryfast", "superfast", "ultrafast"]
    preset_values = ["fast", "faster", "veryfast"]
    
class ProfiledData: #TODO: Find the units of these
    PROFILING_SLEEP_INTERVAL_SECONDS = 1
    ORIGINAL_VIDEO_NAME_WITH_PATH = "original name"
    VIDEO_NAME_WITH_PATH = "encoded name"
    ENCODING_COMMAND = "command"
    CPU_TIME = "cpu" #user: time (in seconds) spent by normal processes executing in user mode; on Linux this also includes guest time
    MEMORY_CONSUMED = "memory" #vms+rss in bytes. rss: aka “Resident Set Size”, this is the non-swapped physical memory a process has used. On UNIX it matches “top“‘s RES column). vms: aka “Virtual Memory Size”, this is the total amount of virtual memory used by the process. On UNIX it matches “top“‘s VIRT column. 
    ENCODING_TIME = "encode duration"
    GENERATED_FILE_SIZE = "filesize" #bytes
    ORIGINAL_FILE_SIZE = "original filesize"
    VIDEO_DURATION = "video duration"
    VIDEO_QUALITY = "video quality"
    ENCODING_START_TIME = "start time"
    ENCODING_END_TIME = "end time"
    

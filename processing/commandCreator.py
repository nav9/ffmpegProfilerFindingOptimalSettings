import shlex #useful for recognizing quotes inside a command to be split

class EncoderCommand:
    def __init__(self):#Note: many of the members are not declared in __init__ so that if the generation command tries using a member that does not exist, an error would immediately be thrown
        self.ffmpeg = "ffmpeg"
        self.command = ""
    
    def setToOverwriteExistingFile(self):
        self.overwrite = "-y"
        
    def setInputFile(self, filename):
        self.inputFile = f"-i {filename}"

    def setOutputFile(self, filename):
        self.outputFile = f"{filename}"
        
    def copyAudioUnchanged(self):
        self.audio = "-c:a copy"
        
    def setVideoCodec(self):
        self.codec = "-c:v libx264"
        
    def suppressReportPrinting(self):#lines starting with "frame=" that are output every few frames
        self.noStats = "-nostats"
        
    def suppressBanner(self):#copyright notice, libraries, etc
        self.noBanner = "-hide_banner"
    
    def setParameters(self, parameters):
        self.parameters = parameters
    
    #TODO: This function needs to be made generic. The way the command is being created here is pointless
    def generateSimpleEncoderCommand(self, parameterString, inputFile, outputFilename):
        self.suppressReportPrinting()
        self.suppressBanner()
        self.setParameters(parameterString)
        self.setInputFile(inputFile)
        self.setOutputFile(outputFilename)
        self.setToOverwriteExistingFile()
        self.copyAudioUnchanged()
        self.setVideoCodec()
        self.command = shlex.split(f"{self.ffmpeg} {self.noStats} {self.noBanner} {self.overwrite} {self.inputFile} {self.audio} {self.codec} {self.parameters} {self.outputFile}")
        return self.command
    
class CommandCreator:
    def __init__(self):
        pass
    
    def generateEncoderCommand(self, parameterString, originalFile, outputFilename):
        encoder = EncoderCommand()
        return encoder.generateSimpleEncoderCommand(parameterString, originalFile, outputFilename)
    
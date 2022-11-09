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
    
    def setParameters(self, parameters):
        self.parameters = parameters
    
    def generateSimpleEncoderCommand(self, parameterString, inputFile, outputFilename):
        self.setParameters(parameterString)
        self.setInputFile(inputFile)
        self.setOutputFile(outputFilename)
        self.setToOverwriteExistingFile()
        self.copyAudioUnchanged()
        self.setVideoCodec()
        self.command = shlex.split(f"{self.ffmpeg} {self.overwrite} {self.inputFile} {self.audio} {self.codec} {self.parameters} {self.outputFile}")
        return self.command
    
class CommandCreator:
    def __init__(self):
        pass
    
    def generateEncoderCommand(self, parameterString, originalFile, outputFilename):
        encoder = EncoderCommand()
        return encoder.generateSimpleEncoderCommand(parameterString, originalFile, outputFilename)
    
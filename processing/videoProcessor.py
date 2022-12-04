import random
import cv2

class ExtractImageFromVideo:
    def __init__(self, videoPathWithVideoName):
        #print(f"OpenCV version: {cv2.__version__}")
        self.videoName = videoPathWithVideoName
        self.videoSource = cv2.VideoCapture(self.videoName)
        self.totalFramesInVideo = self.videoSource.get(cv2.CAP_PROP_FRAME_COUNT) 
        self.START_FRAME = 0     
        
    def getImageAtThisFrameNumber(self, frameNumber):        
        self.videoSource.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
        successfullyGotFrame, frameImageAtThisPosition = self.videoSource.read()
        return frameImageAtThisPosition, successfullyGotFrame      
        
    def getRandomImage(self):
        randomFrameNumber = random.randint(self.START_FRAME, self.totalFramesInVideo)
        return self.getImageAtThisFrameNumber(randomFrameNumber)
        
    def writeVideoFrameImageToFile(self, image, fileNameWithPath):#fileName will be a jpeg
        successfulWrite = cv2.imwrite(fileNameWithPath, image)
        return successfulWrite
        
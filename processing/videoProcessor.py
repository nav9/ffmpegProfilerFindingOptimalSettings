import os
import cv2
import random
from programConstants import constants
from sewar.full_ref import mse, rmse, psnr, uqi, ssim, ergas, scc, rase, sam, msssim, vifp

class ExtractImageFromVideo:
    def __init__(self, videoPathWithVideoName):
        #print(f"OpenCV version: {cv2.__version__}")
        self.videoName = videoPathWithVideoName
        self.videoSource = cv2.VideoCapture(self.videoName)
        self.totalFramesInVideo = self.videoSource.get(cv2.CAP_PROP_FRAME_COUNT)           
        
    def getTotalFramesInVideo(self):
        return self.totalFramesInVideo   
        
    def getImageFromVideoAtThisFrameNumber(self, frameNumber):   
        if frameNumber > self.totalFramesInVideo:
            raise ValueError(f"The total number of frames in this video is {self.totalFramesInVideo}. The frame number you want to view is {frameNumber}. Out of bounds.")
        self.videoSource.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
        successfullyGotFrame, frameImageAtThisPosition = self.videoSource.read()
        return frameImageAtThisPosition, successfullyGotFrame      
        
    def getImageFromVideoAtRandomFrame(self):#returns frameImageAtThisPosition, successfullyGotFrame
        randomFrameNumber = random.randint(constants.GlobalConstants.START_FRAME, self.totalFramesInVideo)
        return self.getImageFromVideoAtThisFrameNumber(randomFrameNumber)
        
class VideoQualityEvaluator:#https://superuser.com/a/338734
    def __init__(self, videosToCompare, fileOps) -> None:#all video names need to be with path. They will be used as keys in a dict
        self.fileOps = fileOps
        if not isinstance(videosToCompare, list):#convert it into a list if it is not already one
            videosToCompare = [videosToCompare]
        self.videosToCompare = videosToCompare #This will be a list of videos
        self.extractors = dict()
        for convertedVideo in self.videosToCompare:
            self.extractors[convertedVideo] = ExtractImageFromVideo(convertedVideo)
            
    def getTotalFramesInVideo(self, videoNameWithPath):
        return self.extractors[videoNameWithPath].getTotalFramesInVideo()
    
    def getScoreForVideoComparisonAtThisFrame(self, video1, video2, frameNumber):#The higher the score, the better
        frameForVideo1 = self.extractors[video1].getImageFromVideoAtThisFrameNumber(frameNumber)
        frameForVideo2 = self.extractors[video2].getImageFromVideoAtThisFrameNumber(frameNumber)        
        tempFolder = self.fileOps.folderSlash("temp")
        self.fileOps.deleteFolderIfItExists(tempFolder)
        self.fileOps.createDirectoryIfNotExisting(tempFolder)
        path1 = os.path.join(tempFolder, "vid1"+constants.Tests.JPG_Extension)
        path2 = os.path.join(tempFolder, "vid2"+constants.Tests.JPG_Extension)
        wrote1 = cv2.imwrite(path1, frameForVideo1)
        wrote2 = cv2.imwrite(path2, frameForVideo2)
        if wrote1 and wrote2:
            frameForVideo2 = cv2.imread(path1)
            frameForVideo1 = cv2.imread(path2)
        return msssim(frameForVideo2, frameForVideo1) #video1 is generally the original video
        
    def getScoresForVideosAtRandomFrames(self, video1, video2, numberOfComparisons):#The higher the score, the better
        scores = []
        totalFrames = min(self.getTotalFramesInVideo(video1), self.getTotalFramesInVideo(video2))
        for _ in range(numberOfComparisons):
            randomFrameNumber = random.randint(constants.GlobalConstants.START_FRAME, totalFrames)
            scores.append(self.getScoreForVideoComparisonAtThisFrame(video1, video2, randomFrameNumber))
        return scores
    
    def writeVideoFrameImageToFile(self, image, fileNameToGiveImage):#fileName will be a jpeg
        successfulWrite = cv2.imwrite(fileNameToGiveImage, image)
        return successfulWrite
    
import os
import numpy
import string
import random
import subprocess
from PIL import Image
from random import randrange
from programConstants import constants 
import matplotlib.pyplot as plotter
from fileAndFolder import fileFolderOperations as fileOps

class ImageAndVideoGenerator: #https://stackoverflow.com/questions/15261851/100x100-image-with-random-pixel-colour
    def __init__(self):
        self.IMAGE_Z_AXIS = 3
        self.SHADE_RANGE_START = 0
        self.MAX_SHADE_RANGE = 255
        self.MAX_SHADE_RANGE_SANS_ZERO = 256        
    
    def generateRandomRGB_PNG_Image(self, imageWidth, imageHeight, filenameWithoutExtensionAndWithPath):
        imageArray = numpy.random.rand(imageHeight, imageWidth, self.IMAGE_Z_AXIS) * self.MAX_SHADE_RANGE
        generatedImage = Image.fromarray(imageArray.astype('uint8')).convert('RGBA')
        if not filenameWithoutExtensionAndWithPath.lower().endswith(constants.Tests.PNG_Extension):
            filenameWithoutExtensionAndWithPath = filenameWithoutExtensionAndWithPath + constants.Tests.PNG_Extension
        generatedImage.save(filenameWithoutExtensionAndWithPath)
        return filenameWithoutExtensionAndWithPath
    
    def generateRandomBarGraph(self, filenameWithPath):
        randMin = 10; randMax = 40
        numberOfAxisElements = randrange(randMin, randMax)
        xAxis = [randrange(randMin, randMax) for _ in range(0, numberOfAxisElements)]
        yAxis = [random.choice(string.ascii_letters) for _ in range(0, numberOfAxisElements)]
        plotter.bar(numpy.array(yAxis), numpy.array(xAxis))
        plotter.savefig(filenameWithPath)
        #plotter.show() #show should be after savefig. Else the image saved will be blank

    def generateRandomBarGraphWithTheseValues(self, xAxisValues, yAxisValues, filenameWithPath):
        plotter.bar(numpy.array(yAxisValues), numpy.array(xAxisValues), color = "blue")
        plotter.savefig(filenameWithPath)   
        
    def generateVideoFromImages(self, folderWithImages, imagePrefix, imageExtension, videoNameWithPath):
        framerate = 25; videoCodec = "mpeg4"
        command = f"ffmpeg -r {framerate} -i {folderWithImages}{imagePrefix}%d{imageExtension} -vcodec {videoCodec} -y {videoNameWithPath}"
        #subprocess.Popen(command) #Absolute path may need to be given to use this command
        os.system(command)
        
class TestVideoExtraction:
    def recreateDummyFolder(self, folderName):
        fileFolderOps = fileOps.FileOperations()
        folderLocation = os.path.join(constants.Tests.testFolder, constants.GlobalConstants.dummyPrefix + folderName, "") #the quotes at the end add a folder slash if it does not exist
        fileFolderOps.deleteFolderIfItExists(folderLocation)
        fileFolderOps.createDirectoryIfNotExisting(folderLocation)  
        return folderLocation  
    
    def generateRandomVideo(self, imageFilename, folderPathAndName, imageWidth, imageHeight, numberOfVideoFrames, videoFolder, videoName):
        fileFolderOps = fileOps.FileOperations()
        folderLocation = self.recreateDummyFolder(folderPathAndName)
        gen = ImageAndVideoGenerator()
        imagesGenerated = []
        for i in range(0, numberOfVideoFrames):
            imageName = os.path.join(folderLocation, imageFilename + str(i))      
            imagesGenerated.append(gen.generateRandomRGB_PNG_Image(imageWidth, imageHeight, imageName))
        videoLocation = os.path.join(folderLocation, videoFolder, "")
        fileFolderOps.createDirectoryIfNotExisting(videoLocation)
        videoNameWithPath = os.path.join(videoLocation, videoName)
        gen.generateVideoFromImages(folderLocation, imageFilename, constants.Tests.PNG_Extension, videoNameWithPath)
      
    def varyValuesInThisListLittle(self, theList):
        maxVariation = 2
        for i in range(len(theList)):
            variation = i + random.randrange(-maxVariation, maxVariation)
            if theList[i] + variation > 0:
                theList[i] = theList[i] + variation
        return theList
    
    def generateVaryingBarGraphVideo(self, imageFilename, folderPathAndName, numberOfVideoFrames, videoFolder, videoName):
        randMin = 10; randMax = 40
        numberOfAxisElements = randrange(randMin, randMax)        
        fileFolderOps = fileOps.FileOperations()
        folderLocation = self.recreateDummyFolder(folderPathAndName)
        gen = ImageAndVideoGenerator()
        yAxis = [randrange(randMin, randMax) for _ in range(0, numberOfAxisElements)]
        xAxis = [random.choice(string.ascii_letters) for _ in range(0, numberOfAxisElements)]        
        imagesGenerated = []
        for i in range(0, numberOfVideoFrames):
            imageName = os.path.join(folderLocation, imageFilename + str(i) + constants.Tests.PNG_Extension)      
            imagesGenerated.append(imageName)
            yAxis = self.varyValuesInThisListLittle(yAxis)
            gen.generateRandomBarGraphWithTheseValues(yAxis, xAxis, imageName)
            print(yAxis)
        videoLocation = os.path.join(folderLocation, videoFolder, "")
        fileFolderOps.createDirectoryIfNotExisting(videoLocation)
        videoNameWithPath = os.path.join(videoLocation, videoName)
        gen.generateVideoFromImages(folderLocation, imageFilename, constants.Tests.PNG_Extension, videoNameWithPath)
    
    # #DO NOT DELETE: This is a working function for generating random video. Not yet developed into a test case though
    # def test_gettingImageAtFrame1(self):
    #     imageFilename = "rand"; folderPathAndName = "imagesForRandVideo"
    #     imageWidth = 640; imageHeight = 480; numberOfVideoFrames = 10
    #     videoFoldername = "randVideo"; videoName = "video.mp4"
    #     self.generateRandomVideo(imageFilename, folderPathAndName, imageWidth, imageHeight, numberOfVideoFrames, videoFoldername, videoName)
        
    def test_gettingImageAtFrame(self):
        imageFilename = "bar"; folderPathAndName = "imagesForBarVideo"
        numberOfFrames = 10
        videoFoldername = "barVideo"; videoName = "video.mp4"
        self.generateVaryingBarGraphVideo(imageFilename, folderPathAndName, numberOfFrames, videoFoldername, videoName)   
        assert False     
# ffmpegProfilerFindingOptimalSettings
A profiler for FFMPEG that helps you find the optimal settings to encode a good quality video while consuming minimum resources.
  
# Requirements  
Python 3.6+ (for this project, Python 3.9.13 was used).  
* To install required packages, use: `pip install -r requirements.txt`. (There are also automated tools like pipreqs, pipreqsnb or pigar, which can install the required packages).  
* Install `sudo apt install ffmpeg ffprobe`.  
  
`ffmpeg-quality-metrics` is planned to be used for [image quality metrics](https://github.com/slhck/ffmpeg-quality-metrics). The `sewar` package could also be attempted for image quality metrics. The `opencv-contrib-python` package is used by the test cases for extracting frames from videos.  
  
# Run  
First, ensure you place the video in a folder named `originals`, and this folder should be located in the same folder that `main.py` is located in. Then run the program using:  
`python main.py`
  
# Supported video formats:  
`.mkv`, `.mp4`, `.m4v`. You could add more in the `supportedFormats` list in the `GlobalConstants` class in `./programConstants/constants.py` file.  
    
# Running the test cases  
First install PyTest: `pip install pytest==7.1.2`.  
At the program's root directory, run `pytest`.  
You can also run tests in the following ways:  
* Tests in a module: `pytest tests/test_mod.py`
* Tests in a directory: `pytest tests/testing/`
* Tests by keyword expressions: `pytest -k "MyClass and not method"`
* [and more](https://stackoverflow.com/a/54493489/453673).

# ffmpegProfilerFindingOptimalSettings
A profiler for FFMPEG that helps you find the optimal settings to encode a good quality video while consuming minimum resources.
  
# Requirement  
Python 3.6+ (for this project, Python 3.9.13 was used).  
To install required packages, use: `pip install -r requirements.txt`. (There are also automated tools like pipreqs, pipreqsnb or pigar, which can install the required packages).  
  
* `pip install ffmpeg-quality-metrics==3.0.0` for [image quality metrics](https://github.com/slhck/ffmpeg-quality-metrics). Also make sure `ffmpeg` and `ffprobe` are installed.   
* For future trials: `pip install sewar` could also be attempted for image quality metrics.  
* `pip3 install opencv-contrib-python==4.5.5.62` for extracting frames from videos.  
  
# Running the test cases  
First install PyTest: `pip install pytest==7.1.2`.  
At the program's root directory, run `pytest`.  
You can also run tests in the following ways:  
* Tests in a module: `pytest tests/test_mod.py`
* Tests in a directory: `pytest tests/testing/`
* Tests by keyword expressions: `pytest -k "MyClass and not method"`
* [and more](https://stackoverflow.com/a/54493489/453673).

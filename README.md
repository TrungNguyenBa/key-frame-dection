# key-frame-dection

The program is built to detect and retreive key-frame and short videos based on the keyframe from long-duration videos.
This is project of UMASS-COMPSCI 696E

# Instructions to use the program
## Dependency
* python3
* cv2
* moviepy

## Run program
python3 key-frame.py <video-path> <threshold> <time-frame>

# Progress Update
## Week 2 (1):
* Finalized the project
* Started researching for methods and implementations

## Week 3 (2):
* Built first iteration keyframe detections using differences in frame hitogram
* Was able to detect keyframe but was not able to generalize for all tests videos
* Presentation slides: https://docs.google.com/presentation/d/1L4FIFTQAXGdLLrmkEwJCsD3zq-XkpLt6qxYk2w1q0_o/edit?usp=sharing

## Week 4 (3):
* Improved the program -- was able to better generalize the program for multiple videos
* Built features to create the short videos instead of just retrieving keyframe
* Finished planning for the rest of the semesters
* Presnetation slides: https://docs.google.com/presentation/d/1Z7T9R8i61UViuW7c7OAW9S4aWDFnaqOvEHeDHPeLN2s/edit?usp=sharing

## Week 5 (4):
* Improve the short videos features by using new lib to reduce the time
* Update the documentation
* Tested the program on some new datasets

## Week 6 (5):
* Improve the current process of collecting dataframe, allow user to define the number of top short videos/keyframes.
* Update documentation
* Add SURF features into the program to detect keyframe with subject image
* Presnetation slides: https://docs.google.com/presentation/d/1OzZ4x7MI0MlgbxFo0Z6scTR2Pg6ourUJZbsoYcGzR2E/edit#slide=id.p




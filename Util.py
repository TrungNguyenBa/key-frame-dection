import cv2 as cv
import numpy as np
import argparse
from math import sqrt
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def histogram_diff(f1,f2):
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges
    channels = [0, 1]
    f1 = cv2.calcHist([f1], channels, None, histSize, ranges, accumulate=False)
    cv2.normalize(f1, f1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    f2 = cv2.calcHist([f2], channels, None, histSize, ranges, accumulate=False)
    cv2.normalize(f2, f2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    diff = cv2.compareHist(f1, f2, 0)
    if diff < threshold:
        return True
    return False

def extract_keypoint(img):    
    orb = cv.ORB_create()
    kp = orb.detect(img,None)
    kpts1, desc1 = orb.compute(img, kp) 
    return kpts1,desc1

def image_comparision(img1,img2, ratio = 0.8):
    matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_BRUTEFORCE_HAMMING)
    kpts1,desc1 = extract_keypoint(img1)
    kpts2,desc2 = extract_keypoint(img2)
    try:
        nn_matches = matcher.knnMatch(desc1, desc2, 2)
        nn_match_ratio = ratio # Nearest neighbor matching ratio
        nn_matches = [i for i in nn_matches if len(i) > 1  ]
        matches = 0
        for m, n in nn_matches:
            if m.distance < nn_match_ratio * n.distance:
                matches +=1
        return matches
    except:
        return 0 

# create the short videos based on the interval times
# The short video is the video with start-time,end-time as (keyframe-interval,key+interval)
def get_short_video(video_path,keyframe_time,interval=3,name=None):
    start_time = keyframe_time-interval
    end_time = keyframe_time+interval
    ffmpeg_extract_subclip(video_path, start_time, end_time, targetname= name)
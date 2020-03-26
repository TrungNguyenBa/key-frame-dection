import cv2 as cv
import numpy as np
import argparse
from math import sqrt
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def extract_keypoint(img):
    kp = orb.detect(img,None)
    kpts1, desc1 = orb.compute(img, kp) 
    return kpts1,desc1

def image_comparision(img1,img2, ratio = 0.8):
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

# Find the key frames based on an anchor image
def find_key_frame(img_path,video_path,threshold):
    img_target = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
    cap = cv.VideoCapture(video_path)
    suc, frame = cap.read()
    m = {}
    while suc:
        suc, curr_frame = cap.read()
        if suc:
            s = int(cap.get(cv.CAP_PROP_POS_MSEC)/1000)
            k = list(m.keys())  
            for i in k:
                if i < s - timeframe:
                    m.pop(i)
            for i in m.get(s - timeframe,[]):
                img = cv.cvtColor(i, cv.COLOR_BGR2GRAY)
                diff = image_comparision(img_target,img)
                if diff >= threshold:
                    NotInclude = True
                    for i in range(0,timeframe):
                        if s - i in ret:
                            NotInclude = False
                    if NotInclude:
                        images[s] = curr_frame
                        ret[s] = diff
                    break
            m[s] = m.get(s,[])
            m[s].append(curr_frame)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Key-frame detection program for extracting and retrieving important frames afrom long-duration videos.')
    parser.add_argument('--target-image', help='Path to target image')
    parser.add_argument('--video_path', help='Path to the video.')
    parser.add_argument('--threshold', help ='threshold of numbers of matches for 2 images', default = 5)
    parser.add_argument('--time_interval', help='The time interval for generating the short videos from collected keyframe.', default=3)
    parser.add_argument('--number-of-frames', help='The numbers of keyframes to collect.',default=4)
    args = parser.parse_args()
    ret = {}
    images = {}
    image_path = args.target_image    
    video_path = args.video_path
    threshold = int(args.threshold)
    timeframe = int(args.time_interval)
    number_of_keyframe = int(args.number_of_frames)
    orb = cv.ORB_create()
    matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_BRUTEFORCE_HAMMING)
    find_key_frame(image_path,video_path,threshold)
    for i,_ in sorted(ret.items(), key = lambda x: x[1] )[:number_of_keyframe]:
        cv.imwrite('images'+str(i)+'.png',images[i])
        get_short_video(video_path,i)
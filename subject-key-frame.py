from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
from math import sqrt
parser = argparse.ArgumentParser(description='Code for AKAZE local features matching tutorial.')
parser.add_argument('--input1', help='Path to input image 1.', default='graf1.png')
parser.add_argument('--input2', help='Path to input image 2.', default='graf3.png')
parser.add_argument('--homography', help='Path to the homography matrix.', default='H1to3p.xml')
args = parser.parse_args()
img1 = cv.imread(cv.samples.findFile(args.input1), cv.IMREAD_GRAYSCALE)
img2 = cv.imread(cv.samples.findFile(args.input2), cv.IMREAD_GRAYSCALE)
if img1 is None or img2 is None:
    print('Could not open or find the images!')
    exit(0)
fs = cv.FileStorage(cv.samples.findFile(args.homography), cv.FILE_STORAGE_READ)
homography = fs.getFirstTopLevelNode().mat()
akaze = cv.AKAZE_create()
kpts1, desc1 = akaze.detectAndCompute(img1, None)
kpts2, desc2 = akaze.detectAndCompute(img2, None)
matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_BRUTEFORCE_HAMMING)
nn_matches = matcher.knnMatch(desc1, desc2, 2)
matched1 = []
matched2 = []
nn_match_ratio = 0.8 # Nearest neighbor matching ratio
for m, n in nn_matches:
    if m.distance < nn_match_ratio * n.distance:
        matched1.append(kpts1[m.queryIdx])
        matched2.append(kpts2[m.trainIdx])
inliers1 = []
inliers2 = []
good_matches = []
inlier_threshold = 2.5 # Distance threshold to identify inliers with homography check
for i, m in enumerate(matched1):
    col = np.ones((3,1), dtype=np.float64)
    col[0:2,0] = m.pt
    col = np.dot(homography, col)
    col /= col[2,0]
    dist = sqrt(pow(col[0,0] - matched2[i].pt[0], 2) +\
                pow(col[1,0] - matched2[i].pt[1], 2))
    if dist < inlier_threshold:
        good_matches.append(cv.DMatch(len(inliers1), len(inliers2), 0))
        inliers1.append(matched1[i])
        inliers2.append(matched2[i])
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Key-frame detection program for extracting and retrieving important frames afrom long-duration videos.')
    parser.add_argument('--video_path', help='Path to the video.')
    parser.add_argument('--threshold', help='The threshold for frames comparations. The value should be in range 0.99-0.9999', default=0.99)
    parser.add_argument('--time_interval', help='The time interval for generating the short videos from collected keyframe.', default=3)
    parser.add_argument('--number-of-frames', help='The numbers of keyframes to collect.',default=4)
    args = parser.parse_args()
    ret = {}
    images = {}
    video_path = args.video_path
    threshold = float(args.threshold)
    timeframe = int(args.time_interval)
    number_of_keyframe = int(args.number_of_frames)
    find_general_keyframe()
    for i,_ in sorted(ret.items(), key = lambda x: x[1] )[:number_of_keyframe]:
        cv2.imwrite('images'+str(i)+'.png',images[i])
        get_short_video(i)
import sys 
import cv2
import numpy as np
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


# compute true diff of two frames based on their histograms
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

# create the short videos based on the interval times
# The short video is the video with start-time,end-time as (keyframe-interval,key+interval)
def get_short_video(keyframe_time,interval=3):
	start_time = keyframe_time-interval
	end_time = keyframe_time+interval
	ffmpeg_extract_subclip(video_path, start_time, end_time, targetname="test_keyframe{}.mp4".format(keyframe_time))


# find the general keyframe (i.e, the keyframe in the videos without prior knowledge)
def find_general_keyframe():
	compare = histogram_diff
	cap = cv2.VideoCapture(video_path)

	suc, frame = cap.read()
	images = {}
	m = {}
	while suc:
		suc, curr_frame = cap.read()
		if suc:
			s = int(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)
			k = list(m.keys())	
			for i in k:
				if i < s - timeframe:
					m.pop(i)
			for i in m.get(s - timeframe,[]):
				diff = compare(curr_frame,i)
				if diff:
					NotInclude = True
					for i in range(0,timeframe):
						if s - i in ret:
							NotInclude = False
					if NotInclude:
						images[s] = curr_frame
						ret.add((s,d))
					break
			m[s] = m.get(s,[])
			m[s].append(curr_frame)

# find SURF keypoint for an images
def find_SURF_keypoint(image.threshold = 400):
	surf = cv2.SURF(threshold)
	kp, des = surf.detectAndCompute(img,None)
	return kp,des

# find the general keyframe based on picture/image of a suject
def find_keyframe_with_subject(ret):
	pass

if __name__ == '__main__':
	ret = set()
	video_path = sys.argv[1]
	threshold = float(sys.argv[2])
	timeframe = int(sys.argv[3])
	number_of_keyframe = 4 if not sys.argv[4] else sys.argv[4]

	find_general_keyframe(ret)
	for i,_ in sorted(ret, key = lambda x: x[1])[:number_of_keyframe]:
		cv2.imwrite('images'+str(i)+'.png',images[i])
		get_short_video(i)
# for i,v in enumerate(images):
 	


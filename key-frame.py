import argparse
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
						ret[s] = diff
					break
			m[s] = m.get(s,[])
			m[s].append(curr_frame)

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
 	


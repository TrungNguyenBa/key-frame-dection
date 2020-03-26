import argparse
import cv2
import numpy as np
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import Util
import subprocess

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

def check_target_image(video_path, target_image, threshold = 150):
	img_target = cv2.imread(target_image, cv2.IMREAD_GRAYSCALE)
	cap = cv2.VideoCapture(video_path)
	suc,frame = cap.read()
	while suc:
		suc, curr_frame = cap.read()
		if suc:
			img = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)	
			diff = Util.image_comparision(img_target,img)
			if diff >= threshold:
				print(video_path)
				print(diff)
				return True
	return False

def remove_videos(l):
	if not len(l):
		return
	string = " ".join(l)
	subprocess.call('rm {}'.format(string), shell = True)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Key-frame detection program for extracting and retrieving important frames afrom long-duration videos.')
	parser.add_argument('--video-path', help='Path to the video.')
	parser.add_argument('--threshold', help='The threshold for frames comparations. The value should be in range 0.99-0.9999', default=0.99)
	parser.add_argument('--time_interval', help='The time interval for generating the short videos from collected keyframe.', default=2)
	parser.add_argument('--number-of-frames', help='The numbers of keyframes to collect.',default=6)
	parser.add_argument('--target-image', help='path the target image to filter keyfame', default=None)
	args = parser.parse_args()
	ret = {}
	images = {}
	video_path = args.video_path
	threshold = float(args.threshold)
	timeframe = int(args.time_interval)
	number_of_keyframe = int(args.number_of_frames)
	target_image= args.target_image
	find_general_keyframe()
	names = []
	for i,_ in sorted(ret.items(), key = lambda x: x[1] )[:number_of_keyframe]:
		file_name = 'images'+str(i)+'.png'
		cv2.imwrite('images'+str(i)+'.png',images[i])
		video_name = "frame_test{}.mp4".format(str(i))
		Util.get_short_video(video_path,i, name=video_name)
		names.append((file_name,video_name))
		# if target_image and not check_target_image(name,target_image):
		# 	remove_lst.append(name)
	if target_image:
		remove_lst = []
		for fname,vname in names:
			if not check_target_image(vname,target_image):
				remove_lst.append(fname)
				remove_lst.append(vname)
		remove_videos(remove_lst)

 		


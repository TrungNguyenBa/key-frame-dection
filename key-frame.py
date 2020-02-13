import sys 
import cv2
import numpy as np

video_path = sys.argv[1]
method = sys.argv[2]
threshold = float(sys.argv[3])
timeframe = int(sys.argv[4])

# def absolute_diff(f1,f2):
# 	diff = cv2.absdiff(f1,f2)
# 	non_zero_count = np.count_nonzero(diff)
# 	if non_zero_count > threshold:
# 		return True
# 	return False

def histogram_diff(f1,f2):
	h_bins = 50
	s_bins = 60
	histSize = [h_bins, s_bins]
	h_ranges = [0, 180]
	s_ranges = [0, 256]
	ranges = h_ranges + s_ranges
	channels = [0, 1]
	f1 = cv2.calcHist([f1], channels, None, histSize, ranges, accumulate=False)
	f2 = cv2.calcHist([f2], channels, None, histSize, ranges, accumulate=False)
	diff = cv2.compareHist(f1, f2, 0)
	if diff < threshold:
		return True
	return False

compare = histogram_diff


cap = cv2.VideoCapture(video_path)

suc, prev_frame = cap.read()
ret = set()
images = []
while suc:
	suc, curr_frame = cap.read()
	
	if suc:
		diff = compare(curr_frame, prev_frame)
		if diff :
			s = int(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)
			if s not in ret:
				images.append(curr_frame)
				ret.add(s)
	prev_frame = curr_frame

for i,v in enumerate(images):
	cv2.imwrite('images'+str(i)+'.png',v)


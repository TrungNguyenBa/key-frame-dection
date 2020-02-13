import sys 
import cv2
import numpy as np

video_path = sys.argv[1]
threshold = float(sys.argv[2])
timeframe = int(sys.argv[3])

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
	cv2.normalize(f1, f1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
	f2 = cv2.calcHist([f2], channels, None, histSize, ranges, accumulate=False)
	cv2.normalize(f2, f2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
	diff = cv2.compareHist(f1, f2, 0)
	if diff < threshold:
		return True
	return False

compare = histogram_diff


cap = cv2.VideoCapture(video_path)

suc, frame = cap.read()
ret = set()
images = []
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
					images.append(curr_frame)
					ret.add(s)
				break
		m[s] = m.get(s,[])
		m[s].append(curr_frame)
print(len(images))
print(sorted(ret))
# for i,v in enumerate(images):
# 	cv2.imwrite('images'+str(i)+'.png',v)


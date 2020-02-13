import pytube
import sys
link = sys.argv[1]
print(link)
pytube.YouTube(link)

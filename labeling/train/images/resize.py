import cv2
import os

for _, _, fileNames in os.walk("./"):
    for file in fileNames:
    	if file.endswith("jpg"):
    		img = cv2.imread(file)
    		img = cv2.resize(img, (352, 480))
    		
    		cv2.imwrite(file, img)
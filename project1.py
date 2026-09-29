import numpy as np
import cv2
import sys

#must write tests_new/"any image number".png
if len(sys.argv)<2:
    print("Not enough arguments")
    sys.exit(1)


pickimg = sys.argv[1] 
img = cv2.imread(pickimg)
print(pickimg)
def hough_transform():
    coordinates = []
    with open(sys.argv[1].replace(".png",".txt"),"r") as file:
        for line in file:
            coordinates.append(line.strip())

    print(coordinates)
    int_coordinates = []
    for coord in coordinates:
        for num in coord.split():
            int_coordinates.append(int(num))
    print(int_coordinates)
Houghtransform = hough_transform()

cv2.imshow("Picture",img)
cv2.waitKey(0)
cv2.destroyAllWindows()



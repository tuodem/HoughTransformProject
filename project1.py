import numpy as np
import cv2
import sys

#must write tests_new/"any image number".png
if len(sys.argv)<2:
    print("Not enough arguments")
    sys.exit(1)

#grabs the image name from command line
pickimg = sys.argv[1]
#cv2 reads the image to be able to show 
img = cv2.imread(pickimg)
#turns image gray for hough
gray_scale = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def hough_transform(image):
    #list for coordinates
    coordinates = []
    #reads the file with command line and replaces with txt
    with open(sys.argv[1].replace(".png",".txt"),"r") as file:
        for line in file:
            coordinates.append(line.strip())

    #turns all numbers from the original coordinates list into integers
    int_coordinates = [tuple(map(int,coord.split(" "))) for coord in coordinates if len(coord.split(" ")) == 3]

    #gets image pixels and uses it for hough matrix
    height, width = image.shape
    #range for my radius
    r_min = 0
    r_max = 50
    #creates array thta turns degrees from 0 to 360 into radians and stores it
    thetas = np.deg2rad(np.arange(0,180))
    #cos stores the x coordinate and sin stores the y coordinate as separate arrays
    cos_t = np.cos(thetas)
    sin_t = np.sin(thetas)

    #hough matrix that is filled with zeros
    h_votes = np.zeros((height,width),dtype=np.float64)

   
    #loops through coordinates
    for x,y,v in int_coordinates:
        #loops with radius range from 0-50
        for r in range(r_min,r_max+1):
            #loops through thetas for my sin and cos from 0 to 180 
            for i in range(len(thetas)):
                #gets the a and b distance of each ball
                a = int(x-r*cos_t[i])
                b = int(y-r*sin_t[i])
                #compares the distance with width and height of image for boundary issues
                if 0 <= a < width and 0 <= b < height:
                    #votings for hough transformation stored into array with b the height of image representing the rows and a the width of the image respresenting the columns
                    h_votes[b,a]+=1


        

#returns voting for hough and coordinates
    return h_votes, int_coordinates
#takes the hough matrix and coordinates for drawing the circles
votes_matrix, coordinates = hough_transform(gray_scale)
#set a random radius that was between 20 and 45
radius = 25
#loop through coordinates to draw the circles
for x,y,v in coordinates:
    #checks if v is 1 to see if its the spot ball
    if v == 1:
        color = (0,0,255) #sets color to red
        thickness = 3 #makes the circle thicker
    else:
        color = (0,255,0) #sets color to green
        thickness = 2 #setes thickness of line
    #draws the circles for each ball
    cv2.circle(img,(x,y),radius,color,thickness)

#calls to show the image and keep it open until you exit
cv2.imshow("Picture",img)
cv2.waitKey(0)
cv2.destroyAllWindows()



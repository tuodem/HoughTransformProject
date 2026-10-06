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
    thetas = np.deg2rad(np.arange(0,360))
    #cos stores the x coordinate and sin stores the y coordinate as separate arrays
    cos_t = np.cos(thetas)
    sin_t = np.sin(thetas)

    #hough matrix that is filled with zeros
    h_votes = np.zeros((height,width),dtype=np.float64)
    spot_x = None
    spot_y = None
   
    #loops through coordinates
    for x,y,v in int_coordinates:
        if v == 1:
            spot_x = x
            spot_y = y
        
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
                        
                        
    #sets the max votes to compare to votes for the regions with the highest voting       
    max_votes = np.max(h_votes)
    #radius for how big i want the circles to be
    radius = 25
    #loop to go through the height and width of the image
    for b in range(height):
        for a in range(width):
            #takes each vote for each region
            votes = h_votes[b,a]
            #checks to see if the votes are the same as the max votes which are my highest for the shape
            if votes >= max_votes:
                #checking for my spot ball to color it green
                if spot_x == a and spot_y == b:
                    color = (0,0,255)#color is red for circle
                    thickness = 3 #how thick i want the circle to be
                else:
                    color = (0,255,0)#color is green for circle
                    thickness = 2 #how thick i want the circle to be
                    
                cv2.circle(img,(a,b),radius,color,thickness) #draws circle around the balls

        



#calls hough_transform function with a gray image
hough_transform(gray_scale)


#calls to show the image and keep it open until you exit
cv2.imshow("Picture",img)
cv2.waitKey(0)
cv2.destroyAllWindows()



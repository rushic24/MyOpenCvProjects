import argparse
import cv2
import pyautogui
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
refPt_cpy=[]
cropping = False
cnt=0

def draw_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping,cnt,clone,image,refPt_cpy

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN and (cnt%3!=0 or cnt==0):
        refPt.append((x, y))
        cnt=cnt+1
        cropping = True
    elif event == cv2.EVENT_MOUSEMOVE and len(refPt)==1:
        image = clone.copy()
        cv2.rectangle(image, refPt[0], (x,y), (0, 255, 0), 2)
        cv2.imshow("image", image)
    
    elif cnt==2:
        cropping = False
        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)
        cnt=0
        refPt_cpy=refPt
        refPt=[]
        #print len(refPt)
        return

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        image = clone.copy()

    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break
# if there are two reference points, then crop the region of interest
# from teh image and display it

if len(refPt_cpy) == 2:
    roi = clone[refPt_cpy[0][1]:refPt_cpy[1][1], refPt_cpy[0][0]:refPt_cpy[1][0]]
    cv2.imshow("ROI", roi)
    cv2.waitKey(0)

# close all open windows
cv2.destroyAllWindows()     
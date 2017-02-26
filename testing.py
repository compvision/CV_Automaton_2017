import cv2  # OpenCV Library
 
#-----------------------------------------------------------------------------
#       Load and configure Haar Cascade Classifiers
#-----------------------------------------------------------------------------
  
# build our cv2 Cascade Classifiers
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
noseCascade = cv2.CascadeClassifier("haarcascade_mcs_nose.xml")
 
#-----------------------------------------------------------------------------
#       Load and configure hat (.png with alpha transparency)
#-----------------------------------------------------------------------------
 
# Load our overlay image: hat.png
hat = cv2.imread('hat.png',-1)
 
# Create the mask for the hat
orig_mask = hat[:,:,3]
 
# Create the inverted mask for the hat
orig_mask_inv = cv2.bitwise_not(orig_mask)
 
# Convert hat image to BGR
# and save the original image size (used later when re-sizing the image)
hat = hat[:,:,0:3]
origHatHeight, origHatWidth = hat.shape[:2]
 
#-----------------------------------------------------------------------------
#       Main program loop
#-----------------------------------------------------------------------------
 
# collect video input from first webcam on system
video_capture = cv2.VideoCapture(0)
 
while(cv2.waitKey(30) != 30):
    # Capture video feed
    ret, frame = video_capture.read()
 
    # Create greyscale image from the video feed
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    # Detect faces in input video stream
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
 
   # Iterate over each face found
    for (x, y, w, h) in faces:
        # Un-comment the next line for debug (draw box around all faces)
        # face = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
 
        #roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[0:y+h, x:x+w]
 
        # Detect a nose within the region bounded by each face (the ROI)
        #nose = noseCascade.detectMultiScale(roi_gray)
 
        #for (nx,ny,nw,nh) in nose:
            # Un-comment the next line for debug (draw box around the nose)
            #cv2.rectangle(roi_color,(nx,ny),(nx+nw,ny+nh),(255,0,0),2)
 
            # The hat should be three times the width of the nose
        hatWidth = w
        hatHeight = hatWidth * origHatHeight / origHatWidth

        # Center the hat
        x1 = 0
        x2 = w
        y1 = y + h - (hatHeight*3/4)
        y2 = y + h + (hatHeight/4)

        # Check for clipping
        #if x1 < 0:
        #    x1 = 0
        #if y1 < 0:
        #    y1 = 0
        #if x2 > w:
        #    x2 = w
        #if y2 > h:
        #    y2 = h

        # Re-calculate the width and height of the hat image
        hatWidth = x2 - x1
        hatHeight = y2 - y1

        # Re-size the original image and the masks to the hat sizes
        # calcualted above
        hat = cv2.resize(hat, (hatWidth,hatHeight), interpolation = cv2.INTER_AREA)
        mask = cv2.resize(orig_mask, (hatWidth,hatHeight), interpolation = cv2.INTER_AREA)
        mask_inv = cv2.resize(orig_mask_inv, (hatWidth,hatHeight), interpolation = cv2.INTER_AREA)

        # take ROI for hat from background equal to size of hat image
        roi = roi_color[y1:y2, x1:x2]

        # roi_bg contains the original image only where the hat is not
        # in the region that is the size of the hat.
        roi_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

        # roi_fg contains the image of the hat only where the hat is
        roi_fg = cv2.bitwise_and(hat,hat,mask = mask)

        # join the roi_bg and roi_fg
        dst = cv2.add(roi_bg,roi_fg)

        # place the joined image, saved to dst back over the original image
        roi_color[y1:y2, x1:x2] = dst

        break
 
    # Display the resulting frame
    cv2.imshow('Video', frame)
 
    # press any key to exit
    # NOTE;  x86 systems may need to remove: &amp;amp;amp;amp;amp;amp;amp;quot;&amp;amp;amp;amp;amp;amp;amp;amp; 0xFF == ord('q')&amp;amp;amp;amp;amp;amp;amp;quot;
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
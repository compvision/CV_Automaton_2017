import cv2  # OpenCV Library

#-----------------------------------------------------------------------------
#       Load and configure Haar Cascade Classifiers
#-----------------------------------------------------------------------------

# build our cv2 Cascade Classifiers
faceCascade = cv2.CascadeClassifier("cascadeFiles/haarcascade_frontalface_default.xml")
noseCascade = cv2.CascadeClassifier("reference/haarcascade_mcs_nose.xml")
#eyeCascade = cv2.CascadeClassifier("cascadeFiles/haarcascade_eye.xml")
#leftEyeCascade = cv2.CascadeClassifier("cascadeFiles/haarcascade_lefteye_2splits.xml")

#-----------------------------------------------------------------------------
#       Load and configure hat (.png with alpha transparency)
#-----------------------------------------------------------------------------

# Load our overlay image: hat.png & monocle.png
imgHat = cv2.imread('hat.png',-1)
#imgMonacle = cv2.imread('monocle.png',-1)
imgMonacle = cv2.imread('reference/mustache.png',-1)

# Create the mask for the hat & monocle
orig_mask = imgHat[:,:,3]
orig_mask_m = imgMonacle[:,:,3]

# Create the inverted mask for the hat & monocle
orig_mask_inv = cv2.bitwise_not(orig_mask)
orig_mask_inv_m = cv2.bitwise_not(orig_mask_m)

# Convert hat & monocle image to BGR
# and save the original image size (used later when re-sizing the image)
imgHat = imgHat[:,:,0:3]
origHatHeight, origHatWidth = imgHat.shape[:2]
imgMonacle = imgMonacle[:,:,0:3]
origMonacleHeight, origMonacleWidth = imgMonacle.shape[:2]

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
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Iterate over each face found
    for (x, y, w, h) in faces:
        # Un-comment the next line for debug (draw box around all faces)
        # face = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        hatWidth = w * 3 / 2
        hatHeight = hatWidth * origHatHeight / origHatWidth

        x1 = x - (hatWidth/4)
        x2 = x + w + (hatWidth/4)
        y1 = y - (hatHeight*3/4)
        y2 = y + (hatHeight/4)

        if x1 < 0:
            x1 = 0
        if x2 > 1280:
            x2 = 1280
        if y1 < 0:
            y1 = 0
        if y2 > 960:
            y2 = 960

        hatHeight = y2 - y1
        hatWidth = x2 - x1

        #print hatWidth
        #print hatHeight

        hat = cv2.resize(imgHat, (hatWidth,hatHeight), interpolation = cv2.INTER_AREA)
        mask = cv2.resize(orig_mask, (hatWidth,hatHeight), interpolation = cv2.INTER_AREA)
        mask_inv = cv2.resize(orig_mask_inv, (hatWidth,hatHeight), interpolation = cv2.INTER_AREA)

        roi = frame[y1:y2, x1:x2]
        roi_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
        roi_fg = cv2.bitwise_and(hat,hat,mask = mask)
        dst = cv2.add(roi_bg,roi_fg)
        frame[y1:y2, x1:x2] = dst

        roi_gray_m = gray[y:y+h, x:x+w]
        roi_color_m = frame[y:y+h, x:x+w]

        # Detect an eye within the region bounded by each face (the ROI)
        eye = noseCascade.detectMultiScale(roi_gray_m)

        for (ex,ey,ew,eh) in eye:
            # Un-comment the next line for debug (draw box around the nose)
            cv2.rectangle(roi_color_m,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)

            monocleWidth = ew * 3
            monocleHeight = monocleWidth * origMonacleHeight / origMonacleWidth

            ex1 = ex - (monocleWidth/4)
            ex2 = ex + ew + (monocleWidth/4)
            ey1 = ey + eh - (monocleHeight/2)
            ey2 = ey + eh + (monocleHeight/2)

            if ex1 < 0:
                ex1 = 0
            if ex2 > ew + ex + ex:
                ex2 = ew + ex + ex
            if ey1 < 0:
                ey1 = 0
            if ey2 > eh + eh + ey:
                ey2 = eh + eh + ey

            monocleHeight = ey2 - ey1
            monocleWidth = ex2 - ex1

            print "EX: " + str(ex)
            print "EW: " + str(ew)
            print "EH: " + str(eh)
            print "EY: " + str(ey)
            #print eh
            #print ex2
            #print ex1
            print "MustsacheWidth" + str(monocleWidth)
            print "MustacheHeight" + str(monocleHeight)

            monocle = cv2.resize(imgMonacle, (monocleWidth,monocleHeight), interpolation = cv2.INTER_AREA)
            mask_m = cv2.resize(orig_mask_m, (monocleWidth,monocleHeight), interpolation = cv2.INTER_AREA)
            mask_inv_m = cv2.resize(orig_mask_inv_m, (monocleWidth,monocleHeight), interpolation = cv2.INTER_AREA)

            roi_m = roi_color_m[ey1:ey2, ex1:ex2]
            roi_bg_m = cv2.bitwise_and(roi_m,roi_m,mask = mask_inv_m)
            roi_fg_m = cv2.bitwise_and(monocle,monocle,mask = mask_m)
            dst_m = cv2.add(roi_bg_m,roi_fg_m)
            roi_color_m[ey1:ey2, ex1:ex2] = dst_m

            break

    # Display the resulting frame
    cv2.imshow('Live Feed', frame)

    # press any key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

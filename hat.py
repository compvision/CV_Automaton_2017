from SimpleCV import *
cam = Camera()
display = Display()
# load the cascades
hat = Image("hat.png", sample=True) # load the stache
mask = stache.createAlphaMask().invert() # load the stache mask
while display.isNotDone():
    img = cam.getImage()
    faces = img.findHaarFeatures("face.xml") #find faces
    if faces: # if we have a face
        faces.sortArea() #get the biggest one
        face = faces[-1] #last element
        # get the face image
        xf = face.x -(face.width()/2)
        yf = face.y
        #calculate the hat's position
        xmust = xf-(hat.width/2)
        ymust = (hat.height/3)
        #blit the stache/mask onto the image
        img = img.blit(stache, pos=(xmust,ymust), mask = mask)

img.save(display) #display

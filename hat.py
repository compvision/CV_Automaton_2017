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
        xf = face.width()/2
        yf = face.y
        #calculate the hat's position
        xmust = xf - (hat.width/2)
        ymust = yf + hat.height
        #blit the stache/mask onto the image
        img = img.sprite(hat, pos=(xmust,ymust), scale=1.0, rot=0.0, alpha=255)

img.save(display) #display

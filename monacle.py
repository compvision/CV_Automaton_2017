from SimpleCV import *

cam = Camera()
display = Display()

# load the cascades
monacle = Image("monacle.png") # load the stache
mask = monacle.createAlphaMask().invert() # load the stache mask

while display.isNotDone():
	img = cam.getImage()
	faces = img.findHaarFeatures("face.xml") #find faces

	if faces: # if we have a face
		faces.sortArea() #get the biggest one
		face = faces[-1] #last element
		myFace = face.crop() # get the face image
		eyes = myFace.findHaarFeatures('lefteye.xml') #find the eye
				
		if eyes:
			eyes.sortArea()
			eye = eyes[-1]
			#these get the upper left corner of the face/nose with respect to original image
			xf = face.x - (face.width()/2)
			yf = face.y - (face.height()/2)
			xe = eye.x - (eye.width()/2)
			ye = eye.y - (eye.height()/2)
			#calculate the monacle position
			xmust = xf + xe - (monacle.width/2) # + (eye.width()/2)
			ymust = yf-ye #+(2*nose.height()/3)
			#blit the stache/mask onto the image
			img = img.blit(monacle, pos=(xmust,ymust), mask = mask)
			img.save(display) #display
	img.save(display)

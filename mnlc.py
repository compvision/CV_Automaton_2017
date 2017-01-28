from SimpleCV import *
cam = Camera()
disp = Display()

monacle = Image("monacle.png") # load the stache
mask = monacle.createAlphaMask().invert() # load the stache mask

while disp.isNotDone():
        img = cam.getImage()
       
    img.save(disp)

import pyscreenshot as ImageGrab

if __name__=="__main__":
    im=ImageGrab.grab(bbox=(10,10,510,510))
    im.show()
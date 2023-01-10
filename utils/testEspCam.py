from esp32CamWiFiInterface import *

if __name__=="__main__":
    cam=ESP32CAM("192.168.174.4")
    if cam.isOnline():
        print(cam.ip)
        cam.setImgRes(IMG_RES_HD)
        cam.saveStill("./test.jpg")
    else:
        print("Can't connect with the cam")
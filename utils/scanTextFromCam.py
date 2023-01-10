from esp32CamWiFiInterface import *
import pytesseract
from PIL import Image

CAM_IP="http://192.168.174.4"

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'

if __name__=="__main__":
    cam=ESP32CAM(CAM_IP)
    if cam.isOnline():
        cam.setImgRes(IMG_RES_HD)
        cam.setImgQuality(IMG_QUALITY_BEST)
        cam.setImgBrightness(0)
        cam.saveStill("./temp.jpg")
        print(pytesseract.image_to_string(Image.open('./temp.jpg')))
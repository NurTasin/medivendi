import requests as req
from .camDefinitions import *

def _sanitize_ip(ip:str):
    if ip.endswith('/'):
        ip=ip[::-1]
    if not ip.startswith("http://"):
        ip="http://"+ip
    return ip

class ESP32CAM:
    def __init__(self,ip:str):
        """
        Initializes the ESP32CAM Object
        
        Parameters:
            ip         IP adress of the ESP32CAM
        Returns:
            None
        Example:
            `cam=ESP32CAM("192.168.0.4")`
        """
        self.ip=_sanitize_ip(ip)

    def _send_req(self,path:str,args:dict={}):
        res=req.get(self.ip+"/"+path,params=args)
        return res

    def _set_control(self,variable,value):
        res = self._send_req(CONTROL_PATH,{
            "var":variable,
            "val":value
        })
        return res.status_code==200
    
    def isOnline(self):
        """
        Returns True if the cam is online
        """
        try:
            req.get(self.ip,timeout=2)
        except req.exceptions.ConnectTimeout:
            return False
        
        return True
    
    def setImgRes(self,res:int):
        """
        Sets The Reselution of ESP32-CAM
        Parameters:
            res       Reselution of the camera you want to set to
        
        Example:
            `ESP32CAM.setImgRes(IMG_RES_HD)` will set the reselution to HD
        Returns:
            True if the operation was successful otherwise returns False
        """
        return self._set_control("framesize",res)
    
    def setImgBrightness(self,value:int):
        """
        Sets The Image Brightness of ESP32-CAM
        Parameters:
            value       Brightness of the camera you want to set to
        
        Example:
            `ESP32CAM.setImgBrightness(1)` will set the brightness to +1
        Returns:
            True if the operation was successful otherwise returns False
        """
        # Checking if brightness level is in limits
        if value>2:
            value=2
        if value<-2:
            value=-2
        
        return self._set_control("brightness",value)
    
    def setImgQuality(self,value:int):
        """
        Sets The Image Quality of ESP32-CAM
        Parameters:
            value       Quality of the camera you want to set to
        
        Example:
            `ESP32CAM.setImgQuality(IMG_QUALITY_BEST)` will set the Quality to BEST
        Returns:
            True if the operation was successful otherwise returns False
        """
        return self._set_control("quality",value)
    
    def setLEDIntensity(self,value:int):
        """
        Sets The LED (Flash) Intensity of ESP32-CAM
        Parameters:
            value       8bit PWM value (0-255)
        
        Example:
            `ESP32CAM.setLEDIntensity(128)` will set the LED Intensity to 128
        Returns:
            True if the operation was successful otherwise returns False
        """
        #Checking if the intensity level is in range
        if value>255:
            value=255
        if value<0:
            value=0
        return self._set_control("led_intensity",value)
    
    def saveStill(self,fpath):
        """
        Saves a image from the camera in JPG format
        Parameters:
            fpath      File name you want to save the image at.
        Returns:
            None
        Example:
            `ESP32CAM.saveStill("example.jpg")`
        """
        res=self._send_req("capture")
        if res.status_code==200:
            with open(fpath,"wb+") as handle:
                handle.write(res.content)
        else:
            print(f"[Error Occured] Status Code `{res.status_code}`")
    

        

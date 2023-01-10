import pytesseract
from PIL import Image
import requests as req
from urllib.parse import quote
from logger import LOG

pytesseract.pytesseract.tesseract_cmd ="C:\\Program Files\\Tesseract-OCR\\tesseract"

def getText(imagePath:str):
    return pytesseract.image_to_string(Image.open(imagePath),lang="eng+ben")

def in2in(arr1,string:str):
    for i in arr1:
        if i.lower() in string.lower():
            return True,string.lower().find(i.lower())
    return False,-1

def getMedicines(text:str):
    medicines=[]
    text_arr=text.split("\n")
    for i in text_arr:
        isMed=in2in(["CAP.","TAB.","SYR."],i)
        if isMed[0]:
            medicines.append(i[isMed[1]::])
    return medicines

def getMedicineDetails(name):
    res=req.get("https://api.arogga.com/v1/medicines/",params={
        "search":name
    })
    LOG(res.url)
    return res.json()["data"][0]

def getAllMedicineDetails(medlist):
    res=[]
    for med in medlist:
        res.append(getMedicineDetails(med))
    return res

if __name__=="__main__":
    test="""
Rx,
CAP. CEFIM-3 DS 400 MG

১0১৪ = খাওয়ার পরে ২ ৭ দিন
2. TAB. ACE XR 665 MG

১ +১+১+ ১টি -------- খাওয়ার পরে, জ্বর ১০১ ডিগ্রির উপরে হলে খাবেন
3. TAB. MAXPRO 20 MG

১৩৪ ১৪ sea খাওয়ার আরো ১০ মাস
4. TAB. FENADIN 120 MG

., ১ sees খাঙয়ার গরে ৮- ১০ দিন

উপদেশ
1. বেশি করে পানি পান করুন
2. সময়মত ঔষধ সেবন করুন
3. যে কোন সমস্যা হলে আগেই আসবেন
4, পরবর্তী সাক্ষাতে প্রেসক্রিপশন সাথে নিয়ে আসবেন

Dr. Md. Amirul Islam
"""
    print(getMedicines(test))

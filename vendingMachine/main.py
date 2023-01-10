from flask import Flask,jsonify,request,render_template,redirect,url_for
from flask_cors import CORS, cross_origin
from dbms import DBMS
from logger import *
from os import path
import uuid
from prescriptionHandler import getMedicines,getText,getAllMedicineDetails
import json

UPLOAD_FOLDER = path.abspath('./uploads')

app=Flask(__name__)
app_cors=CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

user_db=DBMS("./db/users.json")

@app.route("/",methods=["GET"])
@cross_origin()
def landingPage():
    return render_template("index.html")


@app.route('/medicine_list', methods = ['GET', 'POST'])
@cross_origin()
def upload_file():
    if request.method == 'POST':
      f = request.files['prescription']
      file_path=path.join(app.config["UPLOAD_FOLDER"],str(uuid.uuid4())[0::8]+"."+f.filename.split(".")[-1])
      f.save(file_path)
      INFO(f"New image uploaded. path: {file_path}")
      INFO(f"Running OCR on {file_path}")
      pres_text=getText(file_path)
      medicines=getMedicines(pres_text)
      INFO(f"Found {len(medicines)} medicines in {file_path}")
      INFO(f"Searching for details in Arogga API")
      medDetails=getAllMedicineDetails(medicines)
      INFO("Rendering and serving template")
      return render_template("medicine_details.html",details_group=medDetails)
    else:
        return redirect(url_for("landingPage"))
        
@app.route("/confirm_order",methods=["GET","POST"])
@cross_origin()
def ConfirmOrder():
    if request.method=="POST":
        medicines=json.loads(request.form.get("names"))
        cost=float(request.form.get("cost"))
        userid=str(request.form.get("usrid"))

        userdata=user_db.read()
        if userdata[userid]["token"] >= cost:
            userdata[userid]["token"]=userdata[userid]["token"]-cost
            user_db.write(userdata)
            #Do the hardwear magic!!
            return f"""Sucess!! {medicines} are given!! Cost : {cost} BDT deducted from USERID={userid} . New Balance : {userdata[userid]["token"]} BDT.
            Thank you ❤
"""
        else:
            return "Insufficient Ballance"

@app.route("/usr/<usrid>",methods=["GET","POST"])
@cross_origin()
def getUserDetails(usrid):
    usrid="USR_"+usrid
    if request.method=="GET":
        data=user_db.read()
        if usrid in data:
            return render_template("user.html",usr=data[usrid])
        else:
            return jsonify({"msg":"User not found!"}),404
    else:
        return jsonify({"msg":"For Security reasons we don't allow tresspassing"}),403

if __name__=="__main__":
    app.run("0.0.0.0",80,True)
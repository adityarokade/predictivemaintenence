
from flask import Flask,render_template,redirect

from wsgiref import simple_server

from flask import Flask, session, request, Response, jsonify
from Training import Training_Validation
from File_operations.File_operation import File_operation
from Prediction import Prediction
import atexit
import uuid
import os

import shutil
import pandas as pd



app = Flask(__name__)

@app.route('/train',methods=['GET','POST'])
def training():
    path="archive/CMaps/"
    train=Training_Validation(path)
    score,score1=train.Data_Validation()
    
    print("Train Complete",score,score1)
    return render_template('index.html')


@app.route('/',methods=['GET','POST'])
def Predict():
    if request.method=='POST':
        file=request.form['file']

        df=pd.read_csv(file,sep=" ",header=None)
        Input_File_Path="Prediction_Files/Input.csv"
        File_Operation=File_operation()
        File_Operation.Delete_Existing_File(Input_File_Path)
        df.to_csv(Input_File_Path,sep=",")
       
        pred=Prediction().Prediction()
       
    



              




    return render_template('index.html')
    # return "Flask app is running to good to go pankaj is chutiya"

@app.route('/Train_Profile_Report',methods=['GET','POST'])
def Train_profile_Report():
    return render_template("Train_Data_Profiling.html")



@app.route('/Test_Profile_Report',methods=['GET','POST'])
def Test_profile_Report():
    return render_template("Test_Data_Profiling.html")



port = int(os.getenv("PORT", 5001))

if __name__ == "__main__":
    host = '0.0.0.0'
    #app.run()
    httpd = simple_server.make_server(host=host, port=port, app=app)
    #httpd = simple_server.make_server(host='127.0.0.1', port=5000, app=app)
    # print("Serving on %s %d" % (host, port))
    httpd.serve_forever()

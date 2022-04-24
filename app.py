from flask import Flask,flash,redirect,render_template,request
from Training import Training_Validation
from Prediction import Prediction
from File_operations.File_operation import File_operation
import os
import shutil
import pandas as pd
import os









app=Flask(__name__)

# @app.route('/',methods=['GET'])
# # @cross_origin
# def Home():

#     return("<h1>hi to home page</h1>")

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

@app.route('/Train_Profile_Report',methods=['GET','POST'])
def Train_profile_Report():
    return render_template("Train_Data_Profiling.html")



@app.route('/Test_Profile_Report',methods=['GET','POST'])
def Test_profile_Report():
    return render_template("Test_Data_Profiling.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)

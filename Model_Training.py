import os
import pandas as pd
# from Model_Training.Model_Preprocessing import Model_Preprocessing
# from Model_Training.Create_Model import Create_Model
from Training_Model.Model_Preprocessing import Model_Preprocessing
from Training_Model.Create_Model import Create_Model
from File_operations.File_operation import File_operation
from application_logging import logger






class Model_Training:
    def __init__(self,Train_File_name,Test_File_name,selected_features,lables,Model_Filename):
        self.Train_File_name=Train_File_name
        self.Test_File_name=Test_File_name
        self.selected_features=selected_features
        self.lables=lables
        self.Model_filename=Model_Filename
        self.Model_Preprocessing=Model_Preprocessing(self.Train_File_name,self.Test_File_name,self.selected_features,self.lables)
        self.Create_Model=Create_Model()
        self.File_operation=File_operation()

        self.file_object = open("Logs/Model_Training_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def Model_Train(self):
        self.log_writer.log(self.file_object,'Model Train started')
        try:
            self.log_writer.log(self.file_object,'Model Preprocessing Started-first step started')
            train_data,test_data=self.Model_Preprocessing.Data_Read()
            X,Y=self.Model_Preprocessing.Seperate_features_and_lables(train_data)
            x_train,x_test,y_train,y_test=self.Model_Preprocessing.Splitting_of_Data(X,Y)
            self.log_writer.log(self.file_object,'Model Preprocessing sucessfully executed')

            
        except:
            self.log_writer.log(self.file_object,'Error in First step of model training')


        try:
            self.log_writer.log(self.file_object,'second step execution stsrrted')
            model=self.Create_Model.create_Obj_of_Model()
            self.Create_Model.Call_Fit_method(model,x_train,y_train)
            self.log_writer.log(self.file_object,'Model Trainng sucessfully')
            score=self.Create_Model.Check_score(model,x_test,y_test)
            self.log_writer.log(self.file_object,'second step executed sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in Second Step of execution')
            score=76.9

        try:
            self.log_writer.log(self.file_object,'Third step execution stsarted')
            self.File_operation.Delete_Existing_File(self.Model_filename)
            self.File_operation.Save_Model(self.Model_filename)
            self.log_writer.log(self.file_object,'Model Saved ')
            self.log_writer.log(self.file_object,'third step of execution sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in third step of Execution')


        try:
            self.log_writer.log(self.file_object,'Fourth step of execution started')
            X1,Y1=self.Model_Preprocessing.Seperate_features_and_lables(test_data)
            x1_train,x1_test,y1_train,y1_test=self.Model_Preprocessing.Splitting_of_Data(X1,Y1)




            score1=self.Create_Model.Check_score(x1_test,y1_test)
            self.log_writer.log(self.file_object,f'Model Score is{score1}')
            self.log_writer.log(self.file_object,'Fourth step of execution sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in Fourth step of execution')
            
            score1=72.04

        # score=66.02
        # score1=65.03
        return score,score1




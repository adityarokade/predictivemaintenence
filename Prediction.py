import os
import shutil
# from Prediction.Basic_Preprocessing import Basic_Preprocessing
# from Prediction.Data_Prediction import Data_Prediction
from Prediction_process.Basic_Preprocessing import Basic_Preprocessing
from Prediction_process.Data_Prediction import Data_Prediction
from File_operations.File_operation import File_operation
from application_logging import logger



# selected_features=['cycles', 'T24', 'T30', 'T50','P15', 'P30','Nf', 'Nc','Ps30','NRf', 'NRc', 'BPR']




class Prediction:
    def __init__(self):
        self.datapath="./Prediction_Files/Input1.csv"
        self.selected_features=['cycles', 'T24', 'T30', 'T50','P15', 'P30','Nf', 'Nc','Ps30','NRf', 'NRc', 'BPR']
        self.Model_Filename="./Forest_model_11.sav"
        # self.Model_Filename="./Forset_Model_11.sav"

        # Forset_Model_1.sav
        self.result_filename="./Result_Files/result11.csv"
        self.Basic_Preprocessing=Basic_Preprocessing(self.datapath,self.selected_features)
        self.File_operation=File_operation()
        self.Data_Prediction=Data_Prediction()
        self.file_object = open("Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def Prediction(self):
        try:
            self.log_writer.log(self.file_object,'Prediction Execution Started')
            try:
                self.log_writer.log(self.file_object,'First Step Of execution Started')
                df=self.Basic_Preprocessing.Data_Read()
                df=self.Basic_Preprocessing.Remove_Unwanted_Columns(df)

                df=self.Basic_Preprocessing.Give_column_names(df)
                df.to_csv("My_file.csv",sep=",")
                self.Basic_Preprocessing.Check_Missing_Value(df)
                X=self.Basic_Preprocessing.Select_Features(df)
                self.log_writer.log(self.file_object,'First Step Of execution Sucessfully...')
            except:
                print("Error in 1")
                self.log_writer.log(self.file_object,'Error in First Step Of Execution')

            try:
                self.log_writer.log(self.file_object,'Second Step Of Execution Started')
                self.log_writer.log(self.file_object,'Second Step loding model')
                loaded_model=self.File_operation.Load_Model(self.Model_Filename)
                self.log_writer.log(self.file_object,'Second step- model loaded ')
                result=self.Data_Prediction.Predict(loaded_model,X)
                self.log_writer.log(self.file_object,'Second Step prediction')
                df_new=self.Data_Prediction.Create_dataframe_of_result(result)
                self.log_writer.log(self.file_object,'Second Step  create dataframe')
                df_new=self.Data_Prediction.Insert_UnitID_column(df_new)

                self.log_writer.log(self.file_object,'Second Step  Insert unit id')

                self.Data_Prediction.Save_Result_file(df_new,self.result_filename)
                self.log_writer.log(self.file_object,'Second Step reesult file saved')
                print("result file saved ")
                
                self.log_writer.log(self.file_object,'Second Step Of execution sucessfully...')
            except:
                print("Errro in 2")
                self.log_writer.log(self.file_object,'Error in Second Step Of execution')
        except:
            print("Error in main")
            self.log_writer.log(self.file_object,'Error in Prediction Execution')
        # print("Prediction done")
        # abc="okk result"
        # return abc

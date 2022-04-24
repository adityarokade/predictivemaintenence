import os
import pandas as pd
import pickle
import numpy as np

from File_operations.File_operation import File_operation
from application_logging import logger




class Data_Prediction:
    def __init__(self):
        self.File_operation=File_operation()
        self.file_object = open("Logs/Data_Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def Predict(self,loaded_model,data):
        """
                                  Method Name: Predict
                                  Description: This function is used to Predict The Values  
                                  Output: 2D Array(Result)
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.loaded_model=loaded_model
        self.data=data
        try:

            result=self.loaded_model.predict(self.data)
            self.log_writer.log(self.file_object,'Data Prediction successfully')
        except:
            self.log_writer.log(self.file_object,'Error in Data Prediction')
        return result

    def Create_dataframe_of_result(self,result):
        """
                                  Method Name: Create_dataframe_of_result
                                  Description: This function is used to Create A Pandas Dataframe of given Result.
                                  Output: Pandas Dataframe
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.result=result
        try:

            df=pd.DataFrame(self.result)
            self.log_writer.log(self.file_object,'Dataframe created of Result successfully')
        except:
            self.log_writer.log(self.file_object,'Error in Creation of Dataframe')
        return df

    def Insert_UnitID_column(self,df):
        """
                                  Method Name: Insert_UnitID_column
                                  Description: This function is used to Insert UnitID column in result dataframe  
                                  Output: Pandas Dataframe(df)
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.df=df
        try:

            columns=['unit_ID','RUL']
            self.df.insert(0, 'unit_ID', range(1, 1 + len(df)))
            df.columns=columns
            df.astype(int)
            self.log_writer.log(self.file_object,'Insert UntitId successfully')
        except:
            self.log_writer.log(self.file_object,'Error in Insertion Of UnitId')

        return df

    def Save_Result_file(self,df,result_filename):
        """
                                  Method Name: Save_Result_file
                                  Description: This function is used to Save The Result File  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.df=df
        try:

            self.result_filename=result_filename
            self.File_operation.Delete_Existing_File(self.result_filename)
            self.df.to_csv(self.result_filename,sep=",")
            self.log_writer.log(self.file_object,'Result File Saved successfully')
        except:
            self.log_writer.log(self.file_object,'Error in Saving Result File')
        


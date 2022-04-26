import pandas as pd
import os
from sklearn.model_selection import train_test_split
from application_logging import logger



class Model_Preprocessing:
    def __init__(self,Train_File_name,Test_File_name,selected_features,lables):
        self.Train_File_name=Train_File_name
        self.Test_File_name=Test_File_name
        self.selected_features=selected_features
        self.lables=lables
        self.file_object = open("Logs/Model_Preprocessing_Training_Model_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

        

    def Data_Read(self):
        """
                                  Method Name: Data_Read
                                  Description: This function is used to Read Data From  CSV File
                                  Output: Data Frame 
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        try:
          
            train_data=pd.read_csv(self.Train_File_name)
            test_data=pd.read_csv(self.Test_File_name)
            self.log_writer.log(self.file_object,' Data Read Sucessfully')
         
        except:
            self.log_writer.log(self.file_object,' Error in Data Read')
        return train_data,test_data

        
       

    def Seperate_features_and_lables(self,data):
        """
                                  Method Name: Seperate_features_and_lables
                                  Description: This function is used to Seperate features and lables from dataframe  
                                  Output: Dataframes (features and lables)
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.data=data
        try:


            X=self.data[self.selected_features]
            Y=self.data[self.lables]
            self.log_writer.log(self.file_object,' Seperate Features Sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in Seperate Features')

        return X,Y
    def Splitting_of_Data(self,X,Y):
        """
                                  Method Name: Splitting_of_Data
                                  Description: This function is used to splitting of Data Using Train and test split  
                                  Output: Train and Test Split
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.X=X
        self.Y=Y
        try:

            x_train,x_test,y_train,y_test=train_test_split(self.X,self.Y)
            self.log_writer.log(self.file_object,'Splitting Of data Sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in splitting of data')
        return x_train,x_test,y_train,y_test


    



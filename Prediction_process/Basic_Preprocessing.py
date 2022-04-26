import os
import shutil
import pandas as pd
from application_logging import logger



class Basic_Preprocessing:
    def __init__(self,datapath,selected_features):
        self.column_names= ['Unnamed 0','unit_ID','cycles','setting_1','setting_2','setting_3','T2','T24','T30','T50','P2','P15','P30','Nf','Nc','epr','Ps30','phi','NRf','NRc','BPR','farB','htBleed','Nf_dmd','PCNfR_dmd','W31','W32' ]
        self.selected_features=selected_features
        self.datapath=datapath
        self.file_object = open("Logs/Basic_Preprocessing_prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()



    def Data_Read(self):
        """
                                  Method Name: Data_Read
                                  Description: This function is used to Read data  
                                  Output: Pandas Data Frame (Data)
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        try:

            df=pd.read_csv(self.datapath,header=None)
            self.log_writer.log(self.file_object,'Data Read successfully')
        except:
            self.log_writer.log(self.file_object,'Error In Data Read')
        return df

    def Remove_Unwanted_Columns(self,df):
        """
                                  Method Name: Remove_Unwanted_Columns
                                  Description: This function is used to Remove Unwanted Columns from Dataframe  
                                  Output: Pandas Data Frame
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.df=df
        try:

            self.df.drop(columns=[26,27],inplace=True)
            self.log_writer.log(self.file_object,'Column Drop [26,27] successfully')
        except:
             self.log_writer.log(self.file_object,'Error To Drop Columns')
        return self.df
    
    def Give_column_names(self,df):
        """
                                  Method Name: Give_column_names
                                  Description: This function is used to Give Column Names.  
                                  Output: Pandas Data Frame
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.df=df
        try:

            self.df.columns=self.column_names
            self.log_writer.log(self.file_object,'Columns names give successfully')
        except:
             self.log_writer.log(self.file_object,'Error to give  columns  names')
        return self.df


    def Check_Missing_Value(self,df):
        """
                                  Method Name: Check_Missing_Value
                                  Description: This function is used to create Check Missing Value.  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        
        self.df=df
        try:


            total = self.df.isnull().sum().sort_values(ascending=False)
            percent = (self.df.isnull().sum()/self.df.isnull().count()).sort_values(ascending=False)
            missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
            self.log_writer.log(self.file_object,'Missing value successfully')
        except:
             self.log_writer.log(self.file_object,'Error in Check Missing Value')
    
    def Select_Features(self,df):
        """
                                  Method Name: Select_Features
                                  Description: This function is used to Select Features From Data  
                                  Output: X(data)
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.df=df
        try:

            X=df[self.selected_features]
            self.log_writer.log(self.file_object,'Features selected successfully')
        except:
             self.log_writer.log(self.file_object,'Error in selection Of Features')
        return X
    
        
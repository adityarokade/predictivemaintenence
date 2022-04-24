import os
import shutil
import pandas as pd
import numpy as np
import glob
from application_logging import logger




class File_Preprocessing:
    def __init__(self,Data_Files_path,train_path,test_path,RUL_path):

        self.columns_train_and_test = ['unit_ID','cycles','setting_1','setting_2','setting_3','T2','T24','T30','T50','P2','P15','P30','Nf','Nc','epr','Ps30','phi','NRf','NRc','BPR','farB','htBleed','Nf_dmd','PCNfR_dmd','W31','W32' ]
        self.columns_RUL = ['RUL']
        self.Data_Files_path=Data_Files_path
        self.train_path=train_path
        self.test_path=test_path
        self.RUL_path=RUL_path
        self.file_object = open("Logs/File_Preprocessing_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def Read_CSV_Files(self):
        """
                                  Method Name: Read_CSV_Files
                                  Description: This function is used to Read CSV files   
                                  Output: List Of Dataframe Of Data Files
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        train_df_list=[]
        train_filename_list=[]

        test_df_list=[]
        test_filename_list=[]

        RUL_df_list=[]
        RUL_filename_list=[]

        train_file_path=os.path.join(self.Data_Files_path+self.train_path)
        test_file_path=os.path.join(self.Data_Files_path+self.test_path)
        RUL_file_path=os.path.join(self.Data_Files_path+self.RUL_path)
        # print("train_file_path",train_file_path)
        # print("test_file_path",test_file_path)
        # print("RUL_file_path",RUL_file_path)
        try:

            for file in glob.glob(f'{train_file_path}/*.txt'):
                df=pd.read_csv(file,sep=" ",header=None)
                train_df_list.append(df)
                train_filename_list.append(file)
            self.log_writer.log(self.file_object,'Read Train File sucessfully')

            for file in glob.glob(f'{test_file_path}/*.txt'):
                df=pd.read_csv(file,sep=" ",header=None)

                test_df_list.append(df)
                test_filename_list.append(file)

            self.log_writer.log(self.file_object,'Read Test File sucessfully')

            for file in glob.glob(f'{RUL_file_path}/*.txt'):
                df=pd.read_csv(file,sep=" ",header=None)

                RUL_df_list.append(df)
                RUL_filename_list.append(file)

            self.log_writer.log(self.file_object,'Read RUL file sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in Data read files')

        
        return train_df_list,train_filename_list,test_df_list,test_filename_list,RUL_df_list,RUL_filename_list

    def Remove_Unwanted_Columns(self,train_df_list,test_df_list,RUL_df_list):
        """
                                  Method Name: Remove_Unwanted_Columns
                                  Description: This function is used to Remove Unwanted Columns from Dataframe  
                                  Output: List Of Data Frames
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.train_df_list=train_df_list
        self.test_df_list=test_df_list
        self.RUL_df_list=RUL_df_list
        
        train_df1_list=[]
        test_df1_list=[]
        RUL_df1_list=[]
        

        try:


            for df in self.train_df_list:
                df.drop(columns=[26,27],inplace=True)
                train_df1_list.append(df)
                # print("REmoved column_Train")
                # df.to_csv(file,sep=',')
            self.log_writer.log(self.file_object,'Remove Unwanted columns sucessfully from train files')

            for df in self.test_df_list:
                
                df.drop(columns=[26,27],inplace=True)

                test_df1_list.append(df)
                # print("REmoved column_Test")
                # df.to_csv(file,sep=',')
            self.log_writer.log(self.file_object,'Remove Unwanted Columns sucessfully from test files')

            for df in self.RUL_df_list:
                
                df.drop(columns=[1],inplace=True)
                RUL_df1_list.append(df)
                # print("REmoved column_RUL")
                # df.to_csv(file,sep=',')

            self.log_writer.log(self.file_object,'Remove Unwanted Columns sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in Remove Unwanted Columns')

        return train_df1_list,test_df1_list,RUL_df1_list



    def Give_Column_Names(self,train_df1_list,test_df1_list,RUL_df1_list):
        """
                                  Method Name: Give_Column_Names
                                  Description: This function is used to Give Column Names Form List Of names to List Of Data Frames 
                                  Output: Data Frame
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.train_df1_list=train_df1_list
        self.test_df1_list=test_df1_list
        self.RUL_df1_list=RUL_df1_list


        train_df2_list=[]
        test_df2_list=[]
        RUL_df2_list=[]
        try:
            for df in self.train_df1_list:
                df.columns = self.columns_train_and_test
                train_df2_list.append(df)
            
            self.log_writer.log(self.file_object,'Give Columns names sucessfully for train')

            for df in self.test_df1_list:
                df.columns = self.columns_train_and_test
                test_df2_list.append(df)
            self.log_writer.log(self.file_object,'Give Columns names sucessfully for test')

            for df in self.RUL_df1_list:
                df.columns = self.columns_RUL
                df.insert(0, 'unit_ID', range(1, 1 + len(df)))
                RUL_df2_list.append(df)
            self.log_writer.log(self.file_object,'Give Column names sucessfully for RUL')
        except:
            self.log_writer.log(self.file_object,'Error in Give Column names')
        # df=pd.concat(train_df2_list,ignore_index=True)
        # df.to_csv("Train_Data.csv",sep=',')

        # df=pd.concat(test_df2_list,ignore_index=True)
        # df.to_csv("Test_Data.csv",sep=',')

        # df=pd.concat( RUL_df2_list,ignore_index=True)
        # df.to_csv("RUL_Data.csv",sep=',')

        
        return train_df2_list,test_df2_list,RUL_df2_list



    def Save_Csv_Files(self,train_df2_list,test_df2_list,RUL_df2_list,train_filename_list,test_filename_list,RUL_filename_list):
        """
                                  Method Name: Save_Csv_Files
                                  Description: This function is used to Save Files  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.train_df2_list=train_df2_list
        self.train_filename_list=train_filename_list

        self.test_df2_list=test_df2_list
        self.test_filename_list=test_filename_list


        self.RUL_df2_list=RUL_df2_list
        self.RUL_filename_list=RUL_filename_list

        try:


            for i in range(len(self.train_df2_list)):
                df=self.train_df2_list[i]
                file=self.train_filename_list[i]

                df.to_csv(file,sep=",")

            self.log_writer.log(self.file_object,'Files Are Saved sucessfully- train')

            for i in range(len(self.test_df2_list)):

                df=self.test_df2_list[i]
                file=self.test_filename_list[i]

                df.to_csv(file,sep=",")

            self.log_writer.log(self.file_object,'Files are Saved sucessfully-test')

            for i in range(len(self.RUL_df2_list)):

                df=self.RUL_df2_list[i]
                file=self.RUL_filename_list[i]

                df.to_csv(file,sep=",")

            self.log_writer.log(self.file_object,'Files are Saved sucessfully-RUL')
        except:
            pass











   

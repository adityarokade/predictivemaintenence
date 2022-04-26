import os
import pandas as pd
import glob
from pandas_profiling import ProfileReport
from application_logging import logger

class Basic_Train_Data_Preprocessing:
    def __init__(self):
        self.file_object = open("Logs/Basic_Train_Data_Preprocessing_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def Data_Read(self,Data_Files_path,train_path):
        """
                                  Method Name: Data_Read
                                  Description: This function is used to Read Data  
                                  Output: Data Frame
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.Data_Files_path=Data_Files_path
        self.train_path=train_path
       

        train_file_path=os.path.join(self.Data_Files_path+self.train_path)
        List_Df=[]
        try:

            for file in glob.glob(f'{train_file_path}/*.txt'):
                df=pd.read_csv(file)
                List_Df.append(df)
            self.log_writer.log(self.file_object,'Data Read and appended sucessfully')

        except:
            self.log_writer.log(self.file_object,'Error in Data Read and appended')
        return List_Df

    def Find_WhenMachineFail(self,List_df):
        """
                                  Method Name: Find_WhenMachineFail
                                  Description: This function is used to Find When Machine Fail  
                                  Output: List Of Dataframes 
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.List_df=List_df
        data_train_cycles_failure_list=[]
        try:

            for df in self.List_df:
                data_train_cycles_failure = pd.DataFrame(df.groupby('unit_ID')['cycles'].max()).reset_index()
                
                data_train_cycles_failure.columns = ['unit_ID', 'failure']
                data_train_cycles_failure_list.append(data_train_cycles_failure)
            self.log_writer.log(self.file_object,'Find WhenMachineFail and appended sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in Find WhenMachineFail')
        return data_train_cycles_failure_list

    def Marge(self,List_df,data_train_cycles_failure_list):
        """
                                  Method Name: Marge
                                  Description: This function is used to Marge files Of Some Columns Like RUL ,etc  
                                  Output: List Of Dataframe
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.List_df=List_df
        
        self.data_train_cycles_failure_List=data_train_cycles_failure_list
        List_df_1=[]
        try:

            for i in range(len(self.List_df)):
                df=self.List_df[i]
                data_train_cycles_failure=self.data_train_cycles_failure_List[i]
                df=df.merge(data_train_cycles_failure,on=['unit_ID'],how='left')
                df['RUL']=df['failure']-df["cycles"]
                List_df_1.append(df)
            self.log_writer.log(self.file_object,'Data Marge and appended sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in Marge')
        return List_df_1

    # def Save_Files(self,List_df_1,Data_Files_path,train_path):
    #     self.Data_Files_path=Data_Files_path
    #     self.train_path=train_path
    #     train_file_path=os.path.join(self.Data_Files_path+self.train_path)
    #     self.List_df_1=List_df_1
    #     file_path_list=glob.glob(f'{train_file_path}/*.txt')
    #     for i in range(len(List_df_1)):
    #         df=self.List_df_1[i]
    #         file=file_path_list
    #         df.to_csv(file,sep=',')


    def Check_Missing_Value(self,List_Df_1):
        """
                                  Method Name: Check_Missing_Value
                                  Description: This function is used to Check Missing Value  
                                  Output: Data Frame Of Missing Value
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        
        self.List_Df=List_Df_1
        try:

            for df in self.List_Df:

                total = df.isnull().sum().sort_values(ascending=False)
                percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
                missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
            self.log_writer.log(self.file_object,'Check Missing Value sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in check Missing Value')
            # missing_data
    
    # def Profiling(self,List_Df_1):
    #     # files=glob.glob(f'{self.TrainFile_path}/*.txt')
        
    #     self.List_Df=List_Df_1
    #     for i in range(len(self.List_Df)):
    #         df=self.List_Df[i]

    #         name=(f"./Visulization/Pandas_Profile{i}.html")
    #         pf = ProfileReport(df)
    #         pf.to_widgets()
    #         pf.to_file(name)



    def concat_files(self,List_Df_1,Total_Train_Data):
        """
                                  Method Name: concat_files
                                  Description: This function is used to concat Files to one  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.Total_Train_Data=Total_Train_Data
        self.List_Df=List_Df_1
        try:

            df=pd.concat(self.List_Df,ignore_index=True)
            # df.to_csv("./Total_Train_Data.csv",sep=',')
            df.to_csv(self.Total_Train_Data,sep=',')
            self.log_writer.log(self.file_object,'Data Concated at one file sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in Concation of Files')



    def Profiling(self,Total_Train_Data):
        """
                                  Method Name: Profiling
                                  Description: This function is used to Create Profile Report using Pandas Profiling  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        # files=glob.glob(f'{self.TrainFile_path}/*.txt')
        
        self.Total_Train_Data=Total_Train_Data
        try:

            name="./temlates/Train_Data_Profiling.html"
            df=pd.read_csv(self.Total_Train_Data)

            pf = ProfileReport(df)
            # pf.to_widgets()
            pf.to_file(name)
            self.log_writer.log(self.file_object,'Pandas Profiling sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in Pandas Profiling')
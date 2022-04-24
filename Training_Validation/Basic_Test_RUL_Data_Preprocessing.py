import os
import pandas as pd
import glob
from pandas_profiling import ProfileReport
from application_logging import logger


class Basic_Test_RUL_Data_Preprocessing:
    def __init__(self):
        self.file_object = open("Logs/Basic_Test_Rul_Data_Preprocessing_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def Data_Read(self,Data_Files_path,test_path,RUL_path):
        """
                                  Method Name: Data_Read
                                  Description: This function is used to Read Data  
                                  Output: Dataframe
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.Data_Files_path=Data_Files_path
        self.test_path=test_path
        self.RUL_path=RUL_path
        List_test_Df=[]
        List_RUL_Df=[]
        try:

            test_file_path=os.path.join(self.Data_Files_path+self.test_path)
            RUL_file_path=os.path.join(self.Data_Files_path+self.RUL_path)
            
            for file in glob.glob(f'{RUL_file_path}/*.txt'):
                df=pd.read_csv(file)
                List_RUL_Df.append(df)
                self.log_writer.log(self.file_object,'RUL Data Read sucessfully')
            for file in glob.glob(f'{test_file_path}/*.txt'):
                df=pd.read_csv(file)
                List_test_Df.append(df)
                self.log_writer.log(self.file_object,'test Data Read sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in Data read')
        return List_test_Df,List_RUL_Df


    def Get_Max_Cycles(self,List_test_Df):
        """
                                  Method Name: Get_Max_Cycles
                                  Description: This function is used to Get_Max_Cycles  
                                  Output: Max Cycles List of each Dataframe
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        
        self.List_test_Df=List_test_Df
        data_test_cycles_MAX_List=[]
        try:

            for i in range(len(self.List_test_Df)):
                df=self.List_test_Df[i]
                
                data_test_cycles_MAX = pd.DataFrame(df.groupby('unit_ID')['cycles'].max()).reset_index()
                data_test_cycles_MAX.columns = ['unit_ID', 'cycles MAX']
                data_test_cycles_MAX_List.append(data_test_cycles_MAX)
                self.log_writer.log(self.file_object,'Get_Max_Cycles sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in GET_Max_Cycles')

        return data_test_cycles_MAX_List

    def Marge_RUL_To_Test(self,List_test_Df,List_RUL_Df,data_test_cycles_MAX_List):
        """
                                  Method Name: Marge_Rul_To_Test
                                  Description: This function is used to Marge Rul DataFile To Test File  
                                  Output:  Pandas Dataframe
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        
        self.List_RUL_Df=List_RUL_Df
        self.List_test_Df=List_test_Df
        self.data_test_cycles_MAX_List=data_test_cycles_MAX_List
        Test_df_List=[]
        try:

            for i in range(len(self.List_test_Df)):
                RUL_df=self.List_RUL_Df[i]
                Test_df=self.List_test_Df[i]
                data_test_cycles_MAX =self.data_test_cycles_MAX_List[i]
                Test_df=Test_df.merge(RUL_df,on=['unit_ID'],how='left')
                Test_df=Test_df.merge(data_test_cycles_MAX,on=['unit_ID'],how='left')
                Test_df['failure']=Test_df['cycles MAX']+Test_df['RUL']
                Test_df_List.append(Test_df)
                self.log_writer.log(self.file_object,'Marge RUL To Test sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in Marge RUL to Test')

        return Test_df_List

    # def Save_Files(self,Test_df_List,Data_Files_path,test_path):
    #     self.Data_Files_path=Data_Files_path
    #     self.test_path=test_path
    #     test_file_path=os.path.join(self.Data_Files_path+self.test_path)
    #     self.Test_df_List=Test_df_List
    #     file_path_list=glob.glob(f'{test_file_path}/*.txt')
    #     for i in range(len(self.Test_df_List)):
    #         df=self.Test_df_List[i]
    #         file_path=file_path_list[i]
    #         df.to_csv(file_path,sep=',')


    def Check_Missing_Value(self,Test_df_List):
        """
                                  Method Name: Check_Missing_Value
                                  Description: This function is used to Check the missing Value From Dataframe.  
                                  Output: Dataframe Of Missing Value In Percentage By Column names
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        
        self.List_Df=Test_df_List
        try:

            for df in self.List_Df:

                total = df.isnull().sum().sort_values(ascending=False)
                percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
                missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
                self.log_writer.log(self.file_object,'Check missing value sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in Check Missing Value')
            # missing_data

    def concat_files(self,Test_df_List,Total_Test_Data):
        """
                                  Method Name: Concat_files
                                  Description: This function is used to Concate The files To marge The All files to one   
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.Total_Test_Data=Total_Test_Data
        self.List_Df=Test_df_List
        try:

            df=pd.concat(self.List_Df,ignore_index=True)
            # df.to_csv("./Total_Test_Data.csv",sep=',')
            df.to_csv(self.Total_Test_Data,sep=',')
            self.log_writer.log(self.file_object,'Files are Concated at One file')
        except:
            self.log_writer.log(self.file_object,'Error in Concating File To one ')

    def Profiling(self,Total_Test_Data):
        """
                                  Method Name: Profiling
                                  Description: This function is used to Load Pandas  Profiling.  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        # files=glob.glob(f'{self.TrainFile_path}/*.txt')
        
        self.Total_Test_Data=Total_Test_Data
        try:

            name="./templates/Test_Data_Profiling.html"
            df=pd.read_csv(self.Total_Test_Data)

            pf = ProfileReport(df)
            # pf.to_widgets()
            pf.to_file(name)
            self.log_writer.log(self.file_object,' Pandas Profiling is sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in Pandas Profiling')
import os
import shutil
from Training_Validation.File_Selection import File_Selection
from Training_Validation.File_Preprocessing import File_Preprocessing
from Training_Validation.Basic_Train_Data_Preprocessing import Basic_Train_Data_Preprocessing
from Training_Validation.Basic_Test_RUL_Data_Preprocessing import Basic_Test_RUL_Data_Preprocessing
from File_operations.File_operation import File_operation
from Model_Training import Model_Training
from Database_Management.Cassandra_DBMS import Cssandra_Management
from application_logging import logger
import time




class Training_Validation:
    def __init__(self,path):
        self.src_Data_path=path
        self.Raw_data_path="./Raw_data_files/"
        self.Data_Files_path='./Data_Files/'
        self.train_path='Train_files'
        self.test_path='Test_files'
        self.RUL_path='RUL_files'
        self.Total_Train_Data="./Total_Train_Data.csv"
        self.Total_Test_Data="./Total_Test_Data.csv"
        self.selected_features=['cycles', 'T24', 'T30', 'T50','P15', 'P30','Nf', 'Nc','Ps30','NRf', 'NRc', 'BPR']
        self.lables='RUL'
        self.Model_Filename="./Forest_model_11.sav"
        # self.Model_Filename="./Forset_Model_11.sav"
        self.File_Selection=File_Selection()
        self.File_Preprocessing=File_Preprocessing(self.Data_Files_path,self.train_path,self.test_path,self.RUL_path)
        self.Basic_Train_Data_Preprocessing=Basic_Train_Data_Preprocessing()
        self.Basic_Test_RUL_Data_Preprocessing=Basic_Test_RUL_Data_Preprocessing()
        self.File_operation=File_operation()

        self.Model_Training=Model_Training(self.Total_Train_Data,self.Total_Test_Data,self.selected_features,self.lables,self.Model_Filename)
        self.Cassandra_management=Cssandra_Management()

        self.file_object = open("Logs/Training_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()



    def Data_Validation(self):
        try:
            self.log_writer.log(self.file_object,'Data Validation started')

            try:
                self.log_writer.log(self.file_object,'First Step Of Execution Started')
                self.File_Selection.Take_Data_Files(self.src_Data_path,self.Raw_data_path)
                self.File_Selection.Remove_unwanted_files(self.Raw_data_path)
                self.File_Selection.Create_seperate_Files(self.Raw_data_path,self.Data_Files_path,self.train_path,self.test_path,self.RUL_path)
                train_regex_list,test_regex_list,RUL_regex_list=self.File_Selection.Regex_create()
                self.File_Selection.Seperate_Files(self.Raw_data_path,train_regex_list,test_regex_list,RUL_regex_list)

                self.log_writer.log(self.file_object,'First Step Of Execution sucessfully...')
            except:
                self.log_writer.log(self.file_object,'Error in Execution Of First step')
            print("ALL OK")
            try:
                self.log_writer.log(self.file_object,'Second Step Of Execution Started')

                train_df_list,train_filename_list,test_df_list,test_filename_list,RUL_df_list,RUL_filename_list=self.File_Preprocessing.Read_CSV_Files()

                train_df1_list,test_df1_list,RUL_df1_list=self.File_Preprocessing.Remove_Unwanted_Columns(train_df_list,test_df_list,RUL_df_list)

                train_df2_list,test_df2_list,RUL_df2_list=self.File_Preprocessing.Give_Column_Names(train_df1_list,test_df1_list,RUL_df1_list)
                
                self.File_Preprocessing.Save_Csv_Files(train_df2_list,test_df2_list,RUL_df2_list,train_filename_list,test_filename_list,RUL_filename_list)

                self.log_writer.log(self.file_object,'Second Step Of Execution Secussfully...')
            except:
                self.log_writer.log(self.file_object,'Error in Execution Of second step')
            print("All OKK 2")
            try:
                self.log_writer.log(self.file_object,'Third Step Of Execution Started')

                List_Df=self.Basic_Train_Data_Preprocessing.Data_Read(self.Data_Files_path,self.train_path)
                data_train_cycles_failure_list=self.Basic_Train_Data_Preprocessing.Find_WhenMachineFail(List_Df)
                List_df_1=self.Basic_Train_Data_Preprocessing.Marge(List_Df,data_train_cycles_failure_list)


                self.Basic_Train_Data_Preprocessing.Check_Missing_Value(List_df_1)
                
                self.File_operation.Delete_Existing_File(self.Total_Train_Data)
                self.Basic_Train_Data_Preprocessing.concat_files(List_df_1,self.Total_Train_Data)
                self.Basic_Train_Data_Preprocessing.Profiling(self.Total_Train_Data)
                self.log_writer.log(self.file_object,'Third Step Of Execution sucessfully...')
            except:
                self.log_writer.log(self.file_object,'Error in Execution Third step')
            # 
            try:
                self.log_writer.log(self.file_object,'Fourth Step Of Execution Started')

                session=self.Cassandra_management.Create_Connection()
                uniqueName = time.asctime().replace(" ", "_").replace(":", "")
                Dbname="Train"+uniqueName

                # uniqueName = time.asctime().replace(" ", "_").replace(":", "")
                self.Cassandra_management.Create_Table(session,self.Total_Train_Data,Dbname)
                self.Cassandra_management.Insert_Values(session,self.Total_Train_Data,Dbname)
                self.log_writer.log(self.file_object,'Fourth Step Of Execution sucessfully...')
            except:
                self.log_writer.log(self.file_object,'Error in Execution Fourth step')


            
            try:
                self.log_writer.log(self.file_object,'Fiveth Step Of Execution Started')

                List_test_Df,List_RUL_Df=self.Basic_Test_RUL_Data_Preprocessing.Data_Read(self.Data_Files_path,self.test_path,self.RUL_path)
                data_test_cycles_MAX_List=self.Basic_Test_RUL_Data_Preprocessing.Get_Max_Cycles(List_test_Df)
                Test_df_List=self.Basic_Test_RUL_Data_Preprocessing.Marge_RUL_To_Test(List_test_Df,List_RUL_Df,data_test_cycles_MAX_List)


                self.Basic_Test_RUL_Data_Preprocessing.Check_Missing_Value(Test_df_List)
                self.File_operation.Delete_Existing_File(self.Total_Test_Data)
                self.Basic_Test_RUL_Data_Preprocessing.concat_files(Test_df_List,self.Total_Test_Data)
                self.Basic_Test_RUL_Data_Preprocessing.Profiling(self.Total_Test_Data)
                self.log_writer.log(self.file_object,'Fiveth Step Of Execution sucessfully...')
            except:
                self.log_writer.log(self.file_object,'Error in Execution Fivth step')

            try:
                self.log_writer.log(self.file_object,'Sixth Step Of Execution Started')

                session=self.Cassandra_management.Create_Connection()
                # DBNAME=time.asctime().replace(" ", "_").replace(":", "")
                uniqueName1 = time.asctime().replace(" ", "_").replace(":", "")
                Dbname1="Test"+uniqueName1
                self.Cassandra_management.Create_Table(session,self.Total_Test_Data,Dbname1)
                self.Cassandra_management.Insert_Values(session,self.Total_Test_Data,Dbname1)
                self.log_writer.log(self.file_object,'Sixth Step Of Execution sucessfully...')
            except:
                self.log_writer.log(self.file_object,'Error in Execution Sixth step')

            



            try:
                self.log_writer.log(self.file_object,'Seventh Step Of Execution Started')

                score,score1=self.Model_Training.Model_Train()
                self.log_writer.log(self.file_object,'Seventh Step Of Execution sucessfully...')
            except:
                self.log_writer.log(self.file_object,'Error in Execution Seventh step')
        except:
            self.log_writer.log(self.file_object,'Error in Data Validation')
        return score,score1







        
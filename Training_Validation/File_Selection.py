import os
import shutil
import glob

from File_operations.File_operation import File_operation
from application_logging import logger


class File_Selection:
    def __init__(self):
        self.readme='readme.txt'
        self.x='x.txt'
        self.File_operation=File_operation()
        self.file_object = open("Logs/File_Selection_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()


    
    

    def Take_Data_Files(self,src_data_path,Raw_data_path):
        """
                                  Method Name: Take_Data_Files
                                  Description: This function is used to pick up data files to new folder  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.Raw_data_path=Raw_data_path
        self.src_data_path=src_data_path
        try:

            self.File_operation.Delete_Existing_Directory(self.Raw_data_path)
            self.File_operation.Create_Directory(self.Raw_data_path)
            datafiles=glob.glob(f"{self.src_data_path}/*.txt")
            
            for file in datafiles:
                shutil.copy(file,self.Raw_data_path)
                self.log_writer.log(self.file_object,f'{file} Are Copied to {self.Raw_data_path}')
        except:
            self.log_writer.log(self.file_object,'Error in coping Files')
            


    def Remove_unwanted_files(self,Raw_data_path):
        """
                                  Method Name: Remove_unwanted_files
                                  Description: This function is used to Remove unwanted files  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.Raw_data_path=Raw_data_path
        try:

            path_readme=os.path.join(self.Raw_data_path+self.readme)
            path_x=os.path.join(self.Raw_data_path+self.x)


            if os.path.isfile(path_readme):
                os.remove(path_readme)
                self.log_writer.log(self.file_object,f'{self.readme} Removed from {self.Raw_data_path}')

            if os.path.isfile(path_x):
                os.remove(path_x)
                self.log_writer.log(self.file_object,f'{self.x}Removed From  {self.Raw_data_path}')
        except:
            self.log_writer.log(self.file_object,'Error in Removing Unwanted Files')

    def Create_seperate_Files(self,Raw_data_path,Data_Files_path,train_path,test_path,RUL_path):
        self.Raw_data_path=Raw_data_path
        self.Data_Files_path=Data_Files_path
        self.train_path=train_path
        self.test_path=test_path
        self.RUL_path=RUL_path
        try:

            train_data_path=os.path.join(self.Data_Files_path+self.train_path)
            self.File_operation.Delete_Existing_Directory(train_data_path)
            self.File_operation.Create_Directory(train_data_path)

            test_data_path=os.path.join(self.Data_Files_path+self.test_path)

            self.File_operation.Delete_Existing_Directory(test_data_path)
            self.File_operation.Create_Directory(test_data_path)

            RUL_data_path=os.path.join(self.Data_Files_path+self.RUL_path)

            self.File_operation.Delete_Existing_Directory(RUL_data_path)
            self.File_operation.Create_Directory(RUL_data_path)

            self.log_writer.log(self.file_object,'Seperate Files are created')
        except:
            self.log_writer.log(self.file_object,'Error In Create Seperate Files')

    def Regex_create(self):
        """
                                  Method Name: Regex_create
                                  Description: This function is used to Create a regex of filename  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        train_regex_list=[]
        test_regex_list=[]
        RUL_regex_list=[]
        try:

            for i in range(1,5):
                train_regex=f"train_FD00{i}.txt"
                test_regex=f"test_FD00{i}.txt"
                RUL_regex=f"RUL_FD00{i}.txt"

                train_regex_list.append(train_regex)
                test_regex_list.append(test_regex)
                RUL_regex_list.append(RUL_regex)
            self.log_writer.log(self.file_object,'Regex Created sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in Regex Creation')

        return train_regex_list,test_regex_list,RUL_regex_list
        
    def Seperate_Files(self,Raw_data_path,train_regex_list,test_regex_list,RUL_regex_list):
        """
                                  Method Name: Seperate Files
                                  Description: This function is used to Seperate files  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.Raw_data_path=Raw_data_path
        self.train_regex_list=train_regex_list
        self.test_regex_list=test_regex_list
        self.RUL_regex_list=RUL_regex_list
        train_data_path='./Data_Files/Train_files/'
        test_data_path='./Data_Files/Test_files/'
        RUL_data_path='./Data_Files/RUL_files/'
        
        
            # train_file_path=os.path.join(train_data_path+train_regex)
        try:

            datafiles=glob.glob(f"{self.Raw_data_path}/*.txt")
            
            for file in datafiles:
            
                for i in range(4):
                    train_regex=self.train_regex_list[i]
                    test_regex=self.test_regex_list[i]
                    RUL_regex=self.RUL_regex_list[i]
                    file_path_train=os.path.join(self.Raw_data_path,train_regex)
                    file_path_test=os.path.join(self.Raw_data_path,test_regex)
                    file_path_RUl=os.path.join(self.Raw_data_path,RUL_regex)
                    
                    if file==file_path_train:
                        shutil.move(file,train_data_path)
                        print(f"File Moved{file}TO {train_data_path}")
                    else:
                        pass
                        
                    if file==file_path_test:
                        shutil.move(file,test_data_path)
                        print(f"File Moved{file}TO {test_data_path}")
                    else:
                        pass
                    if file==file_path_RUl:
                        shutil.move(file,RUL_data_path)
                        print(f"File Moved{file}TO {RUL_data_path}")
                    else:
                        pass
            self.log_writer.log(self.file_object,'seperate Files Are Sucessfully')
            self.File_operation.Delete_Existing_Directory(self.Raw_data_path)
        except:
            self.log_writer.log(self.file_object,'Error in Seperate Files')
        
# self.RUL_regex_list
        
# train_FD001.txt
    
# ./Raw_data_files/train_FD001.txt



# regex = "['qsar']+['_']+['fish']+['_']+['toxicity']+.csv"
# qsar_fish_toxicity.csv
# train_regex=f"['train']+['_']+['FD00']+['{i}'].txt"
#test_regex=f"['test']+['_']+['FD00']+['{i}'].txt"
#RUL_regex=f"['RUL']+['_']+['FD00']+['{i}'].txt"
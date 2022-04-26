import os
import shutil
import pickle
from application_logging import logger



class File_operation:
    def __init__(self):
        self.file_object = open("Logs/File_operation_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()
        
        

    def Create_Directory(self,path):
        """
                                  Method Name: Create_Directory
                                  Description: This function is used to create Directory using Os Module.  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.path=path
        
        try:
            
            if not os.path.isdir(self.path):
                os.makedirs(self.path)
                self.log_writer.log(self.file_object,f'{self.path}Directory created')
                

        except:
            self.log_writer.log(self.file_object,'Directory Not created')
            

            

    def Delete_Existing_Directory(self,path):
        """
                                  Method Name: Delete_Existing_Directory
                                  Description: This function is used to Delete_Existing_Directory.  
                                  Output: None.
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.path=path
        try:

            if os.path.isdir(self.path):
                shutil.rmtree(self.path)
                self.log_writer.log(self.file_object,f'{self.path} Directory Removed')
        except:
            self.log_writer.log(self.file_object,f'{self.path}Directory not Removed')

    def Delete_Existing_File(self,file):
        """
                                  Method Name: Delete_Existing_File
                                  Description: This function is used to Delete_Existing_File  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.file=file
        try:

            if os.path.isfile(self.file):
                os.remove(self.file)
                self.log_writer.log(self.file_object,f'{self.file}File Removed')
        except:
            self.log_writer.log(self.file_object,f'{self.file}File Not Removed')


    def Save_Model(self,model,Filename):
        """
                                  Method Name: Save_Model
                                  Description: This function is used to Save_Model  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.model=model
        self.Filename=Filename
        try:

            pickle.dump(self.model,open(self.Filename,'wb'))
            self.log_writer.log(self.file_object,f'{self.Filename}Model Saved')
        except:
            self.log_writer.log(self.file_object,f'{self.Filename}Error In Model Saving')


    def Load_Model(self,Filename):
        """
                                  Method Name: Load_Model
                                  Description: This function is used to Load_Model from saved File  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.Filename=Filename
        try:

            model=pickle.load(open(self.Filename,'rb'))
            self.log_writer.log(self.file_object,'Model Loading Completed')
        except:
            self.log_writer.log(self.file_object,'Error In Model Loading')
        return model


   

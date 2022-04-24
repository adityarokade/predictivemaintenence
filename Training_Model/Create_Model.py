import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
from application_logging import logger



class Create_Model:
    def __init__(self):
        self.file_object = open("Logs/Create_Model_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def create_Obj_of_Model(self):
        """
                                  Method Name: create_Obj_of_Model
                                  Description: This function is used to create Object of Model.  
                                  Output: class object os model class
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        try:

            model=RandomForestRegressor(n_estimators=300,random_state=0)
        # model=RandomForestRegressor(n_estimators=6,random_state=0)
            self.log_writer.log(self.file_object,' models Object Created Sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in object creation ')
        return model

    def Call_Fit_method(self,model,x_train,y_train):
        """
                                  Method Name: Call_Fit_method
                                  Description: This function is used to Call Fit Method using class object to train model
                                  Output: Model
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.model=model
        self.x_train=x_train
        self.y_train=y_train
        try:

            self.model.fit(self.x_train,self.y_train)
            self.log_writer.log(self.file_object,'Fit Method Called sucessfully')
        except:
            self.log_writer.log(self.file_object,'Error in calling fit method')

        return self.model

    def Check_score(self,model,x_test,y_test):
        """
                                  Method Name: Check_score
                                  Description: This function is used to Check The Score Of Train Model.
                                  Output: int(score in Int Format)
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.model=model
        self.x_test=x_test
        self.y_test=y_test
        try:

            score=self.model.score(x_test,y_test)
            self.log_writer.log(self.file_object,f'Score checked Sucessfully,score is-{score}')
        except:
            self.log_writer.log(self.file_object,'Error in check score')
        return score



from datetime import datetime


class App_Logger:
    def __init__(self):
        pass

    def log(self, file_object, log_message):
        """
                                  Method Name: log
                                  Description: This function is used for Writting logs
                                    
                                  Output: log in terms of text
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        try:

            self.now = datetime.now()
            self.date = self.now.date()
            self.current_time = self.now.strftime("%H:%M:%S")
            file_object.write(str(self.date) + "/" + str(self.current_time) + "\t\t" + log_message +"\n")
        except:
            pass
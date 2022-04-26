import os
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import csv
from application_logging import logger


class Cssandra_Management:
    def __init__(self):
        self.file_object = open("Logs/Database_Log.txt", 'a+')
        self.log_writer = logger.App_Logger() 

    def Create_Connection(self):
        """
                                  Method Name: Create_Connection
                                  Description: This function is used to create Connection For Execute Querys  
                                  Output: session(connection)
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        try:

            cloud_config= {'secure_connect_bundle':'secure-connect-predictive-maintenence.zip'}
            auth_provider = PlainTextAuthProvider('TwftYiLLzOPdWfCjSuKRWGcj', 'N30vWjycqEiRHlUq7-q.gC5bHLM0xfUWmB_S5W8zoBNjzGZCOta1M3ZIbPLun3mPkypoG7d9CmBop40acOX1ZhTXc+ipoBh7IT_umeDwZS8sj4+Ki9nXAw0,Wc72pX,H')
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect()
            self.log_writer.log(self.file_object,'Database Connection Created')
            print("conn created")
        except:
           self.log_writer.log(self.file_object,'Error in create Connection')
        return session

    def Create_Table(self,session,filename,Dbname):
        """
                                  Method Name: Create_Table
                                  Description: This function is used to create Tables for inseting Data  
                                  Output:None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.session=session
        self.filename=filename
        self.dbname=Dbname
        try:
                
            # df=pd.read_csv("Total_Train_Data.csv")
            df=pd.read_csv(self.filename)
            # df.drop(columns=['Unnamed: 0.1'],inplace=True)
            try:
                df.drop(columns=['Unnamed: 0.1'],inplace=True)
            except:
                pass
            try:
                df.drop(columns=['Unnamed: 0_x'],inplace=True)
            except:
                pass
            column_list=df.columns

            dtype_list=[]
            for i in column_list:
                a=str(df[i].dtype)
                dtype_list.append(a)
            list_total=[]

            for i in range(len(column_list)):
                a=column_list[i]
                a=a.replace(" ","").replace(":","")
        
        
                b=dtype_list[i]
                list_total.append(a)
                if b  in ['float8','float16','float32','float64']:
                    c='float'
                    list_total.append(c)
                if b  in ['int8','int16','int32','int64']:
                    c='int'
                    list_total.append(c)
            
        
        
        
                if a=="Unnamed0":
                    list_total.append("PRIMARY KEY")
                list_total.append(',')
            list_total.pop(-1)
            tu=" ".join(list_total)
            aa=f"CREATE TABLE train_data.{self.dbname}({tu});"
            self.log_writer.log(self.file_object,'query created')
            self.session.execute(aa)
            self.log_writer.log(self.file_object,'Table Created')
        except:
            self.log_writer.log(self.file_object,'Error in Table Creation')



    def Insert_Values(self,session,filename,Dbname):
        """
                                  Method Name: Insert_Values
                                  Description: This function is used to Insert Values In Database(Cassandra)  
                                  Output: None
                                  On Failure: Exception
                                  Written By: Aditya Rokade
                                  Version: 1.0
                                  Revisions: None
                              """
        self.session=session
        self.filename=filename
        self.dbname=Dbname
        try:

            # df=pd.read_csv("Total_Train_Data.csv")
            df=pd.read_csv(self.filename)
            try:
                df.drop(columns=['Unnamed: 0.1'],inplace=True)
            except:
                pass
            try:
                df.drop(columns=['Unnamed: 0_x'],inplace=True)
            except:
                pass
            column_list=df.columns
            list_total=[]
            for i in range(len(column_list)):
                a=column_list[i]
                a=a.replace(" ","").replace(":","")
        
        
                
                list_total.append(a)
                
                list_total.append(',')
            list_total.pop(-1)
            tu=" ".join(list_total)





            with open(self.filename,'r') as data:
                next(data)
                data_csv= csv.reader(data,delimiter=',')
                for values in data_csv:
                    dtype_list=[]
                    for c in column_list:
                        a=str(df[c].dtype)
                        dtype_list.append(a)
                
                    values=values[1:]
                
                    final_values_list=[]
                    for j in range(len(dtype_list)):
                
                        data_type=dtype_list[j]
                
                        value=values[j]
                
                    
                        if data_type  in ['float8','float16','float32','float64']:
                            a=float(value)
                            final_values_list.append(a)
                        
                        
                    
                        if data_type  in ['int8','int16','int32','int64']:
                            a=int(value)
                            final_values_list.append(a)
                    
                    
                    
                    
                    
                    
                
                    final_values_list=tuple(final_values_list)
                    aa=f"INSERT INTO train_data.{self.dbname}({tu}) values{final_values_list}"
                    print(aa)
                    self.session.execute(aa)
            self.log_writer.log(self.file_object,'Values Inserted ')
                

            print("Values inserted")
        except:
            self.log_writer.log(self.file_object,'Error To Insert Values')
    # def Insert_Values(self,session,filename):
    #     self.session=session
        
    #     self.filename=filename
    #     df=pd.read_csv(self.filename)
    #     try:
    #         df.drop(columns=['Unnamed: 0.1'],inplace=True)
    #     except:
    #         pass
    #     column_list=df.columns
    #     list_total=[]
    #     for i in range(len(column_list)):
    #         a=column_list[i]
    #         a=a.replace(" ","").replace(":","")
    
    
    #         # b=dtype_list[i]
    #         list_total.append(a)
    #         # if b  in ['float8','float16','float32','float64']:
    #         #     c='float'
    #         #     list_total.append(c)
    #         # if b  in ['int8','int16','int32','int64']:
    #         #     c='int'
    #         #     list_total.append(c)
        
    
    
    
    #         # if a=="Unnamed0":
    #         #     list_total.append("PRIMARY KEY")
    #         list_total.append(',')
    #     list_total.pop(-1)
    #     tu=" ".join(list_total)





    #     # col=[]
    #     # for i in df.columns:
    #     #     col.append(i)
    #     # tu=",".join(col)
    #     with open(self.filename,'r') as data:
    #         next(data)
    #         data_csv= csv.reader(data,delimiter=',')
    #         for i in data_csv:
    #             values=tuple(i)
    #             values=values.pop(1)
    #             aa=f"INSERT INTO train_data.train_test_data({tu}) values{values}"
    #             self.session.execute(aa)

    #     print("Values inserted")
        
        

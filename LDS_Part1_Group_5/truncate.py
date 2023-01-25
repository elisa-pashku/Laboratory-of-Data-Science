import csv
import pyodbc
import tqdm as tq

#Open the connection of database 'Group_5_DB' and create the cursor
server = 'tcp:lds.di.unipi.it'
database = 'Group_5_DB'
username = 'Group_5'
password = 'CDNA8KYR'
connectionString = 'DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()
cursor.execute('''
                
                truncate table Users;
                truncate table Answers;
                truncate table Organizations;
                truncate table Subjects;
                truncate table Dates;
                truncate table Geography;


               ''')



cnxn.commit()

# Close cursor
cursor.close()

# Close connection
cnxn.close()
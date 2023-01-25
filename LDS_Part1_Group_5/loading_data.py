import csv
import pyodbc
import tqdm as tq
import time

#Open the connection of database 'Group_5_DB' and create the cursor
server = 'tcp:lds.di.unipi.it'
database = 'Group_5_DB'
username = 'Group_5'
password = 'CDNA8KYR'
connectionString = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()

cursor.fast_executemany = True  #speeds up the process of inserting lines

# Reading the files resulting from Assignment 1
# 1 - Dates
dates = open("results/dates.csv", "r")
dates_lines = csv.reader(dates, delimiter=",")
# 2 - Geography
geography = open("results/geo.csv", "r")
geography_lines = csv.reader(geography, delimiter=",")
# 3 - Subjects
subject = open("results/subject.csv", "r")
subject_lines = csv.reader(subject, delimiter=",")
# 4 - Organizations
organization = open("results/organizations.csv", "r")
organization_lines = csv.reader(organization, delimiter=",")
# 5 - Users
users = open("results/users.csv", "r")
users_lines = csv.reader(users, delimiter=",")
# 6 - Answers
answers = open("results/answers.csv", "r")
answers_lines = csv.reader(answers, delimiter=",")

#run code inside the "try" block, if there is an error it goes into the "except" block instead of crashing
try:

    # Dictionary where key = name of table, value = reader
    datatoload = {
        "Dates": dates_lines,
        "Geography": geography_lines,
        "Subjects": subject_lines,
        "Organizations": organization_lines,
        "Users": users_lines,
        "Answers": answers_lines
    }

    is_header = True
    for table_name, lines in datatoload.items():
        sql = ""
        #create list to put all the data
        cache = []
        t0 = time.time()
        for row in tq.tqdm(lines, desc=table_name):
            #if row it's empty
            if not row:
                continue

            if is_header:
                count_param = 0

                # Query to read the header
                parametric_vals = ""
                data_st = ""
                for elem in row:
                    data_st += elem + ","
                    parametric_vals += "?,"
                    count_param+=1
                sql = f"INSERT INTO {username}.{table_name}({data_st[:-1]}) VALUES({parametric_vals[:-1]})"

                is_header = False
            else:

                # Inserting for specific tables
                if table_name == "Dates":
                    #saves it to put it in the cache list instead of executing immediately
                    dat = (int(row[0]),row[1],int(row[2]),int(row[3]),int(row[4]), int(row[5]))

                elif table_name == "Geography":
                    dat = (int(row[0]),row[1],row[2], row[3])

                elif table_name == "Subjects":
                    dat = (int(row[0]),row[1])

                elif table_name == "Organizations":
                    dat = (int(row[0]), int(row[1]), int(row[2]), float(row[3]))

                elif table_name == "Users":
                    dat= (int(row[0]), int(row[1]), int(row[2]), row[3])

                elif table_name == "Answers":
                    dat = (int(row[0]),int(row[1]),int(row[2]),int(row[3]),int(row[4]), int(row[5]), int(row[6]), int(row[7]), row[8],float(row[9]))

                else:
                    raise NameError(f"Unknown Table Name: {table_name}")

                cache.append(dat)
        #here you execute everything in one go
        cursor.executemany(sql, cache)
        cnxn.commit()
        print(f"Loaded - Table{table_name} in {time.time() - t0} [s]")
        print("********************************************")
        is_header = True

except Exception as e:
    #print error if there is
    print(e)

finally:

#Close files and the conncetion to the sql server, if it's in the final block it will always run even if there's an error in the try block
    dates.close()
    geography.close()
    subject.close()
    organization.close()
    users.close()
    answers.close()

    # Close cursor
    cursor.close()

    # Close connection
    cnxn.close()
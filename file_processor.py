# Create .exe by running 'pyinstaller --onefile file_processor.py'
# pyinstaller "CattleLog File Processor.py"

import pandas as pd
import tkinter as tk
from tkinter import filedialog
import datetime
import os
from update_database import updateDatabase

date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
root = tk.Tk()
root.withdraw()
pd.options.mode.chained_assignment = None

# Get files
# print("\n   Choose File 1 - This is Report 1 with columns [Index, DaysSBrd,  DaysTilDue, ...]: ")
# file_path1 = filedialog.askopenfilename()
# print("    " + file_path1 + "\n")
# print("   Choose File 2 - This is Report 2 with columns [Index, DamDHI_ID,  1stPrvBrHt, ...]: ")
# file_path2 = filedialog.askopenfilename()
# print("    " + file_path2 + "\n")
# print("   Choose File 3 - This is Report 3 with columns [Index, BrthDate, AllHlthEvCur]: ")
# file_path3 = filedialog.askopenfilename()
# print("    " + file_path3 + "\n")
# print("   Choose File 4 - This is the Treatments Excel file with columns [Number, Date,  PinkEye, ...]: ")
# file_path4 = filedialog.askopenfilename()
# print("    " + file_path4 + "\n")


# Files for debugging
file_path1 = "C:\\Users\\Camoen\\Documents\\a UF Online\\CIS 4914\\App Data\\Camoen Project 1.csv"
file_path2 = "C:\\Users\\Camoen\\Documents\\a UF Online\\CIS 4914\\App Data\\Camoen Project 2.csv"
file_path3 = "C:\\Users\\Camoen\\Documents\\a UF Online\\CIS 4914\\App Data\\Camoen Project 3.csv"
file_path4 = "C:\\Users\\Camoen\\Documents\\a UF Online\\CIS 4914\\App Data\\Camoen Project 4 New - With Dates.xls"

# file_path1 = "C:\\Users\\Camoen\\Documents\\a UF Online\\CIS 4914\\App Data\\Camoen Project 1 - Test Part 1.csv"
# file_path2 = "C:\\Users\\Camoen\\Documents\\a UF Online\\CIS 4914\\App Data\\Camoen Project 2 - Test Part 1.csv"
# file_path3 = "C:\\Users\\Camoen\\Documents\\a UF Online\\CIS 4914\\App Data\\Camoen Project 3 - Test Part 1.csv"
# file_path4 = "C:\\Users\\Camoen\\Documents\\a UF Online\\CIS 4914\\App Data\\Camoen Project 4 - Test Part 1.xls"

# file_path1 = "C:\\Users\\Camoen\\Documents\\a UF Online\\CIS 4914\\App Data\\Camoen Project 1 - Test Part 2.csv"
# file_path2 = "C:\\Users\\Camoen\\Documents\\a UF Online\\CIS 4914\\App Data\\Camoen Project 2 - Test Part 2.csv"
# file_path3 = "C:\\Users\\Camoen\\Documents\\a UF Online\\CIS 4914\\App Data\\Camoen Project 3 - Test Part 2.csv"
# file_path4 = "C:\\Users\\Camoen\\Documents\\a UF Online\\CIS 4914\\App Data\\Camoen Project 4 - Test Part 2.xls"



# Check that no duplicate files were entered accidentally
if (file_path1 == file_path2 or
    file_path1 == file_path3 or
    file_path1 == file_path4 or
    file_path2 == file_path3 or
    file_path2 == file_path4 or
    file_path3 == file_path4 or
    file_path1 == "" or
    file_path2 == "" or
    file_path3 == "" or
    file_path4 == ""):
    input("   Error in file selection. Each file must exist and be unique. Press Enter to quit.")
    exit()

# Create 'Output' folder if it doesn't exist
out_directory = os.path.split(file_path1)[0] + "/Output/"
if not os.path.exists(out_directory):  # Create directory if it doesn't exist
    print("   Created \"Output\" folder for merged file outputs.\n")
    os.makedirs(out_directory)

try:
    # Merge files 1, 2, and the "Sold" sheet from file 4
    file1 = pd.read_csv(file_path1)
    file2 = pd.read_csv(file_path2)
    file4_sold = pd.read_excel(file_path4, sheet_name=1, skiprows=[1])
    file4_sold.rename(columns={"Index #": "Index", "Date": "DateLeft",
                               "Brthdate": "BrthDate"}, inplace=True)
    merged = file1.merge(file2, on=['Index','BrthDate'], how='outer')
    try:
        merged['BrthDate'] = pd.to_datetime(merged['BrthDate'], format='%m-%d-%y')
    except:
        merged['BrthDate'] = pd.to_datetime(merged['BrthDate'], format='%m/%d/%Y')
    merged2 = pd.merge(merged, file4_sold, on=['Index', 'BrthDate'], how='outer')
    output_file = out_directory + "output_" + date + ".csv"
    print("   Output of merged files 1, 2, 4 (sheet 2): " + output_file + "\n")
    merged2.to_csv(output_file, index=False)

    # Repeat index numbers and birthdates in files 3 and 4
    # TODO: File 3
    file3 = pd.read_csv(file_path3)
    indexNum = ""
    birthDate = ""
    for i in range(len(file3)):
        if pd.notnull(file3['Index'].iloc[i]):
            indexNum = file3['Index'].iloc[i]
            birthDate = file3['BrthDate'].iloc[i]
        else:
            file3['Index'].iloc[i] = indexNum
            file3['BrthDate'].iloc[i] = birthDate
    output_health = out_directory + "health_" + date + ".csv"
    print("   Output of file 3: " + output_health + "\n")
    file3['BrthDate'] = pd.to_datetime(file3["BrthDate"]) 
    file3.to_csv(output_health, index=False)

    file4 = pd.read_excel(file_path4, skiprows=[1])
    indexNum = ""
    birthDate = ""
    for i in range(len(file4)):
        if pd.notnull(file4['Number'].iloc[i]):
            indexNum = file4['Number'].iloc[i]
            birthDate = file4['Brthdate'].iloc[i]
        else:
            file4['Number'].iloc[i] = indexNum
            file4['Brthdate'].iloc[i] = birthDate
    file4.rename(columns={"Number": "Index", "Brthdate": "BrthDate",
                          "Symptom / Treatment" : "Details"}, inplace=True)
    # output_treatments = out_directory + "treatment_" + date + ".csv"
    # print("   Output of file 4: " + output_treatments + "\n")
    # file4.to_csv(output_treatments, index=False)

    # Get data for User Defined Fields
    userdef = pd.read_excel(file_path4, sheet_name=2, skiprows=[1])

except:
    input("   One or more input files are invalid. Press Enter to exit.\n")
    exit()


# Export all data to database
# output_file
# output_health
# output_treatments

print("updating table using pandas dataframes: ")
# Pandas dataframes
cattle = merged2
health = file3
treatment = file4

# treatment['Index'] = treatment['Index'].astype('int64')

# treatment['BrthDate'] = pd.to_datetime(treatment["BrthDate"]) 
# print(treatment.dtypes)
# health['BrthDate'] = pd.to_datetime(health["BrthDate"]) 
# print(health.dtypes)
# treatment['OTHER'] = treatment['OTHER'].astype('str')
# print(treatment['OTHER'].dtype)

# for i in range(len(health)):
#     if (i > 1 and
#         health['Index'].iloc[i] == health['Index'].iloc[i-1] and
#         health['BrthDate'].iloc[i] == health['BrthDate'].iloc[i-1] and
#         health['AllHlthEvCur'].iloc[i] == health['AllHlthEvCur'].iloc[i-1]):
#         print(i,health.iloc[i])


updateDatabase(cattle, health, treatment, userdef)

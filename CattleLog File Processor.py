import datetime
import os
import pandas as pd
import tkinter as tk
from shutil import copyfile
from tkinter import filedialog
from update_database import updateDatabase
from upload_database import uploadDatabase

currentTime = datetime.datetime.now()
date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
root = tk.Tk()
root.withdraw()
pd.options.mode.chained_assignment = None

# Add a year to a date and check that the date is valid -- Thanks Gareth Rees!
def add_year(d):
    try:
        return d.replace(year = d.year + 1)
    except ValueError:
        return d + (date(d.year + 1, 1, 1) - date(d.year, 1, 1))

# Add 21 days to a next expected heat date
def add_21_days(d):
    return d + datetime.timedelta(days=21)

# Set a year for dates with no year (NextExpHeat and DateDue)
def set_date_year(is_heat_date, date_no_year):
    dateWithYear = date_no_year + "-" + datetime.datetime.now().strftime("%Y") + " 23:59:59"
    try:
        dateToCheck = datetime.datetime.strptime(dateWithYear, '%d-%b-%Y %H:%M:%S')
    except ValueError:
        dateToCheck = datetime.datetime.strptime(dateWithYear, '%m-%d-%Y %H:%M:%S')
    # Dates are always in the future, so check that the year is correct relative to the current time.
    if dateToCheck < currentTime:
        if (is_heat_date):
            # If date to check is within the past 4 weeks, this is a late upload
            if (dateToCheck > currentTime - datetime.timedelta(weeks=4)):
                # Add 3 weeks until heat date is > current date
                while dateToCheck < currentTime:
                    dateToCheck = add_21_days(dateToCheck)
            # If the date to check is before the past 4 weeks, this should be a date that occurs next year
            else:
                dateToCheck = add_year(dateToCheck)
        else:
            # For due dates, add year, but only if the due date isn't in the previous month and a half
            # Assumption is that calves generally won't be 6 weeks overdue
            if (dateToCheck < currentTime - datetime.timedelta(weeks=6)):
                dateToCheck = add_year(dateToCheck)
    fixedDate = dateToCheck.strftime("%Y-%m-%d")
    return fixedDate



# Program Messages
print("\n************************************* CattleLog File Processor *************************************")
print("\n   INSTRUCTIONS:")
print("     1. If any of your input files are currently open, close them before continuing.")
print("     2. Enter files in the correct order, as prompted (Treatments.xls, Report 1, Report 2, Report 3).")
print("     3. If any errors are encountered, they will be printed to this console.")
print("     4. Fix all errors and rerun this program to upload new data to the database.")
print("         - A backup of your Treatments.xls file will be saved in the \"Backup\" folder.")
print("         - A backup of the previous database state will be saved in the \"Database_Backup\" folder.\n")
print("****************************************************************************************************\n")

# Get first two files
print("   Choose the Treatments.xls Excel file with columns [Number, Date,  PinkEye, ...]: ")
treatments_path = filedialog.askopenfilename()
print("   Selected Treatments File: " + os.path.split(treatments_path)[1] + "\n")

print("   Choose Report 1 with columns [Index, DaysSBrd,  DaysTilDue, ...]: ")
report1_path = filedialog.askopenfilename()
print("   Selected Report 1 File: " + os.path.split(report1_path)[1] + "\n\n")



# Check that no duplicate files were entered accidentally
if (report1_path == treatments_path or report1_path == "" or treatments_path == ""):
    input("******** Error in file selection. Each file must exist and be unique. Press Enter to exit. ********")
    exit()

# Backup the unmodified treatment file
directory = os.path.split(treatments_path)[0] + "/Backup/"
basename = os.path.split(treatments_path)[1]
backup = directory + basename[:-4] + "_" + date + treatments_path[-4:]
if not os.path.exists(directory):  # Create directory if it doesn't exist
    print("   Created \"Backup\" folder for Treatment file backups.\n")
    os.makedirs(directory)
copyfile(treatments_path, backup)

# Output more info about how the Treatments.xls file is processed
print("   Dates will automatically be added to the \"Birthdate\" column of the \"Treatments\" sheet")
print("   in your Treatments.xls file. This program will not automatically add birthdates to the")
print("   \"Sold_since_01SE2019\" sheet.\n")

# Try to read files, return error if either is invalid
try:
    # Read the first file
    file1 = pd.read_csv(report1_path, usecols=['Index','BrthDate'])
    birth_dict = {}

    # If there are duplicate index numbers, keep the first combination
    # Animals with duplicate index numbers must be placed in Treatments file chronologically based on birth date
    for i in range(len(file1)):
        if file1['Index'].iloc[i] not in birth_dict:
            birth_dict[file1['Index'].iloc[i]] = file1['BrthDate'].iloc[i]

except:
    input("****** Input file for Report 1 is invalid. Retry with a different file. Press Enter to exit. ******\n")
    exit()


try:
    # Put birthdates in second file   
    file2 = pd.ExcelFile(treatments_path)
    treatments = pd.read_excel(file2, 0, skiprows=[1])
    number_seen = set() # Set of numbers that have already been seen
    error_count = 0
except:
    input("***** Input file for Treatments is invalid. Retry with a different file. Press Enter to exit. *****\n")
    exit()


# Iterate over all rows in Treatments file except Header and Spacer, outputs errors in real time
for i in range(len(treatments)):
    if pd.notnull(treatments['Number'].iloc[i]):
        indexNum = treatments['Number'].iloc[i]

        # If the cell's value hasn't been seen yet
        if indexNum not in number_seen:
            number_seen.add(indexNum)
            if indexNum in birth_dict:
                treatments['Birthdate'].iloc[i] = birth_dict[indexNum]
            else:
                error_count += 1
                if error_count == 1:
                    print("   Error(s) Found:")
                print("  ",indexNum,"has no corresponding birthdate.")

        else:
            # Only trigger an error if a duplicate tagnumber has no associated birthdate
            if pd.isnull(treatments['Birthdate'].iloc[i]):
                error_count += 1
                if error_count == 1:
                        print("   Error(s) Found:")
                print("  ",indexNum,"is a duplicate number.  Add birthdate manually.")

# Output number of errors, if any.
if error_count > 0:
    print("\n   Number of errors found: ",error_count,"\n")
    input("************* Please fix all errors and run the program again. Press Enter to exit. ***************")
    exit()
else:
    print("***************************** Treatments.xls parsed without errors. *******************************\n")


# Get remaining files
print("   Choose Report 2 with columns [Index, DamDHI_ID,  1stPrvBrHt, ...]: ")
report2_path = filedialog.askopenfilename()
print("   Selected Report 2 File: " + os.path.split(report2_path)[1] + "\n")

print("   Choose Report 3 with columns [Index, BrthDate, AllHlthEvCur]: ")
report3_path = filedialog.askopenfilename()
print("   Selected Report 3 File: " + os.path.split(report3_path)[1] + "\n")

# Check that no duplicate files were entered accidentally
if (report1_path == report2_path or
    report1_path == report3_path or
    report1_path == treatments_path or
    report2_path == report3_path or
    report2_path == treatments_path or
    report3_path == treatments_path or
    report1_path == "" or
    report2_path == "" or
    report3_path == "" or
    treatments_path == ""):
    input("******** Error in file selection. Each file must exist and be unique. Press Enter to exit. ********")
    exit()

# Create 'Output' folder if it doesn't exist
out_directory = os.path.split(report1_path)[0] + "/Output/"
if not os.path.exists(out_directory):  # Create directory if it doesn't exist
    print("\n   Created \"Output\" folder for processed file outputs.\n")
    os.makedirs(out_directory)

# Try to process all files.  Return an error if any files are invalid.
try:
    # Merge files 1, 2, and the "Sold" sheet from file 4
    report1 = pd.read_csv(report1_path)
    report2 = pd.read_csv(report2_path)

    report_sold = pd.read_excel(file2, 1, skiprows=[1])
    report_sold.rename(columns={"Index #": "Index", "Date": "DateLeft",
                               "Brthdate": "BrthDate"}, inplace=True)
    merged = report1.merge(report2, on=['Index','BrthDate'], how='outer')
    try:
        merged['BrthDate'] = pd.to_datetime(merged['BrthDate'], format='%m-%d-%y')
    except:
        merged['BrthDate'] = pd.to_datetime(merged['BrthDate'], format='%m/%d/%Y')
    cattle_data = pd.merge(merged, report_sold, on=['Index', 'BrthDate'], how='outer')


    # Add years to NextExpHeat and DateDue
    for i in range(len(cattle_data)):
        if pd.notnull(cattle_data['NextExpHeat'].iloc[i]):
            cattle_data['NextExpHeat'].iloc[i] = set_date_year(True, cattle_data['NextExpHeat'].iloc[i])
        if pd.notnull(cattle_data['DateDue'].iloc[i]):
            cattle_data['DateDue'].iloc[i] = set_date_year(False, cattle_data['DateDue'].iloc[i])
    output_file = out_directory + "output_" + date + ".csv"
    print("   Output of Reports 1, 2, and Sheet 2 of Treatments.xls: " + os.path.split(output_file)[1] + "\n")
    cattle_data.to_csv(output_file, index=False)

    # Repeat index numbers and birthdates in files 3 and 4
    # Also create health record index numbers for composite primary key in treatments
    health = pd.read_csv(report3_path)
    indexNum = ""
    birthDate = ""
    for i in range(len(health)):
        if pd.notnull(health['Index'].iloc[i]):
            indexNum = health['Index'].iloc[i]
            birthDate = health['BrthDate'].iloc[i]
        else:
            health['Index'].iloc[i] = indexNum
            health['BrthDate'].iloc[i] = birthDate
    output_health = out_directory + "health_" + date + ".csv"
    print("   Output of Report 3 processing: " + os.path.split(output_health)[1] + "\n")
    health['BrthDate'] = pd.to_datetime(health["BrthDate"]) 
    health.to_csv(output_health, index=False)

    # treatments = pd.read_excel(treatments_path, skiprows=[1])
    indexNum = ""
    birthDate = ""
    recordNums = []
    recordNum = 0
    for i in range(len(treatments)):
        recordNum += 1
        if pd.notnull(treatments['Number'].iloc[i]):
            indexNum = treatments['Number'].iloc[i]
            birthDate = treatments['Birthdate'].iloc[i]
            recordNum = 1
        else:
            treatments['Number'].iloc[i] = indexNum
            treatments['Birthdate'].iloc[i] = birthDate
        recordNums.append(recordNum)
    treatments['RecordNumber'] = recordNums
    treatments.rename(columns={"Number": "Index", "Birthdate": "BrthDate",
                          "Symptom / Treatment" : "Details"}, inplace=True)
    output_treatments = out_directory + "treatment_" + date + ".csv"
    print("   Output of Treatments.xls processing: " + os.path.split(output_treatments)[1] + "\n")
    treatments['BrthDate'] = pd.to_datetime(treatments["BrthDate"])
    treatments['Date'] = pd.to_datetime(treatments["Date"])
    treatments.to_csv(output_treatments, index=False)

    # Get data for User Defined Fields
    userdef = pd.read_excel(file2, 2, skiprows=[1])

except:
    input("****** One or more input files are invalid. Retry with different files. Press Enter to exit. ******\n")
    exit()


# Use pandas dataframes to update the database
updateDatabase(cattle_data, health, treatments, userdef)
uploadDatabase()
input("******************** Program finished running without errors.  Press Enter to exit. *******************\n")
exit()

# TODO: Add .gitignore for credentials
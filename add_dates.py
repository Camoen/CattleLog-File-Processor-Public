# Create .exe by running 'pyinstaller --onefile file_processor.py'
import pandas as pd
import datetime
import xlwings as xw
import os
from shutil import copyfile
import tkinter as tk
from tkinter import filedialog


date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
root = tk.Tk()
root.withdraw()

# Program Messages
print("\n************* This program will automatically add dates to your Treatments Excel file. *************")
print("\n   If any of your input files are currently open, close them before continuing.\n")
print("   Dates will only be automatically added to the \"BrthDate\" column on the \"Treatments\" sheet.")
print("   This program will not automatically add birthdates to the \"Sold_since_01SE2019\" sheet.\n")

print("   Errors will be printed to this console. Fix all errors and rerun this program before uploading")
print("   the file to the database. A backup of your treatments file is saved in the \"Backup\" folder.\n")
print("****************************************************************************************************")

# Get files
print("\n   Choose File 1 - This is Report 1 with columns [Index, DaysSBrd,  DaysTilDue, ...]: ")
file_path1 = filedialog.askopenfilename()
print("   Selected File 1: " + os.path.split(file_path1)[1] + "\n")
print("   Choose File 2 - This is the Treatments Excel file with columns [Number, Date,  PinkEye, ...]: ")
file_path2 = filedialog.askopenfilename()
print("   Selected File 2: " + os.path.split(file_path2)[1] + "\n\n")

# Check that no duplicate files were entered accidentally
if (file_path1 == file_path2 or file_path1 == "" or file_path2 == ""):
    input("   Error in file selection. Each file must exist and be unique. Press Enter to quit.")
    exit()

# Backup the unmodified treatment file
directory = os.path.split(file_path2)[0] + "/Backup/"
basename = os.path.split(file_path2)[1]
backup = directory + basename[:-4] + "_" + date + file_path2[-4:]
if not os.path.exists(directory):  # Create directory if it doesn't exist
    print("   Created \"Backup\" folder for Treatment file backups.\n")
    os.makedirs(directory)
copyfile(file_path2, backup)

# Try to read first file
file1 = pd.read_csv(file_path1, usecols=['Index','BrthDate'])
birth_dict = dict(zip(file1.Index, file1.BrthDate))

# Put birthdates in second file
file2size = len(pd.read_excel(file_path2))
file2 = xw.Book(file_path2)
Trt_sheet = file2.sheets['Treatments']
number_seen = set() # Set of numbers that have already been seen
error_count = 0

# Iterate over all rows except Header and Spacer
for i in range(2, file2size+2):
    # Get cell val at index 1 (first cell in row)
    cellval = Trt_sheet.cells(i,1).value

    # If the cell has a value
    if (cellval != None):
        # If the cell's value hasn't been seen yet
        if cellval not in number_seen:
            number_seen.add(cellval)
            if cellval in birth_dict:
                Trt_sheet.cells(i,12).value = birth_dict[cellval]
                #print(Trt_sheet.cells(i,1).value)
            else:
                error_count += 1
                if error_count == 1:
                    print("   Error(s) Found:")
                print("  ",cellval,"has no corresponding birthdate.")

        else:
            error_count += 1
            if error_count == 1:
                    print("   Error(s) Found:")
            print("  ",cellval,"is a duplicate number.  Add birthdate manually.")

# Save changes in treatment file
if error_count > 0:
    print("\n   Number of errors found: ",error_count,"\n")
    print("************************ Please fix all errors and run the program again. *************************")
    print("************************************ Program finished running. ************************************\n")
else:
    print("**************************** Program finished running without errors. *****************************\n")

file2.save(file_path2)
# file2.close()








# Write to second file
# file2 = pd.read_excel(file_path2, skiprows=[1], dtype={'Date': str, 'BrthDate': str})
# for i in range(len(file2)):
#     key = file2['Number'].values[i]
#     print(key)
#     if key in birth_dict:
#         file2['BrthDate'].values[i] = birth_dict[key]

# file2.to_excel('students2.xls', index=False)

# try:
#     file1 = pd.read_csv(file_path1, usecols=['Index','BrthDate'])
#     birth_dict = dict(zip(file1.Index, file1.BrthDate))

#     # Write to second file
#     file2 = pd.read_excel(file_path2, skiprows=[1])
#     for i in range(len(file2)):
#         if df['Index'] in birth_dict:
#             df['BrthDate'].values[i] = birth_dict[df['Index']]
    
#     print(file2)
# except:
#     input("Invalid input files. Press Enter to exit.\n")
#     exit()




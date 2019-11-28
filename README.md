# CattleLog File Processor <img src="https://user-images.githubusercontent.com/16565961/69681054-d1caba00-107a-11ea-927b-71256a011751.jpg" alt="CattleLog - Main Screen" width="10%" height="" align="left">
<br>

This repository holds the complete code for the CattleLog File Processor, as well as four sample input files.  Note that all credentials and private cattle records have been redacted.  The primary goal of CattleLog File Processor (CFP) is to provide the VanWagner Family Farm's record-keeper with an efficient, user-friendly method of updating and maintaining CattleLog's backend database.  CFP achieves this goal by accepting four input files, automatically performing any necessary data pre-processing, creating or updating an SQLite database, and uploading the resulting database to DropBox, where it can be accessed by [CattleLog](https://github.com/Camoen/CattleLog) (the mobile application).

## Table of Contents
* [CattleLog File Processor Video Demonstration](#cattlelog-file-processor-video-demonstration)
* [CattleLog (Mobile Application)](#cattlelog-mobile-application)
* [CattleLog File Processor Features](#cattlelog-file-processor-features)
    * [Input File Validation](#input-file-validation)
    * [Backup Functionality](#backup-functionality)
    * [Data Preprocessing](#data-preprocessing)
        * [Treatments File Birthdate Association](#treatments-file-birthdate-association)
        * [Creation of DataFrames](#creation-of-dataframes)
        * [Date Modifications](#date-modifications)
    * [CattleLog Database Modification](#cattlelog-database-modification)
        * [CattleLog Database Schema](#cattlelog-database-schema)
        * [CattleLog Database Creation](#cattlelog-database-creation)
        * [CattleLog Database Updates](#cattlelog-database-updates)
    * [CattleLog Database Upload](#cattlelog-database-upload)

## CattleLog File Processor Video Demonstration
A video demonstration of the CattleLog File Processor is available on YouTube: https://youtu.be/zOrB2FUL0ys

## CattleLog (Mobile Application)
Beyond the development of this Python executable, an Android app, named CattleLog, was created to display data from the resulting database. The primary goals of [CattleLog](https://github.com/Camoen/CattleLog) are to (1) provide employees of the VanWagner Family Farm with an efficient method of cattle record lookup via an intuitive user interface and (2) display requested cattle records in an aesthetically pleasing, organized manner.  Its source code, readme, and a video demonstration of its functionality can be found at https://github.com/Camoen/CattleLog.

## CattleLog File Processor Features
This section is currently a WIP.
### Input File Validation
Duplicate files/nonexistent files
### Backup Functionality
Treatments file, prev databases
### Data Preprocessing
#### Treatments File Birthdate Association
##### Error Checking
#### Creation of DataFrames
##### Cattle DataFrame
##### Health DataFrame
##### Treatments DataFrame
##### User-Defined Field DataFrame
#### Date Modifications
### CattleLog Database Modification
#### CattleLog Database Schema
A full description of CattleLog's database design is provided in section 2.1.1 of the CattleLog documentation, located [here]().
<p align="center"><img src="https://user-images.githubusercontent.com/16565961/69830800-74f30f00-11f4-11ea-82a5-4ffb6d248f87.png" alt="E-R Diagram" width="75%" height=""><br>CattleLog Database E-R Diagram</p>

#### CattleLog Database Creation
If no local `cattlelog_database.db` file already exists, a new database file is created (if such a file already exists, a backup of the file is stored, and the program skips to the [update](#cattlelog-database-updates) functionality).  The complete code for the database's initial creation is located at https://github.com/Camoen/CattleLog-File-Processor-Public/blob/master/create_database.py.

As shown in the E-R diagram above, the `health` (HealthRecords) and `treatment` (Treatments) table are reliant on `TagNumber` and `BirthDate` from the `cattle` table as foreign keys.  The `ON DELETE CASCADE` clause is included to ensure that health records and treatments are deleted if their associated `cattle` entity is deleted.

#### CattleLog Database Updates
Once a database file has been located or created, CFP uses the [generated DataFrames](#creation-of-dataframes) to update the database file.  The complete code for the update functionality is located at https://github.com/Camoen/CattleLog-File-Processor-Public/blob/master/update_database.py.

A majority of the update logic consists of `INSERT OR REPLACE` queries for the `cattle`, `health`, `treatment`, and `userFields` tables.

##### Mistagged Animal Functionality
Since the database is completely abstracted away from the record-keeper, it became necessary to add a way of "resetting" (completely removing) erroneous records for a given animal.  In the "Treatments.xls" input file, the second spreadshset includes data about animals that have left the farm.  There are four fields: Index # (`TagNumber`), Brthdate (`BirthDate`), Date (`DateLeft`), and Reason.  The latter of these two fields are used to indicate the date an animal left the herd and the reason for leaving.  If the "Reason" field is set to the string "Mistagged", all records for the associated animal (as indicated by `TagNumber` and `BirthDate`) are completely removed from the database.  This functionality was first added when a newborn calf was given an incorrect `TagNumber`, hence the use of "Mistagged" as the keyword.

##### Removal of Unnecessary Records
Some of the cattle that are raised on the VanWagner Family Farm belong to another farm.  Each of these animals has a `BarnName` attribute that starts with the letter `R`.  These records (and only these records) can be removed from the database when the specific animals have left the farm.  Other animal records should always be maintained, even if the animal has left the farm.

When any animal leaves the farm, the record-keeper sets their status to "Left Herd" in PCDART, so the output .csv files no longer include data about these animals.  Furthermore, the record-keeper removes this animal from the "Treatments.xls" file.  Therefore, no data about an animal that has left the farm will appear in the generated dataframes, which makes it relatively simple to programmatically identify "missing" animals (animals that have left).  Remember, however, that most animal records must be maintained in perpetuity; only animals with a `BarnName` that begins with an `R` should be purged from the database.  

To implement this functionality, during each database update, the program creates a table called `keep_matches` to record all animals that still exist in the four input files.  Cattle records are purged from the database if (1) the animal does not appear in the `keep_matches` table AND (2) the animal has a `BarnName` starting with `R`.  This leaves all other cattle records intact, regardless of whether or not they have left the farm.  The following bit of SQL implements this logic:

```
c.execute("""
     DELETE FROM cattle 
     WHERE NOT EXISTS
          (SELECT * FROM keep_matches km
          WHERE (cattle.TagNumber =  km.TagNumber AND cattle.BirthDate =  km.BirthDate))
     AND cattle.BarnName LIKE 'R%'
""")
```




### CattleLog Database Upload

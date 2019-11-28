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
##### User-Defined Field Dataframe
#### Date Modifications
## CattleLog Database Modification
## CattleLog Database Upload

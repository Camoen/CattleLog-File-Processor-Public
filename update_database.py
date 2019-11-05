import sqlite3
import datetime
import os
import pandas as pd
import numpy as np
from pathlib import Path
from shutil import copyfile
from create_database import createDatabase


def checkNullDate(dateAttribute):
	# Check for null date values to prevent crash on import
	if pd.isnull(dateAttribute):
		dateAttribute = ""
	else:
		dateAttribute = dateAttribute.strftime("%m/%d/%Y")
	return dateAttribute


def updateDatabase(cattle, health, treatment, userdef):
	sqlite3.register_adapter(np.int64, int)
	date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

	# If file exists, backup the database. Otherwise, create the database.
	current_dir = os.path.dirname(os.path.realpath(__file__))
	db_filename = 'cattlelog_database.db'
	db_filepath = os.path.join(current_dir, db_filename)
	if Path(db_filepath).is_file():
		# Backup Database
		backup_dir = current_dir + "/Database_Backup/"
		backup_filepath = backup_dir + "cattlelog_database_backup_" + date + '.db'

		# If Database_Backup Folder doesn't exist, create it
		if not os.path.exists(backup_dir):
		    print("   Created \"Database_Backup\" folder for database file backups.\n")
		    os.makedirs(backup_dir)

		copyfile(db_filepath, backup_filepath)

	else:
		createDatabase()
	
	# Update the existing database
	conn = sqlite3.connect('cattlelog_database.db')
	c = conn.cursor()
	c.execute("PRAGMA foreign_keys=ON")
	
	# Update cattle Table
	# Create temp table of new data to determine which existing records should be removed
	c.execute("""CREATE TABLE keep_matches (
				TagNumber INTEGER,
				BirthDate TEXT,
				PRIMARY KEY (TagNumber, BirthDate)
				)""")

	for i in range(len(cattle)):
		TagNumber 				= cattle['Index'].iloc[i]
		BirthDate 				= cattle['BrthDate'].iloc[i]
		DaysSinceBredHeat 		= cattle['DaysSBrd'].iloc[i]
		DaysTilDue 				= cattle['DaysTilDue'].iloc[i]
		GroupNumber 			= cattle['Grp'].iloc[i]
		TempGroupNumber 		= cattle['TmpGrp'].iloc[i]
		ReproCode 				= cattle['Repr'].iloc[i]
		TimesBred 				= cattle['TmsBrd'].iloc[i]
		Breed 					= cattle['Brd'].iloc[i]
		UsrDef1 				= cattle['UsrDef1'].iloc[i]
		UsrDef2 				= cattle['UsrDef2'].iloc[i]
		UsrDef3 				= cattle['UsrDef3'].iloc[i]
		UsrDef4 				= cattle['UsrDef4'].iloc[i]
		UsrDef5 				= cattle['UsrDef5'].iloc[i]
		UsrDef6 				= cattle['UsrDef6'].iloc[i]
		UsrDef7 				= cattle['UsrDef7'].iloc[i]
		UsrDef8 				= cattle['UsrDef8'].iloc[i]
		UsrDef9 				= cattle['UsrDef9'].iloc[i]
		UsrDef10 				= cattle['UsrDef10'].iloc[i]
		DaysTilNextHeat 		= cattle['DaysTilNxtHt'].iloc[i]
		BarnName 				= cattle['BarnName'].iloc[i]
		DHIID 					= cattle['DHIID'].iloc[i]
		DamIndex 				= cattle['DamIndex'].iloc[i]
		DamName					= cattle['DamName'].iloc[i]
		SireNameCode 			= cattle['SireNmeCde'].iloc[i]
		TimesBredDate 			= cattle['TmsBrdDate'].iloc[i]	
		DateDue 				= cattle['DateDue'].iloc[i]
		ServiceSireNameCode 	= cattle['SrvSrNmeCde'].iloc[i]
		NextExpHeat 			= cattle['NextExpHeat'].iloc[i]
		AgeInMonthsAtCalving 	= cattle['AgeMons_Clv'].iloc[i]
		DonorDamID 				= cattle['DonorDamID'].iloc[i]
		FarmID 					= cattle['FarmID'].iloc[i]
		DamDHI_ID 				= cattle['DamDHI_ID'].iloc[i]
		PrevBredHeat1 			= cattle['1stPrvBrHt'].iloc[i]
		PrevBredHeat2 			= cattle['2ndPrvBrHt'].iloc[i]
		PrevBredHeat3 			= cattle['3rdPrvBrHt'].iloc[i]
		WeightBirth 			= cattle['WgtBrth'].iloc[i]
		WeightWean 				= cattle['WgtWean'].iloc[i]
		WeightBred 				= cattle['WgtBred'].iloc[i]
		WeightPuberty 			= cattle['WgtPubr'].iloc[i]
		WeightCalving			= cattle['WgtCalv'].iloc[i]
		DaysInCurGroup 			= cattle['DaysInCurGrp'].iloc[i]
		DateLeft 				= cattle['DateLeft'].iloc[i]
		Reason 					= cattle['Reason'].iloc[i]

		BirthDate = checkNullDate(BirthDate)
		DateLeft  = checkNullDate(DateLeft)			

		# If the animal has not left the herd, replace old data with new data
		c.execute("""SELECT * FROM cattle WHERE (TagNumber = ? AND BirthDate = ?)""",
				  (TagNumber, BirthDate))
		getRow = c.fetchone()
		# If no row exists for an animal, a row must be inserted
		# Also, update rows for animals that have not left the herd
		if getRow is None or pd.isnull(Reason):
			# Prevent mistagged animals from being re-entered into the database after a prior removal
			if (Reason != "Mistagged"):
				c.execute("""INSERT OR REPLACE INTO cattle (
							TagNumber, BirthDate, DaysSinceBredHeat, DaysTilDue,
							GroupNumber, TempGroupNumber, ReproCode, TimesBred,
							Breed, UsrDef1, UsrDef2, UsrDef3,
							UsrDef4, UsrDef5, UsrDef6, UsrDef7,
							UsrDef8, UsrDef9, UsrDef10, DaysTilNextHeat,
							BarnName, DHIID, DamIndex, DamName,
							SireNameCode, TimesBredDate, DateDue, ServiceSireNameCode,
							NextExpHeat, AgeInMonthsAtCalving, DonorDamID, FarmID,
							DamDHI_ID, PrevBredHeat1, PrevBredHeat2, PrevBredHeat3,
							WeightBirth, WeightWean, WeightBred, WeightPuberty,
							WeightCalving, DaysInCurGroup, DateLeft, Reason)
					 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
					 		 ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
					 		 ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
					 		 ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
							(TagNumber, BirthDate, DaysSinceBredHeat, DaysTilDue,
							GroupNumber, TempGroupNumber, ReproCode, TimesBred,
							Breed, UsrDef1, UsrDef2, UsrDef3,
							UsrDef4, UsrDef5, UsrDef6, UsrDef7,
							UsrDef8, UsrDef9, UsrDef10, DaysTilNextHeat,
							BarnName, DHIID, DamIndex, DamName,
							SireNameCode, TimesBredDate, DateDue, ServiceSireNameCode,
							NextExpHeat, AgeInMonthsAtCalving, DonorDamID, FarmID,
							DamDHI_ID, PrevBredHeat1, PrevBredHeat2, PrevBredHeat3,
							WeightBirth, WeightWean, WeightBred, WeightPuberty,
							WeightCalving, DaysInCurGroup, DateLeft, Reason))

		# If there is an existing row already AND reason is not NULL, update record instead of insert
		else:
			c.execute("""UPDATE cattle
						 SET DateLeft = ?,
						     Reason = ?
						 WHERE (TagNumber = ? AND
						        BirthDate = ?)""",
						 (DateLeft, Reason, TagNumber, BirthDate))

		# Remove records for mistagged animals
		c.execute("""SELECT Reason FROM cattle WHERE (TagNumber = ? AND BirthDate = ?)""",
				  (TagNumber, BirthDate))
		if c.fetchone() is not None and Reason == "Mistagged":
			print("   Record for",TagNumber, " born on", BirthDate," marked as 'Mistagged'. Deleting all data for this record." )
			c.execute("""DELETE FROM cattle WHERE (TagNumber = ? AND BirthDate = ?)""",
						(TagNumber, BirthDate))

		# Update the temp table
		c.execute("""INSERT OR REPLACE INTO keep_matches (
							TagNumber, BirthDate)
					 VALUES (?, ?)""",
							(TagNumber, BirthDate))


	# Use temp table to delete all Rucks heifers that don't appear in the updated files
	c.execute("""DELETE FROM cattle 
				 WHERE NOT EXISTS (
					SELECT * FROM keep_matches km
					WHERE (cattle.TagNumber =  km.TagNumber AND
						   cattle.BirthDate =  km.BirthDate))
					AND cattle.BarnName LIKE 'R%'""")

	# # Debug what I'm selecting
	# c.execute("""SELECT * FROM cattle
	# 			 WHERE NOT EXISTS (
	# 				SELECT * FROM keep_matches km
	# 				WHERE (cattle.TagNumber =  km.TagNumber AND
	# 					   cattle.BirthDate =  km.BirthDate))
	# 				AND cattle.BarnName LIKE 'R%'""")
	# print(c.fetchall())

	# Drop the temp table
	c.execute("""DROP TABLE keep_matches""")


	# Update health Table
	for i in range(len(health)):
		TagNumber 		= health['Index'].iloc[i]
		BirthDate 		= health['BrthDate'].iloc[i]
		HealthEvent 	= health['AllHlthEvCur'].iloc[i]
		
		# If the record is null, it cannot be added  to the database (primary key attributes are NOT NULL)
		if pd.isnull(HealthEvent):
			continue

		BirthDate = checkNullDate(BirthDate)

		c.execute("""INSERT OR REPLACE INTO health (
							TagNumber, BirthDate, HealthEvent)
					 VALUES (?, ?, ?)""",
							(TagNumber, BirthDate, HealthEvent))


	# Update treatment Table
	for i in range(len(treatment)):
		TagNumber 		= treatment['Index'].iloc[i]
		BirthDate 		= treatment['BrthDate'].iloc[i]
		RecordNumber    = treatment['RecordNumber'].iloc[i]
		EventDate 		= treatment['Date'].iloc[i]
		PinkEye 		= treatment['PinkEye'].iloc[i]
		EyeSide 		= treatment['Eye'].iloc[i]
		Respiratory 	= treatment['Resp.'].iloc[i]
		Scours 			= treatment['Scours'].iloc[i]
		Foot 			= treatment['Foot'].iloc[i]
		FootPosition 	= treatment['Position'].iloc[i]
		Mastitis 		= treatment['MASTiTiS'].iloc[i]
		Other 			= treatment['OTHER'].iloc[i]
		Details 		= treatment['Details'].iloc[i]

		BirthDate = checkNullDate(BirthDate)
		EventDate = checkNullDate(EventDate)							

		c.execute("""INSERT OR REPLACE INTO treatment (
							TagNumber, BirthDate, RecordNumber, EventDate, PinkEye,
					 		EyeSide, Respiratory, Scours, Foot,
							FootPosition, Mastitis, Other, Details)
					 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
							(TagNumber, BirthDate, RecordNumber, EventDate, PinkEye,
					 		EyeSide, Respiratory, Scours, Foot,
					 		FootPosition, Mastitis, Other, Details))

	# Update User Defined Fields Table
	for i in range(len(userdef)):
		FieldNumber		= userdef['UserDefNumber'].iloc[i]
		FieldTitle 		= userdef['UserDefTitle'].iloc[i]
		FieldDetails	= userdef['UserDefDescription'].iloc[i]							

		c.execute("""INSERT OR REPLACE INTO userFields (
							FieldNumber, FieldTitle, FieldDetails)
					 VALUES (?, ?, ?)""",
							(FieldNumber, FieldTitle, FieldDetails))
	
	conn.commit()
	conn.close()



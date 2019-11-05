import sqlite3


def createDatabase():
	print("   First-time database setup in progress.\n")
	conn = sqlite3.connect('cattlelog_database.db')
	c = conn.cursor()
	c.execute("""CREATE TABLE cattle (
				TagNumber INTEGER NOT NULL,
				BirthDate TEXT NOT NULL,
				DaysSinceBredHeat INTEGER,
				DaysTilDue INTEGER,
				GroupNumber INTEGER,
				TempGroupNumber INTEGER,
				ReproCode TEXT,
				TimesBred INTEGER,
				Breed TEXT,
				UsrDef1 TEXT,
				UsrDef2 TEXT,
				UsrDef3 TEXT,
				UsrDef4 TEXT,
				UsrDef5 TEXT,
				UsrDef6 TEXT,
				UsrDef7 TEXT,
				UsrDef8 TEXT,
				UsrDef9 TEXT,
				UsrDef10 TEXT,
				DaysTilNextHeat INTEGER,
				BarnName TEXT,
				DHIID TEXT,
				DamIndex INTEGER,
				DamName	TEXT,
				SireNameCode TEXT,
				TimesBredDate TEXT,
				DateDue TEXT,
				ServiceSireNameCode TEXT,
				NextExpHeat TEXT,
				AgeInMonthsAtCalving INTEGER,
				DonorDamID TEXT,
				FarmID TEXT,
				DamDHI_ID TEXT,
				PrevBredHeat1 TEXT,
				PrevBredHeat2 TEXT,
				PrevBredHeat3 TEXT,
				WeightBirth INTEGER,
				WeightWean INTEGER,
				WeightBred INTEGER,
				WeightPuberty INTEGER,
				WeightCalving	INTEGER,
				DaysInCurGroup INTEGER,
				DateLeft TEXT,
				Reason TEXT,
				PRIMARY KEY (TagNumber, BirthDate)
				)""")

	# May need to add a fourth (indexing) column to keep order?
	c.execute("""CREATE TABLE health (
				TagNumber INTEGER NOT NULL,
				BirthDate TEXT NOT NULL,
				HealthEvent TEXT NOT NULL,
				PRIMARY KEY (TagNumber, BirthDate, HealthEvent),
				FOREIGN KEY (TagNumber, BirthDate) REFERENCES cattle(TagNumber, BirthDate) ON DELETE CASCADE
				)""")

	c.execute("""CREATE TABLE treatment (
				TagNumber INTEGER NOT NULL,
				BirthDate TEXT NOT NULL,
				RecordNumber Integer NOT NULL,
				EventDate TEXT,
				PinkEye TEXT,
				EyeSide TEXT,
				Respiratory TEXT,
				Scours TEXT,
				Foot TEXT,
				FootPosition TEXT,
				Mastitis TEXT,
				Other TEXT,
				Details TEXT,
				PRIMARY KEY (TagNumber, BirthDate, RecordNumber),
				FOREIGN KEY (TagNumber, BirthDate) REFERENCES cattle(TagNumber, BirthDate) ON DELETE CASCADE
				)""")

	c.execute("""CREATE TABLE userFields (
				FieldNumber INTEGER NOT NULL PRIMARY KEY,
				FieldTitle TEXT,
				FieldDetails TEXT
				)""")


	# c.execute("""INSERT INTO cattle """)
	conn.commit()
	conn.close()
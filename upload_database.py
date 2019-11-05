import base64
import codecs
import datetime
import dropbox
from credentials import setAccessToken
import os

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        # Upload a file to Dropbox using API v2
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)

def uploadDatabase():
	print("************************************** Starting database upload. **************************************")
	current_dir = os.path.dirname(os.path.realpath(__file__))
	db_filename = 'cattlelog_database.db'
	db_filepath = os.path.join(current_dir, db_filename)

	access_token = setAccessToken()
	transferData = TransferData(access_token)

	file_from = db_filepath
	file_to = '/cattlelog_database.db'  # The full path to upload the file to, including the file name

	# API v2
	transferData.upload_file(file_from, file_to)
	print("************************************* Database finished uploading. ************************************")

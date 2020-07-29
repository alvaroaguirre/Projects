# By: alvaroaguirre
# Clean up messages in Outlook for Mac older than a year 

import os, datetime

# Set up the path and current directory
user = os.environ['USER']
outlook = "/Users/"+user+"/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/"

# Define a function to check if a file is older than a year
def older_than(file, number_of_days):
	created = datetime.datetime.fromtimestamp(os.path.getmtime(file))
	now = datetime.datetime.now()
	diff = (now-created).days
	if diff > number_of_days:
		return True
	else:
		return False

# Folder that hold the data
to_clean = ['Messages/', 'Messages Attachments/']

for folder in to_clean:
	cwd = outlook + folder
	os.chdir(cwd)
	
	# Get all the directories inside
	dir = [f for f in os.listdir() if os.path.isdir(f)]

	# Clean each directory
	for direc in dir:
		files = os.listdir(cwd+direc)
		for f in files:
			fn = cwd + direc + "/" + f
			if older_than(fn, 365):
				os.remove(fn)



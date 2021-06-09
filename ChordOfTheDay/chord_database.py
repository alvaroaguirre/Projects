# Loading libraries
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Using the credentials to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/ec2-user/.apikey/python.json', scope)

# Authorize
client = gspread.authorize(creds)

# Open the database
db = client.open("chord-database").sheet1

# Get the list of emails
subs = list(set(db.col_values(2)[1:]))

# Open the database of unsubscribers
unsub = client.open("unsubscribe-chord").sheet1
to_unsub = list(set(unsub.col_values(2)[1:]))

# Determine which emails need to be removed from database
subscribers = [element for element in subs if element not in to_unsub]
to_delete = [element for element in to_unsub if element in subs]

# Unsubscribe (Remove from database and from unsubscribe list)
for element in to_delete:
    index_delete = db.col_values(2).index(element)
    db.delete_row(index_delete+1)
    index_delete = unsub.col_values(2).index(element)
    unsub.delete_row(index_delete+1)

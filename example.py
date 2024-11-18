# Importing the library
import jouwloon

# Importing other stuff
from datetime import datetime
import pandas
import json

# Defining credentials
username = 'username' # Change this to your username
password = 'password' # Change this to your password

# Creating a session, loging in and saving it to 'session'
session = jouwloon.login(username, password)

# Making the start and end date
now = datetime.now()
end = pandas.to_datetime(now)+pandas.DateOffset(days=7)

# Fetching the calendar
calendar = jouwloon.getCalendar(session, now, end)

# Pretty printing the response
print(json.dumps(calendar, indent=4))
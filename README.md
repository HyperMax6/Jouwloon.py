# Jouwloon.py
Log in and fetch your working schedule from Jouwloon.

## Log in
To log in use the function `jouwloon.login(username, password)`.
This function will return the request session which is needed to make further requests.

## Fetching calender
Requesting calender information can be done with the function `jouwloon.getCalendar(session, start, end)`.
For `session` enter the session that you created with the `jouwloon.login()` function. This will return all working appointments planned between the `end` and `start` date. The returned object is a stripped down version of the jouwloon `/api/rooster/GetKalender` endpoint, as it includes a lot of useless and repeating information.

## Example
This is an example which prints all appointments withing the next 7 days:
```
# importing
import jouwloon
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
end = pandas.to_datetime(now)+pandas.DateOffset(weeks=1)

# Fetching the calendar
calendar = jouwloon.getCalendar(session, now, end)

# Pretty printing the response
print(json.dumps(calendar, indent=4))
```
Example output:
```
{
    "2024-11-23": {
        "start": "2024-11-23T15:00:00",
        "end": "2024-11-23T19:00:00",
        "afdeling": xxx,
        "vestiging": xxx
    }
}
```

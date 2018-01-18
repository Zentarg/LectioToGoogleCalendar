# LectioToGoogleCalendar
This project takes an individuals schedule from www.lectio.dk, and imports it into their Google calendar.

###Setup
1. Follow this guide: https://developers.google.com/api-client-library/python/start/installation

2. To use this script, you need to add your credentials to the users.json file:

..*The 'Name' column is just your name.
..*The 'calID' column is for your calendarID.
..*The 'credentialFileName' column is the name you want for the credential file the script creates.
..*The 'elevID' column is for the student ID lectio has given you.
..*The 'gymID' column is for the gymnasium ID lectio has given your gymnasium.

####How to find your calendar ID
1. Log in to your google calendar, (https://www.calendar.google.com)
2. Go to your calendar settings
3. Scroll down till you find your calendar ID.

Example calendar ID: i7ob50dh0k5n81cj9m5s5vf93s@group.calendar.google.com

####How to find your student ID
1. Log into lectio (https://www.lectio.dk)
2. Go to your schedule
3. Look at the url and copy the number that follows 'elevid='

####How to find your gymnasium ID
1. Find your school on the start site of lectio (https://www.lectio.dk)
2. Look at the url. The number following 'https://www.lectio.dk/lectio/' and before '/default.aspx' is your gymnasium ID.

3. Run the script with python 3.6

This script was developed by the following:

Zentarg - https://github.com/zentarg
LookACastle - https://github.com/lookacastle
EmilDichmann272 - https://github.com/emildichmann272

# add_events_Google_calendar
A script to get html from rugbykickoff.com using the requests package, convert to a readable string using bs4 and then parse the text create a list of rugby games with the details of each game. Finally use the Google calendar API to add reminders to a calendar, which can then be shared.

Some code is reproduced from https://github.com/karenapp/google-calendar-python-api
and the Google Calendar AIP reference https://developers.google.com/calendar/api/v3/reference


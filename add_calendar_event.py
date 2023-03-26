# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 16:55:14 2023

@author: eljac
"""

from datetime import datetime, timedelta
from calendar_setup import get_calendar_service


def add_event(name, desc, year, month, day, start_hour, start_min, length_hours, length_mins=0,
              calendarID='primary'):
    """
    Add an event to a google calendar, authorisation etc is handled by get_calendar_service()

    Parameters
    ----------
    name : str.
    desc : str.
    year : int.
    month : int.
    day : int.
    start_time : datetime.
    length : timedelta.
    calendarID : str, optional
        default = 'primary'.

    Returns : None.

    """
    service = get_calendar_service()

    start = datetime(year, month, day, start_hour, start_min)
    end = start + timedelta(hours=length_hours, minutes=length_mins)

    event_result = service.events().insert(calendarId=calendarID,
    body={
         "summary": name,
         "description": desc,
         "start": {"dateTime": start.isoformat(), "timeZone": 'Europe/Dublin'},
         "end": {"dateTime": end.isoformat(), "timeZone": 'Europe/Dublin'},
    }
    ).execute()

    print("summary: ", event_result['summary'])
    if 0:
        print("created event")
        print("id: ", event_result['id'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])


import googleapiclient
def clear_calendar(calendar_id=None):
    if not calendar_id: calendar_id = '69df93aaf5ff75f1af3632bba6fcc82b4ce32825a7a24d7a19ddc796fc157c5f@group.calendar.google.com'
    # Delete the event
    service = get_calendar_service()
    try:
        service.calendars().clear( calendarId=calendar_id ).execute()
        print("Calendar Cleared")
    except googleapiclient.errors.HttpError:
        print("Failed to delete event")




if __name__ == '__main__':

    name = 'Test'
    desc = 'This is a test'
    year = 2023
    month = 3
    day = 26
    start_hour = 13

    add_event(name, desc, year, month, day, start_hour, length_hours=2, length_mins=0,
              calendarID='69df93aaf5ff75f1af3632bba6fcc82b4ce32825a7a24d7a19ddc796fc157c5f@group.calendar.google.com')


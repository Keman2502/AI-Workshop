import json
from datetime import datetime, timedelta
import pytz
from google_auth import authenticate_calendar


def get_events(duration=None):
    service = authenticate_calendar()

    now = datetime.now()

    if not duration:
        start_of_week = now - timedelta(days=now.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        time_min = start_of_week.isoformat() + "Z"
        time_max = end_of_week.isoformat() + "Z"
    else:
        time_min = now.isoformat() + "Z"
        time_max = (now + timedelta(days=int(duration))).isoformat() + "Z"

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    print(events_result)
    events = events_result.get("items", [])

    events_list = []
    for event in events:
        event_data = {
            "start": event["start"].get("dateTime", event["start"].get("date")),
            "end": event["end"].get("dateTime", event["end"].get("date")),
            "summary": event.get("summary", "No Title"),
        }
        events_list.append(event_data)

    return json.dumps(events_list)


def create_event(
    title,
    start_time,
    end_time,
    description=None,
    location=None,
    attendees=None,
    conference=None,
    reminders=None,
    visibility="default",
    recurrence=None,
):
    service = authenticate_calendar()

    timezone = "Asia/Karachi"

    tz = pytz.timezone(timezone)
    start_time = tz.localize(datetime.fromisoformat(start_time))
    end_time = tz.localize(datetime.fromisoformat(end_time))

    event = {
        "summary": title,
        "location": location,
        "description": description,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": timezone,
        },
        "attendees": attendees,
        "visibility": visibility,  # Options: "default", "public", "private", "confidential"
        "reminders": {
            "useDefault": False,
            "overrides": (
                reminders
                if reminders
                else [
                    {"method": "popup", "minutes": 10},  # 10 minutes before
                ]
            ),
        },
    }

    if recurrence:
        event["recurrence"] = [recurrence]  # e.g., "RRULE:FREQ=DAILY;COUNT=5"

    if conference:
        event["conferenceData"] = {
            "createRequest": {
                "requestId": "conference_" + str(datetime.timestamp(start_time)),
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
            }
        }
    print(event)

    try:
        created_event = (
            service.events()
            .insert(calendarId="primary", body=event, conferenceDataVersion=1)
            .execute()
        )
        return json.dumps(f"Event created: {created_event.get('htmlLink')}")

    except Exception as e:
        return json.dumps(f"An error occurred: {e}")


# Function to Delete all events with a specific title

# Limitations: 
    # Only deletes events within a week from the current date
    # To delete events beyond a week, modify the time_min and time_max values
    # Does not take into consideration the Date and time, it simply deletes all events with the given title
def delete_event(title):
    service = authenticate_calendar()
    timezone = "Asia/Karachi"
    tz = pytz.timezone(timezone)
    
    now = datetime.now(tz)
    time_min = (now - timedelta(weeks=1)).isoformat()
    time_max = (now + timedelta(weeks=1)).isoformat()

    events_result = service.events().list(
        calendarId="primary",
        timeMin=time_min,
        timeMax=time_max,
        q=title,  # free text search filter
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    print("Event Results: ", events_result)
    
    events = events_result.get("items", [])
    deleted_events = []
    
    for event in events:
        try:
            service.events().delete(
                calendarId="primary", eventId=event["id"]
            ).execute()
            deleted_events.append(event.get("summary", ""))
        except Exception as e:
            print(f"Error deleting event '{event.get('summary', '')}': {e}")
    
    if deleted_events:
        return json.dumps(f"Deleted all events with title '{title}'.")
    else:
        return json.dumps(f"No event with title '{title}' was found.")


def check_attendee_availability(attendee_email, start_time, end_time):
    service = authenticate_calendar()
    
    timezone = "Asia/Karachi"
    tz = pytz.timezone(timezone)
    start = tz.localize(datetime.fromisoformat(start_time))
    end = tz.localize(datetime.fromisoformat(end_time))
    
    try:
        events_result = service.events().list(
            calendarId=attendee_email,
            timeMin=start.isoformat(),
            timeMax=end.isoformat(),
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return json.dumps(f"{attendee_email} is available during this time")
        
        conflicting_events = []
        for event in events:
            event_start = event['start'].get('dateTime')
            event_end = event['end'].get('dateTime')
            
            if event_start and event_end:  # Only check events with specific times
                event_start = datetime.fromisoformat(event_start.replace('Z', ''))
                event_end = datetime.fromisoformat(event_end.replace('Z', ''))
                
                if (event_start < end) and (event_end > start):
                    conflicting_events.append({
                        "title": event.get('summary', 'No title'),
                        "start": event_start.isoformat(),
                        "end": event_end.isoformat()
                    })
        
        if conflicting_events:
            return json.dumps({
                "conflict": True,
                "message": f"{attendee_email} has conflicting events",
                "conflicts": conflicting_events
            })
        return json.dumps(f"{attendee_email} is available during this time")
            
    except Exception as e:
        return json.dumps({
            "error": True,
            "message": f"Could not check availability: {str(e)}"
        })

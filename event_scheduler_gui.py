from __future__ import print_function
import datetime
import os.path
import tkinter as tk
from tkinter import messagebox
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ===========================================
# Revision 1 - 2024-03-19
# Changes made:
# 1. Added date format validation and auto-formatting for MM-DD-YYYY
# 2. Added automatic cursor movement for date input
# 3. Set default reminder to 30 minutes before event
# 4. Removed automatic time adjustments
# ===========================================

# Define the required Google Calendar API scopes
# This scope allows the application to read and write calendar events
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    """
    Establishes and returns a connection to the Google Calendar API.
    Handles authentication and token management.
    Returns:
        service: Google Calendar API service object
    """
    creds = None
    # Check if we have existing valid credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid credentials exist, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Create new credentials through OAuth flow
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build and return the Calendar API service
    service = build('calendar', 'v3', credentials=creds)
    return service

def format_date_input(P):
    """
    Formats the date input as MM-DD-YYYY with automatic cursor movement.
    Args:
        P: The current input value
    Returns:
        str: Formatted date string
    """
    if len(P) <= 10:  # Maximum length of MM-DD-YYYY
        # Remove any non-digit characters
        digits = ''.join(filter(str.isdigit, P))
        
        # Format the date with automatic dashes
        if len(digits) > 0:
            if len(digits) <= 2:
                return digits
            elif len(digits) <= 4:
                return f"{digits[:2]}-{digits[2:]}"
            else:
                return f"{digits[:2]}-{digits[2:4]}-{digits[4:8]}"
    return P

def validate_date(P):
    """
    Validates the date format and ensures proper input length.
    Args:
        P: The current input value
    Returns:
        bool: True if input is valid, False otherwise
    """
    if len(P) <= 10:
        return True
    return False

def add_event_to_calendar(summary, date_str, time_str):
    """
    Creates a new event in the user's Google Calendar.
    Args:
        summary: Event title/name
        date_str: Date in MM-DD-YYYY format
        time_str: Time in HH:MM 24-hour format
    """
    try:
        service = get_calendar_service()
        # Convert MM-DD-YYYY to YYYY-MM-DD for Google Calendar
        month, day, year = date_str.split('-')
        formatted_date = f"{year}-{month}-{day}"
        event_datetime = f"{formatted_date}T{time_str}:00"
        
        # Create event object with all required fields
        event = {
            'summary': summary,
            'start': {
                'dateTime': event_datetime,
                'timeZone': 'America/Chicago',
            },
            'end': {
                'dateTime': (datetime.datetime.fromisoformat(event_datetime) + datetime.timedelta(hours=1)).isoformat(),
                'timeZone': 'America/Chicago',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 30},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }
        # Insert the event into the calendar
        event = service.events().insert(calendarId='primary', body=event).execute()
        messagebox.showinfo("Success", f"Event created!\n{event.get('htmlLink')}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def submit_event():
    """
    Handles the event submission process.
    Validates input and calls add_event_to_calendar if valid.
    """
    name = entry_name.get()
    date = entry_date.get()
    time = entry_time.get()

    # Validate that all fields are filled
    if not name or not date or not time:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    # Validate date format
    try:
        month, day, year = date.split('-')
        if not (1 <= int(month) <= 12 and 1 <= int(day) <= 31 and len(year) == 4):
            messagebox.showwarning("Input Error", "Invalid date format. Please use MM-DD-YYYY.")
            return
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid date format. Please use MM-DD-YYYY.")
        return

    add_event_to_calendar(name, date, time)

# Create the main application window
root = tk.Tk()
root.title("John's Event App")

# Create and layout the input fields
tk.Label(root, text="Event/Task Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=5)

# Date input field with validation and auto-formatting
tk.Label(root, text="Date (MM-DD-YYYY):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
vcmd = (root.register(validate_date), '%P')
entry_date = tk.Entry(root, width=30, validate='key', validatecommand=vcmd)
entry_date.grid(row=1, column=1, padx=10, pady=5)
entry_date.bind('<KeyRelease>', lambda e: entry_date.delete(0, tk.END) or entry_date.insert(0, format_date_input(entry_date.get())))

# Time input field
tk.Label(root, text="Time (HH:MM 24hr):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_time = tk.Entry(root, width=30)
entry_time.grid(row=2, column=1, padx=10, pady=5)

# Submit button
submit_btn = tk.Button(root, text="Add Event to Calendar", command=submit_event)
submit_btn.grid(row=3, column=0, columnspan=2, pady=15)

# Start the application
root.mainloop()

from __future__ import print_function
import datetime
import os.path
import tkinter as tk
from tkinter import messagebox
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request 


# ===========================================
# Revision 5 - 2025-05-14
# Changes made:
# 1. Clears input fields after successful submission.
# 2. Sets focus back to the Event Name field.
# ===========================================

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def add_event_to_calendar(summary, date_str, time_str):
    try:
        service = get_calendar_service()
        month, day, year = date_str.split('-')
        event_start = datetime.datetime(
            int(year), int(month), int(day),
            int(time_str.split(':')[0]),
            int(time_str.split(':')[1])
        )

        event = {
            'summary': summary,
            'start': {
                'dateTime': event_start.isoformat(),
                'timeZone': 'America/Denver',
            },
            'end': {
                'dateTime': (event_start + datetime.timedelta(hours=1)).isoformat(),
                'timeZone': 'America/Denver',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 30},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        messagebox.showinfo("Success", f"Event created!\n{event.get('htmlLink')}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def submit_event():
    name = entry_name.get()
    date = entry_date.get()
    time = entry_time.get()

    if not name or not date or not time:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        month, day, year = date.split('-')
        if not (1 <= int(month) <= 12 and 1 <= int(day) <= 31 and len(year) == 4):
            messagebox.showwarning("Input Error", "Invalid date format. Please use MM-DD-YYYY.")
            return
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid date format. Please use MM-DD-YYYY.")
        return

    add_event_to_calendar(name, date, time)

    # ✅ Clear input fields after successful submission
    entry_name.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_time.delete(0, tk.END)
    entry_name.focus_set()

# ================================
# GUI Setup
# ================================

root = tk.Tk()
root.title("John's Event App")

# Event/Task Name
tk.Label(root, text="Event/Task Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=5)

# Date
tk.Label(root, text="Date (MM-DD-YYYY):").grid(row=1, column=0, padx=10, pady=5, sticky="e")

def validate_date_input(P):
    return P == "" or (P.replace("-", "").isdigit() and len(P.replace("-", "")) <= 8)

vcmd_date = (root.register(validate_date_input), '%P')
entry_date = tk.Entry(root, width=30, validate='key', validatecommand=vcmd_date)
entry_date.grid(row=1, column=1, padx=10, pady=5)

def format_date_on_focus_out(event):
    digits = ''.join(filter(str.isdigit, entry_date.get()))
    if len(digits) >= 4:
        formatted = digits[:2] + '-' + digits[2:4]
        if len(digits) >= 8:
            formatted += '-' + digits[4:8]
        entry_date.delete(0, tk.END)
        entry_date.insert(0, formatted)

entry_date.bind('<FocusOut>', format_date_on_focus_out)

# Time
tk.Label(root, text="Time (HH:MM 24hr):").grid(row=2, column=0, padx=10, pady=5, sticky="e")

def validate_time_input(P):
    return P == "" or (P.replace(":", "").isdigit() and len(P.replace(":", "")) <= 4)

vcmd_time = (root.register(validate_time_input), '%P')
entry_time = tk.Entry(root, width=30, validate='key', validatecommand=vcmd_time)
entry_time.grid(row=2, column=1, padx=10, pady=5)

def format_time_on_focus_out(event):
    digits = ''.join(filter(str.isdigit, entry_time.get()))
    if len(digits) >= 2:
        formatted = digits[:2]
        if len(digits) >= 4:
            formatted += ':' + digits[2:4]
        elif len(digits) > 2:
            formatted += ':' + digits[2:]
        entry_time.delete(0, tk.END)
        entry_time.insert(0, formatted)

entry_time.bind('<FocusOut>', format_time_on_focus_out)

# Submit Button
submit_btn = tk.Button(root, text="Add Event to Calendar", command=submit_event)
submit_btn.grid(row=3, column=0, columnspan=2, pady=15)

# Start the app
root.mainloop()

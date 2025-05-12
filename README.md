# Event Scheduler GUI

## Description
A Python Tkinter-based desktop app that allows you to add events to your Google Calendar.

## Setup Instructions

1. Set up Google Cloud Project and OAuth credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Calendar API:
     - In the left sidebar, click on "APIs & Services" > "Library"
     - Search for "Google Calendar API"
     - Click "Enable"
   - Create OAuth credentials:
     - In the left sidebar, click on "APIs & Services" > "Credentials"
     - Click "Create Credentials" > "OAuth client ID"
     - Select "Desktop app" as the application type
     - Give it a name (e.g., "Event Scheduler")
     - Click "Create"
   - Download the credentials:
     - Click the download icon (⬇️) next to your newly created OAuth client
     - Rename the downloaded file to `credentials.json`
     - Place it in this folder (same folder as script and batch file)

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   - Double-click `run_event_scheduler_gui.bat` to run the app
   - For quick access, create a desktop shortcut:
     - Right-click on `run_event_scheduler_gui.bat`
     - Select "Create shortcut"
     - Move the shortcut to your desktop
     - (Optional) Right-click the shortcut > Properties > Change Icon to customize its appearance

4. First-time setup:
   - When you run the app for the first time, it will open your default web browser
   - Sign in with your Google account
   - You will be asked to grant the following permissions:
     - "View and edit events on all your calendars" - This allows the app to:
       - Create new events in your calendar
       - Set event reminders
       - Manage event details
     - "View your calendars" - This allows the app to:
       - Access your calendar list
       - Read calendar settings
   - Click "Continue" to grant these permissions
   - The app will automatically create a `token.json` file in the same folder
     - This file stores your authentication token and refresh token
     - It allows the app to access your calendar without requiring you to log in again
     - Keep this file secure as it provides access to your calendar
     - The file will be automatically updated when needed

5. Enter event details and they will be added to your Google Calendar.

## Troubleshooting

- If you get an error about missing credentials, ensure `credentials.json` is in the correct folder
- If you get authentication errors:
  - Delete the `token.json` file and restart the application
  - This will force the app to go through the authentication process again
- Make sure you have a stable internet connection when running the app
- If you need to revoke access:
  - Go to your [Google Account Security Settings](https://myaccount.google.com/security)
  - Find "Third-party apps with account access"
  - Remove the Event Scheduler app
  - Delete the `token.json` file from your computer

## Note
The application requires Python 3.6 or higher to run properly.

## License
This project is licensed under the terms of the MIT license. See the [LICENSE.md](LICENSE.md) file for details.

## Google API Setup
Ensure you have enabled the Google Calendar API and created OAuth credentials (Desktop type) in Google Cloud Console.

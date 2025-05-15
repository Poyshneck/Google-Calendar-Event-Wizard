# Revision History

---

## Revision 5 - 2025-05-14  
**Changes made:**  
1. Clears input fields after successful submission.  
2. Sets focus back to the Event Name field.

---

## Revision 4 - 2025-05-11 19:08 MDT  
**Changes made:**  
1. Fixed missing import for `Request()` from `google.auth.transport.requests`.  
2. Replaced `<KeyRelease>` auto-formatting with input validation via `validatecommand` on each keystroke.  
3. Implemented clean auto-formatting for both Date and Time fields on `<FocusOut>` event.  
4. Ensured numeric-only input for both Date (MM-DD-YYYY) and Time (HH:MM) fields.  
5. Eliminated backspacing and cursor jump issues in date and time entry fields.  
6. Retained Google Calendar API integration, reminders, and event creation logic.  
7. Preserved previous revision comments for audit trail.

---

## Revision 3 - 2025-05-11 18:42 MDT  
**Changes made:**  
1. Replaced problematic `<KeyRelease>` event binding with input validation on keystroke.  
2. Added clean auto-formatting for date and time fields on `<FocusOut>`.  
3. Prevented cursor backspacing issue during typing.  
4. Retained numeric-only input for both date and time fields.  
5. Fixed missing `Request()` import from `google.auth.transport.requests`.

---

## Revision 2 - 2025-05-11  
**Changes made:**  
1. Added date format validation and auto-formatting for MM-DD-YYYY.  
2. Added time format validation and auto-formatting for HH:MM.  
3. Improved cursor management for both fields.  
4. Cleaned up redundant operations.

---

## Revision 1 - 2025-05-11  
**Changes made:**  
1. Added date format validation and auto-formatting for MM-DD-YYYY.  
2. Added automatic cursor movement for date input.  
3. Set default reminder to 30 minutes before event.  
4. Removed automatic time adjustments.

---

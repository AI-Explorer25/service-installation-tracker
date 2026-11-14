# Service and Installation Tracker

A Python command-line application for tracking installation jobs and annual services. It models common service-operations workflows: maintaining customer job records, updating progress and identifying maintenance that needs attention.

Built as a learning project using fictional records and Python's standard library.

## Features

- View jobs and search by unique ID.
- Add jobs with input validation and duplicate-ID checks.
- Update status: Scheduled, In progress or Completed.
- List overdue annual services and those due within 30 days.
- Save and reload records using JSON.

Each record contains an ID, customer name, location, job type, scheduled date and status.

## Run

Developed with Python 3.13.9 on Windows using VS Code and Conda. No third-party packages are required.

From the project folder, with Python available in your terminal:

```bash
python main.py
```

Choose an action from the numbered menu. Select **7. Save jobs** to persist changes before exiting. Saving is manual; unsaved changes are lost when the program closes.

The repository includes `jobs.json` with fictional example records, loaded automatically on startup. Saving updates this file beside `main.py`, so changes will appear in Git for review before committing. If the file is missing, the application starts with the sample records defined in the code.

## Service rules

Both filters include only annual services with status Scheduled or In progress. Installations and completed jobs are excluded.

| Filter | Scheduled date |
| --- | --- |
| Overdue | Before the reference date |
| Upcoming | From the reference date through 30 days later, inclusive |

The menu uses the computer's current date. Tests use a fixed reference date for reproducible results. Dates must be entered as `YYYY-MM-DD` and represent valid calendar dates.

## Tests

```bash
python test_tracker.py
```

Assertion-based checks cover date boundaries, completed-service exclusions, overdue installation exclusion, duplicate IDs, status updates and JSON round trips. File tests use a temporary directory and do not modify the application's saved records.

## Structure and scope

- `main.py`: job operations, input validation, menu and JSON storage.
- `test_tracker.py`: automated checks using fictional test records.
- `jobs.json`: committed fictional example data and the application's working records.

Jobs are represented as dictionaries within a list. Functions separate record operations from terminal interaction. The `main()` entry point allows functions to be imported for testing without starting the menu.

This is a local, single-user learning application, not a production CRM. Loaded JSON is not yet checked for record structure, and saves replace the existing file directly. Authentication, concurrent access and database storage are outside the current scope.

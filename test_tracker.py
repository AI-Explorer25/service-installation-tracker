from datetime import date
from main import find_overdue_services, find_upcoming_services, add_job, save_jobs, load_jobs, update_job_status

from pathlib import Path
from tempfile import TemporaryDirectory


reference_date = date(2026, 11, 14)

test_jobs = [
    {
        "id": 1,
        "customer_name": "Test Court",
        "location": "Maidstone",
        "job_type": "Annual service",
        "scheduled_date": "2026-11-14",
        "status": "Scheduled",
    }
]

overdue = find_overdue_services(test_jobs, reference_date)
upcoming = find_upcoming_services(test_jobs, reference_date)

assert overdue == [], "A service due today must not be overdue."
assert upcoming == test_jobs, "A service due today must be upcoming."

print("Due-today test passed.")

test_jobs[0]["scheduled_date"] = "2026-12-14"

upcoming = find_upcoming_services(test_jobs, reference_date)

assert upcoming == test_jobs, "A service exactly 30 days away must be included."

test_jobs[0]["scheduled_date"] = "2026-12-15"

upcoming = find_upcoming_services(test_jobs, reference_date)

assert upcoming == [], "A service 31 days away must be excluded."

test_jobs[0]["scheduled_date"] = "2026-11-24"

upcoming = find_upcoming_services(test_jobs, reference_date)

assert upcoming == test_jobs, "A service within 30 days must be included."

test_jobs[0]["status"] = "Completed"

upcoming = find_upcoming_services(test_jobs, reference_date)

assert upcoming == [], "Completed jobs must be excluded from upcoming services."

print("30-day boundary tests passed.")

test_jobs[0]["scheduled_date"] = "2026-11-13"
test_jobs[0]["status"] = "Scheduled"

overdue = find_overdue_services(test_jobs, reference_date)
upcoming = find_upcoming_services(test_jobs, reference_date)

assert overdue == test_jobs, "An unfinished service before today must be overdue."
assert upcoming == [], "An overdue service must not appear as upcoming."

test_jobs[0]["status"] = "Completed"

overdue = find_overdue_services(test_jobs, reference_date)

assert overdue == [], "Completed services must be excluded from overdue results."

test_jobs[0]["status"] = "Scheduled"

test_jobs[0]["job_type"] = "Installation"

overdue = find_overdue_services(test_jobs, reference_date)

assert overdue == [], "Installations must be excluded from overdue service results."

print("Overdue-service tests passed.")

duplicate_job = test_jobs[0].copy()
duplicate_job["customer_name"] = "Duplicate Customer"

original_jobs = [test_jobs[0].copy()]

was_added = add_job(test_jobs, duplicate_job)

assert was_added is False, "Adding a duplicate ID must fail."
assert test_jobs == original_jobs, "A rejected duplicate must leave records unchanged."

duplicate_job["id"] = 2

was_added = add_job(test_jobs, duplicate_job)

assert was_added is True, "A job with a unique ID must be added."
assert len(test_jobs) == 2, "The list must contain two jobs after adding one."

print("Duplicate-ID test passed.")

with TemporaryDirectory() as temporary_folder:
    test_file = Path(temporary_folder) / "test_jobs.json"

    assert load_jobs(test_file) is None, "A missing file must return None."

    was_saved = save_jobs(test_jobs, test_file)
    assert was_saved is True, "Saving valid jobs must succeed."

    loaded_jobs = load_jobs(test_file)
    assert loaded_jobs == test_jobs, "Loaded jobs must match the saved records."

    was_saved = save_jobs([], test_file)
    assert was_saved is True, "Saving an empty list must succeed."

    loaded_jobs = load_jobs(test_file)
    assert loaded_jobs == [], "An empty saved list must reload as an empty list."
print("JSON saving and loading tests passed.")

test_jobs[0]["status"] = "Scheduled"
job_id = test_jobs[0]["id"]

was_updated = update_job_status(test_jobs, job_id, "Completed")

assert was_updated is True, "A valid status update must succeed."
assert test_jobs[0]["status"] == "Completed", "The job's status must change."

was_updated = update_job_status(test_jobs, job_id, "Finished")

assert was_updated is False, "An invalid status must be rejected."
assert test_jobs[0]["status"] == "Completed", "A rejected update must preserve the status."

was_updated = update_job_status(test_jobs, 999, "Scheduled")
assert was_updated is False, "Updating a nonexistent job ID must fail."

print("Status-update tests passed.")
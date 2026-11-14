
from datetime import date, timedelta
import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "jobs.json"


jobs = [
    {
        "id": 1,
        "customer_name": "Example Court",
        "location": "Maidstone",
        "job_type": "Annual service",
        "scheduled_date": "2026-11-23",
        "status": "Scheduled",
    },
    {
        "id": 2,
        "customer_name": "Willow House",
        "location": "Ashford",
        "job_type": "Installation",
        "scheduled_date": "2026-11-25",
        "status": "In progress",
    },
]

def view_jobs(job_records):
    if not job_records:
        print("No jobs found.")
        return
    
    for job in job_records:
        print(
            f"{job['id']}: {job['customer_name']} | "
            f"{job['job_type']} | {job['scheduled_date']} | "
            f"{job['status']} | {job['location']}"
        )
        

def find_job(job_records, job_id):
    for job in job_records:
        if job["id"] == job_id:
            return job

    return None

def update_job_status(job_records, job_id, new_status):
    allowed_statuses = ["Scheduled", "In progress", "Completed"]

    if new_status not in allowed_statuses:
        return False

    job = find_job(job_records, job_id)

    if job is None:
        return False

    job["status"] = new_status
    return True

def add_job(job_records, new_job):
    existing_job = find_job(job_records, new_job["id"])

    if existing_job is not None:
        return False

    job_records.append(new_job)
    return True

def find_overdue_services(job_records, reference_date):
    overdue_jobs = []

    for job in job_records:
        scheduled_date = date.fromisoformat(job["scheduled_date"])

        if (
            job["job_type"] == "Annual service"
            and job["status"] in ["Scheduled", "In progress"]
            and scheduled_date < reference_date
        ):
            overdue_jobs.append(job)

    return overdue_jobs

def find_upcoming_services(job_records, reference_date):
    upcoming_jobs = []
    end_date = reference_date + timedelta(days=30)

    for job in job_records:
        scheduled_date = date.fromisoformat(job["scheduled_date"])

        if (
            job["job_type"] == "Annual service"
            and job["status"] in ["Scheduled", "In progress"]
            and reference_date <= scheduled_date <= end_date
        ):
            upcoming_jobs.append(job)

    return upcoming_jobs

def get_valid_choice(prompt, allowed_values):
    while True:
        value = input(prompt).strip()

        if value in allowed_values:
            return value

        print(f"Please choose from: {', '.join(allowed_values)}")

def get_required_text(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be blank.")

def get_scheduled_date():
    while True:
        value = input("Scheduled date (YYYY-MM-DD): ").strip()

        try:
            parsed_date = date.fromisoformat(value)
        except ValueError:
            print("Enter a real date in YYYY-MM-DD format.")
        else:
            if value == parsed_date.isoformat():
                return value

            print("Use YYYY-MM-DD format, such as 2026-11-23.")

def get_job_id():
    while True:
        try:
            entered_id = int(input("Enter a job ID: "))
        except ValueError:
            print("Please enter a whole number, such as 2.")
        else:
            return entered_id

def load_jobs(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def save_jobs(job_records, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(job_records, file, indent=4)
    except OSError as error:
        print(f"Could not save jobs: {error}")
        return False

    return True

def collect_job(job_records):
    job_id = get_job_id()

    if find_job(job_records, job_id) is not None:
        print("That job ID already exists.")
        return None

    customer_name = get_required_text("Customer name: ")
    location = get_required_text("Location: ")
    job_type = get_valid_choice(
        "Job type (Installation, Annual service): ",
        ["Installation", "Annual service"],
    )
    scheduled_date = get_scheduled_date()
    status = get_valid_choice(
        "Status (Scheduled, In progress, Completed): ",
        ["Scheduled", "In progress", "Completed"],
    )

    return {
        "id": job_id,
        "customer_name": customer_name,
        "location": location,
        "job_type": job_type,
        "scheduled_date": scheduled_date,
        "status": status,
    }

def main():
    try:
        saved_jobs = load_jobs(DATA_FILE)
    except (OSError, ValueError) as error:
        print(f"Could not load saved jobs: {error}")
        print("Check jobs.json before restarting. No changes have been saved.")
        return
    if saved_jobs is not None:
        job_records = saved_jobs
    else:
        job_records = jobs

    while True:
        print("\nService and installation tracker")
        print("1. View all jobs")
        print("2. Find a job")
        print("3. Update a job's status")
        print("4. Add a job")
        print("5. View overdue services")
        print("6. View services due within 30 days")
        print("7. Save jobs")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_jobs(job_records)
        elif choice == "2":
            entered_id = get_job_id()
            result = find_job(job_records, entered_id)

            if result is None:
                print("Job not found.")
            else:
                view_jobs([result])
        elif choice == "3":
            entered_id = get_job_id()
            new_status = input(
                "Enter status (Scheduled, In progress, Completed): "
            ).strip()

            was_updated = update_job_status(job_records, entered_id, new_status)

            if was_updated:
                print("Status updated.")
            else:
                print("Update failed: job ID not found or status invalid.")
        
        elif choice == "4":
            new_job = collect_job(job_records)

            if new_job is not None:
                was_added = add_job(job_records, new_job)

                if was_added:
                    print("Job added.")
                else:
                    print("Job could not be added: duplicate ID.")
        
        elif choice == "5":
            reference_date = date.today()
            overdue_jobs = find_overdue_services(job_records, reference_date)
            view_jobs(overdue_jobs)
        
        elif choice == "6":
            reference_date = date.today()
            upcoming_jobs = find_upcoming_services(job_records, reference_date)
            view_jobs(upcoming_jobs)
        
        elif choice == "7":
            if save_jobs(job_records, DATA_FILE):
                print("Jobs saved.")
        
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Please choose 1, 2, 3, 4, 5, 6, 7 or 0.")


if __name__ == "__main__":
    main()
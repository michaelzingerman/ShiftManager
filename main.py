# main.py

import pandas as pd

from uility.parser import load_workers_from_csv
from models.employee import Employee
from models.scheduler import Scheduler
from uility.helpers import export_schedule_to_csv


CSV_PATH = "data/raw/workers.csv"


def create_employee_objects(worker_dicts):
    employees = []
    for w in worker_dicts:
        emp = Employee(
            first_name=w["first_name"],
            last_name=w["last_name"],
            role=w["role"],
            min_shifts=w["min_shifts"],
            max_shifts=w["max_shifts"],
            availability=w["availability"]
        )
        employees.append(emp)
    return employees


def generate_schedule():
    workers_raw = load_workers_from_csv(CSV_PATH)
    employees = create_employee_objects(workers_raw)

    scheduler = Scheduler(employees)
    schedule = scheduler.run()

    print("\nWEEKLY SCHEDULE:\n")
    df = schedule.to_dataframe()
    print(df)

    # Export CSV
    export_schedule_to_csv(df)

    print("\nSHIFT SUMMARIES:\n")
    scheduler.print_summary()

    # Check min shifts
    under = scheduler.validate_min_shifts()
    if under:
        print("\n⚠ Workers who did NOT reach minimum required shifts:")
        for e in under:
            print(f" - {e.full_name()} ({e.shifts_assigned_count()} shifts)")
    else:
        print("\nAll workers reached minimum required shifts.")

    return schedule


def main_menu():
    while True:
        print("\n===== SHIFT MANAGER MENU =====")
        print("1. Generate weekly schedule")
        print("2. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            generate_schedule()
        elif choice == "2":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main_menu()

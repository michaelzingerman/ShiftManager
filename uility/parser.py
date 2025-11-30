import pandas as pd
from config.settings import (
    DAYS, SHIFTS,
    AVAILABILITY_SEPARATOR_DAYS,
    AVAILABILITY_SEPARATOR_SHIFTS
)


def parse_availability_string(availability_str):
    availability = {day: [] for day in DAYS}
    if not isinstance(availability_str, str):
        return availability

    day_blocks = availability_str.split(AVAILABILITY_SEPARATOR_DAYS)

    for block in day_blocks:
        block = block.strip()
        if not block:
            continue

        if ":" not in block:
            continue

        day, shifts_str = block.split(":", 1)
        day = day.strip()

        if day not in DAYS:
            continue

        shifts_str = shifts_str.strip()

        # Case: none
        if shifts_str.lower() == "none":
            availability[day] = []
            continue

        # Case: all
        if shifts_str.lower() == "all":
            availability[day] = list(SHIFTS.keys())
            continue

        # Case: specific shifts
        shifts = [
            s.strip().lower()
            for s in shifts_str.split(AVAILABILITY_SEPARATOR_SHIFTS)
            if s.strip()
        ]

        # Filter out invalid shift names
        shifts = [s for s in shifts if s in SHIFTS.keys()]

        availability[day] = shifts

    return availability


def load_workers_from_csv(csv_path):
    """
    Reads workers.csv and returns a list of dictionaries,
    each representing one worker.
    This will be converted to Employee objects later.
    """
    df = pd.read_csv(csv_path)

    workers = []
    for _, row in df.iterrows():
        worker = {
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "role": row["role"].lower(),
            "min_shifts": int(row["min_shifts"]),
            "max_shifts": int(row["max_shifts"]),
            "availability": parse_availability_string(row["availability"])
        }
        workers.append(worker)

    return workers

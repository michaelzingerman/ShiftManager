# uility/helpers.py

import os
import pandas as pd

def export_schedule_to_csv(schedule_df, path="data/processed/schedule_output.csv"):
    """
    Saves the schedule DataFrame as a CSV.
    Automatically creates the folder if it doesn't exist.
    Prints the full absolute path so you know where it went.
    """

    # directory = "data/processed"
    directory = os.path.dirname(path)

    # Create directory if missing
    os.makedirs(directory, exist_ok=True)

    # Write file
    schedule_df.to_csv(path, index=True)

    # Print absolute path
    full_path = os.path.abspath(path)
    print(f"\nCSV exported to:\n{full_path}\n")

import os
import csv

SCHEDULES_DIR = "output"  # directory where all schedule CSVs are stored


# List all saved schedule CSV files
def list_schedules():
    if not os.path.exists(SCHEDULES_DIR):  # check if folder exists
        return []
    return [
        f for f in os.listdir(SCHEDULES_DIR) if f.endswith(".csv")
    ]  # filter only CSV files


# Read a schedule from a CSV file
def read_schedule(filename):
    filepath = os.path.join(SCHEDULES_DIR, filename)  # build full path
    with open(filepath, newline="") as csvfile:
        reader = csv.reader(csvfile)  # csv.reader turns file into list of rows
        return list(reader)

import argparse
import csv
from datetime import datetime
from pathlib import Path


#Loggin a pushup set from the command line.

CSV_PATH = Path(__file__).resolve().parent.parent / "Data" / "pushups.csv"

def append_entry(reps):
    needs_header = not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0
    with CSV_PATH.open("a", newline="") as f:
        writer = csv.writer(f)
        if needs_header:
            writer.writerow(["timestamp", "reps"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), reps])

def main():
    parser = argparse.ArgumentParser(description="Log a pushup set.")
    parser.add_argument("reps", type=int, help="number of pushups in this set")
    args = parser.parse_args()
    append_entry(args.reps)
    print(f"Logged {args.reps} pushups")

if __name__ == "__main__":
    main()
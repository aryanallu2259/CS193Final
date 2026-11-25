import argparse
import csv
import subprocess
from datetime import datetime
from pathlib import Path


#Loggin a pushup set from the command line.

CSV_PATH = Path(__file__).resolve().parent.parent / "Data" / "pushups.csv"
REPO_ROOT = CSV_PATH.parent.parent

def append_entry(reps):
    needs_header = not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0
    with CSV_PATH.open("a", newline="") as f:
        writer = csv.writer(f)
        if needs_header:
            writer.writerow(["timestamp", "reps"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), reps])

def push_to_github(reps):
    def git(*args):
        subprocess.run(["git", *args], cwd=REPO_ROOT, check=True)

    try:
        git("add", "Data/pushups.csv")
        git("commit", "-m", f"Log {reps} pushups")
        git ("push")
    except subprocess.CalledProcessError:
        print("Saved locally, but Github push failed. Please check your connection")

def main():
    parser = argparse.ArgumentParser(description="Log a pushup set.")
    parser.add_argument("reps", type=int, help="number of pushups in this set")
    args = parser.parse_args()
    append_entry(args.reps)
    print(f"Logged {args.reps} pushups")
    push_to_github(args.reps)

if __name__ == "__main__":
    main()
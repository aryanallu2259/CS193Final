import argparse

#Loggin a pushup set from the command line.

def main():
    parser = argparse.ArgumentParser(description="Log a pushup set.")
    parser.add_argument("reps", type=int, help="number of pushups in this set")
    args = parser.parse_args()
    print(f"Logged {args.reps} pushups")

if __name__ == "__main__":
    main()
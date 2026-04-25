import os
from scanner import scan_directory
import json

def main():
    os.makedirs("data", exist_ok=True)

    files = scan_directory(".")

    print(f"Found {len(files)} files")

    for f in files[:5]:
        print(f)

    # Save the file records to a JSON file
    with open("data/files.json", "w") as f:
        json.dump(files, f)


if __name__ == "__main__":
    main()
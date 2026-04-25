import json
from scanner import scan_directory


if __name__ == "__main__":
    root = "."

    scanned = scan_directory(root)

    with open("structure.json", "w", encoding="utf-8") as f:
        json.dump(scanned, f, indent=2)

    print("Scan complete → structure.json generated")
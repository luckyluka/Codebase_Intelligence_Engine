from scanner import scan_directory


def main():
    files = scan_directory(".")

    print(f"Found {len(files)} files")

    for f in files[:5]:
        print(f)


if __name__ == "__main__":
    main()
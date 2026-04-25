from scanner import scan_directory


def main():
    root = "."  # current directory
    files = scan_directory(root)

    print(f"Found {len(files)} files")
    for f in files[:10]:  # print first 10 only
        print(f)


if __name__ == "__main__":
    main()
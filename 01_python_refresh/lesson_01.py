from pathlib import Path

print("Current working directory:", Path.cwd())
print("Home directory:", Path.home())

folder = Path(input("Enter a folder path: "))

if folder.exists() and folder.is_dir():
    print("\n--- Directory Inspection Report ---")
    print(f"Name:          {folder.name}")
    print(f"Exists:        Yes")
    print(f"Absolute path: {folder.resolve()}")
    print(f"Status:        Valid directory confirmed")
    print("-----------------------------------")
else:
    print(f"\nError: '{folder}' does not exist or is not a directory.")
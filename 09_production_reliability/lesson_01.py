def run_operation(name):
    if not name:
        print("Operation name is required.")
        return False

    print(f"Running operation: {name}")
    return True


def main():
    result = run_operation("system check")
    print(f"Success: {result}")


if __name__ == "__main__":
    main()
from Models import Schedule

# Display a saved schedule
def display_schedule():
    
    schedules = Schedule.list_schedules()  # get saved CSVs
    if not schedules:  # no files found
        print("No saved schedules found.")
        return

    # Display numbered list of schedules
    print("\nWhich Schedule?")
    for idx, fname in enumerate(schedules, start=1):
        print(f"{idx}. {fname}")

    # Prompt for user choice
    choice = input("\nEnter a number or file name: ").strip()

    # If user enters a number, convert to file name
    if choice.isdigit():  
        index = int(choice) - 1  # adjust because list is 0-based
        if 0 <= index < len(schedules):
            filename = schedules[index]
        else:
            print("Invalid number.")
            return
    # If user enters the exact file name
    elif choice in schedules:
        filename = choice
    else:
        print("Invalid choice.")
        return

    # Read the selected CSV file
    rows = Schedule.read_schedule(filename)

    # Print the schedule contents in a readable way
    print("\n--- Schedule Contents ---")
    for row in rows:
        print(" | ".join(row))  # join row items with vertical bars
    print("-------------------------\n")

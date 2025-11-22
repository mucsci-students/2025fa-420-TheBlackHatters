# CLI/time_slot_cli.py

from typing import List
from Models.Data_manager import DataManager


def displayTimeSlots(data_manager: DataManager):
    """Display all time intervals organized by day."""
    ts_config = data_manager.getTimeSlotConfig()
    times = ts_config.times

    print("\n" + "=" * 50)
    print("           TIME SLOT CONFIGURATION")
    print("=" * 50)

    if not times:
        print("\nNo time intervals configured.\n")
        return

    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for day in days_order:
        if day not in times:
            continue
        
        intervals = times[day]
        print(f"\n{day}:")
        print("-" * 40)
        
        if not intervals:
            print("  (no intervals)")
            continue
            
        for idx, iv in enumerate(intervals):
            print(f"  [{idx}] {iv.start} - {iv.end} (every {iv.spacing} min)")
            
            # Show generated slots
            slots = iv.generate_slots()
            if len(slots) <= 8:
                slots_str = ", ".join(slots)
            else:
                slots_str = ", ".join(slots[:4]) + " ... " + ", ".join(slots[-2:])
            print(f"      Slots: {slots_str}")
            
            # Show optional fields if present
            if iv.professors:
                print(f"      Professors: {', '.join(iv.professors)}")
            if iv.labs:
                print(f"      Labs: {', '.join(iv.labs)}")
            if iv.courses:
                print(f"      Courses: {', '.join(iv.courses)}")

    print("\n" + "=" * 50 + "\n")


def displayGeneratedSlots(data_manager: DataManager):
    """Display all generated time slots for each day."""
    all_slots = data_manager.list_all_generated_slots()

    print("\n" + "=" * 50)
    print("           GENERATED TIME SLOTS")
    print("=" * 50)

    if not all_slots:
        print("\nNo time slots generated.\n")
        return

    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for day in days_order:
        if day not in all_slots:
            continue
        
        slots = all_slots[day]
        print(f"\n{day}: ({len(slots)} slots)")
        
        # Display in rows of 8
        for i in range(0, len(slots), 8):
            row = slots[i:i+8]
            print(f"  {', '.join(row)}")

    print("\n" + "=" * 50 + "\n")


def selectDay() -> str:
    """Prompt user to select a day of the week."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    print("\nSelect a day:")
    for idx, day in enumerate(days, 1):
        print(f"  {idx}. {day}")
    print("  0. Cancel")
    
    while True:
        choice = input("Enter choice: ").strip()
        if choice == "0":
            return ""
        if choice.isdigit() and 1 <= int(choice) <= 7:
            return days[int(choice) - 1]
        print("Invalid choice. Please enter 1-7 or 0 to cancel.")


def getIntervalInput() -> dict:
    """Prompt user for interval details and return as dict."""
    print("\nEnter interval details:")
    
    # Start time
    while True:
        start = input("  Start time (HH:MM, e.g. 08:00): ").strip()
        if len(start) == 5 and start[2] == ":" and start[:2].isdigit() and start[3:].isdigit():
            break
        print("  Invalid format. Use HH:MM (e.g. 08:00)")
    
    # End time
    while True:
        end = input("  End time (HH:MM, e.g. 17:00): ").strip()
        if len(end) == 5 and end[2] == ":" and end[:2].isdigit() and end[3:].isdigit():
            break
        print("  Invalid format. Use HH:MM (e.g. 17:00)")
    
    # Spacing
    while True:
        spacing_str = input("  Spacing in minutes (e.g. 60): ").strip()
        if spacing_str.isdigit() and int(spacing_str) > 0:
            spacing = int(spacing_str)
            break
        print("  Invalid spacing. Enter a positive integer.")
    
    # Optional fields
    professors_str = input("  Professors (comma-separated, or leave empty): ").strip()
    professors = [p.strip() for p in professors_str.split(",") if p.strip()] if professors_str else []
    
    labs_str = input("  Labs (comma-separated, or leave empty): ").strip()
    labs = [l.strip() for l in labs_str.split(",") if l.strip()] if labs_str else []
    
    courses_str = input("  Courses (comma-separated, or leave empty): ").strip()
    courses = [c.strip() for c in courses_str.split(",") if c.strip()] if courses_str else []
    
    interval_dict = {
        "start": start,
        "end": end,
        "spacing": spacing
    }
    
    if professors:
        interval_dict["professors"] = professors
    if labs:
        interval_dict["labs"] = labs
    if courses:
        interval_dict["courses"] = courses
    
    return interval_dict


def addInterval(data_manager: DataManager):
    """Add a new time interval."""
    day = selectDay()
    if not day:
        print("Cancelled.")
        return
    
    interval_dict = getIntervalInput()
    
    try:
        data_manager.add_time_interval(day, interval_dict)
        print(f"\n✓ Interval added to {day} successfully!")
    except ValueError as e:
        print(f"\n✗ Error adding interval: {e}")


def editInterval(data_manager: DataManager):
    """Edit an existing time interval."""
    day = selectDay()
    if not day:
        print("Cancelled.")
        return
    
    intervals = data_manager.get_time_intervals_for_day(day)
    
    if not intervals:
        print(f"\nNo intervals found for {day}.")
        return
    
    print(f"\nIntervals for {day}:")
    for idx, iv in enumerate(intervals):
        print(f"  [{idx}] {iv['start']} - {iv['end']} (every {iv['spacing']} min)")
    
    while True:
        idx_str = input("Enter interval index to edit (or 'c' to cancel): ").strip()
        if idx_str.lower() == 'c':
            print("Cancelled.")
            return
        if idx_str.isdigit() and 0 <= int(idx_str) < len(intervals):
            idx = int(idx_str)
            break
        print(f"Invalid index. Enter 0-{len(intervals)-1} or 'c' to cancel.")
    
    print(f"\nEditing interval [{idx}]: {intervals[idx]['start']} - {intervals[idx]['end']}")
    new_interval = getIntervalInput()
    
    try:
        data_manager.edit_time_interval(day, idx, new_interval)
        print(f"\n✓ Interval updated successfully!")
    except ValueError as e:
        print(f"\n✗ Error updating interval: {e}")


def removeInterval(data_manager: DataManager):
    """Remove a time interval."""
    day = selectDay()
    if not day:
        print("Cancelled.")
        return
    
    intervals = data_manager.get_time_intervals_for_day(day)
    
    if not intervals:
        print(f"\nNo intervals found for {day}.")
        return
    
    print(f"\nIntervals for {day}:")
    for idx, iv in enumerate(intervals):
        print(f"  [{idx}] {iv['start']} - {iv['end']} (every {iv['spacing']} min)")
    
    while True:
        idx_str = input("Enter interval index to remove (or 'c' to cancel): ").strip()
        if idx_str.lower() == 'c':
            print("Cancelled.")
            return
        if idx_str.isdigit() and 0 <= int(idx_str) < len(intervals):
            idx = int(idx_str)
            break
        print(f"Invalid index. Enter 0-{len(intervals)-1} or 'c' to cancel.")
    
    # Confirm deletion
    iv = intervals[idx]
    confirm = input(f"Remove interval {iv['start']} - {iv['end']}? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return
    
    try:
        data_manager.remove_time_interval(day, idx)
        print(f"\n✓ Interval removed successfully!")
    except (KeyError, IndexError) as e:
        print(f"\n✗ Error removing interval: {e}")


def mainTimeSlotController(data_manager: DataManager):
    """Main controller for time slot CLI menu."""
    while True:
        print("\n--- Time Slot Configuration ---")
        print("1. View All Time Intervals")
        print("2. View Generated Slots")
        print("3. Add Interval")
        print("4. Edit Interval")
        print("5. Remove Interval")
        print("0. Back")
        
        choice = input("Select: ").strip()
        
        if choice == "0":
            return
        elif choice == "1":
            displayTimeSlots(data_manager)
        elif choice == "2":
            displayGeneratedSlots(data_manager)
        elif choice == "3":
            addInterval(data_manager)
        elif choice == "4":
            editInterval(data_manager)
        elif choice == "5":
            removeInterval(data_manager)
        else:
            print("Invalid option. Please try again.")
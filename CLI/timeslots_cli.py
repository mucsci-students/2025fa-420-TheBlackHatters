# cli.py
from Models.Timeslots_model import TimeSlotModel


# Timeslot Controller.
def mainTimeslotController(timeslots):
    # times = timeslots.get("times")
    model = TimeSlotModel(timeslots)

    while True:
        print("\nAvailable days:", ", ".join(model.times.keys()))
        day = input("Enter a day to edit (or 'q' to quit): ").upper().strip()

        if day == "Q":
            break
        if day not in model.times:
            print("Invalid day.")
            continue

        while True:
            slots = model.list_slots(day)
            print(f"\nCurrent time slots for {day}:")
            for i, slot in enumerate(slots):
                print(
                    f"  [{i}] start={slot['start']} spacing={slot['spacing']} end={slot['end']}"
                )

            print("\nOptions:\n 1) Add slot\n 2) Edit slot\n 3) Delete slot\n 0) Back")
            choice = input("Select option: ").strip()

            if choice == "1":
                start = input("Start time (HH:MM): ").strip()
                end = input("End time (HH:MM): ").strip()
                spacing_in = input("Spacing (minutes): ").strip()
                try:
                    spacing = int(spacing_in)
                except ValueError:
                    print("Spacing must be an integer number of minutes.")
                    continue

                try:
                    model.add_slot(day, start, spacing, end)
                    print("Slot added.")
                except ValueError as e:
                    print("Error:", e)

            elif choice == "2":
                if not slots:
                    print("No slots available to edit for this day.")
                    continue

                try:
                    idx = int(input("Index of slot to edit: ").strip())
                except ValueError:
                    print("Please enter a valid integer index.")
                    continue

                if not (0 <= idx < len(slots)):
                    print("Invalid index!")
                    continue
                slot = slots[idx]

                new_start = input(f"Start ({slot['start']}): ").strip() or None
                new_end = input(f"End ({slot['end']}): ").strip() or None
                new_spacing_in = input(f"Spacing ({slot['spacing']}): ").strip()
                new_spacing = int(new_spacing_in) if new_spacing_in else None

                try:
                    model.edit_slot(
                        day, idx, start=new_start, spacing=new_spacing, end=new_end
                    )
                    print("Slot updated.")
                except Exception as e:
                    print("Error:", e)

            elif choice == "3":
                try:
                    idx = int(input("Index of slot to delete: ").strip())
                except ValueError:
                    print("Please enter a valid integer index.")
                    continue

                try:
                    removed = model.delete_slot(day, idx)
                    print("Deleted slot:", removed)
                except IndexError as e:
                    print("Error:", e)

            elif choice == "0":
                break

            else:
                print("Invalid choice.")

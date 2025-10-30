# File: CLI/test_cli.py
# Author: Fletcher Burton
# Created: October 2025
#
# Provides an interactive CLI for running project tests with pytest.

import subprocess
import os

def run_tests_cli():
    """Interactive test runner for Models and Controllers."""
    os.system("clear" if os.name != "nt" else "cls")
    print("=== Test Runner CLI ===\n")
    print("Choose a category of tests to run:\n")
    print("1. Run Model_tests")
    print("2. Run Controller Tests")
    print("0. Exit\n")

    choice = input("Select option: ").strip()

    if choice == "0":
        return

    # --- Model_tests ---
    elif choice == "1":
        print("\nSelect which Model test to run:")
        print("1. All Models")
        print("2. Room Model")
        print("3. Lab Model")
        print("4. Faculty Model")
        print("5. Course Model")
        print("6. Data Manager\n")
        sub_choice = input("Select: ").strip()

        test_map = {
            "1": "tests/Model_tests",
            "2": "tests/Model_tests/test_room_model.py",
            "3": "tests/Model_tests/test_labs_model.py",
            "4": "tests/Model_tests/test_faculty_model.py",
            "5": "tests/Model_tests/test_course_model.py",
            "6": "tests/Model_tests/test_data_manager.py"
        }

        test_path = test_map.get(sub_choice)
        if not test_path:
            print("Invalid choice.")
            return

        print(f"\nRunning: {test_path}\n")
        subprocess.run(["pytest", "-v", test_path])

    # --- Controller Tests ---
    elif choice == "2":
        print("\nRunning Controller Tests...\n")
        subprocess.run(["pytest", "-v", "tests/test_controller.py"])

    else:
        print("Invalid option. Returning to main menu.")
        return

    input("\nPress Enter to return to the main menu...")
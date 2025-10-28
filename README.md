# TheBlackHatters

Authors:

-   Liam Delaney
-   Nicholas DiPace
-   Bhagi Dhakal
-   Fletcher Burton
-   Nick Filemyr
-   Basu Subedi
-   Ben Richardson

# Course Constraint Scheduler Companion

This is a tool built for the Course Constraint Scheduler that allows you to run the Scheduler, create and modify configuration files, and manage output files completely in the command line or a graphical interface.

## Installation Instructions

Must be running at least Python version 3.12
Must have at least UV version 0.8.22

**Installation**

1. Clone the repository with `git clone <url>` to download the project. This will be your working directory.
2. Run `uv sync` to download the requirements and create virtual environment.
3. Run `uv run --python 3.12 -m CLI.main` to start the program.

## Design Patterns

**1: Model View Controller (MVC)**

This project uses the MVC pattern to create the GUI for this project. The model code can be found inside the `Models` folder, the views can be found inside the `Views` folder, and the controllers can be found inside the `Controller` folder.

The Problem: We wanted to write maintainable code with good organization, and also build and test components easily so we could divide our tasks among team members.

The Solution: The MVC model fixed our problem. With this method we modularized our project into three sections. This made development easier and faster as teammates could work on diffrent modules. This method also forced use to organization our code.

**2: Singleton**

This project uses the Singleton design pattern to implement a data manager. The code can be found inside `Models/Data_manager.py`, and we use the DataManager in the `Controller/main_controller.py `file.

The Problem: Opening the same file from multiple points in the program slowed the system down since we were reading and parsing the same file multiple times and loading the same data repeatedly.

The Solution: With the Singleton pattern, we created a DataManager class to open, save, and read the file only once. Now, when the user imports a file, it is handled by a single DataManager instance. When other parts of the program need the imported data, they request it from the DataManager, which provides the same data consistently.

**3: Decorator**

This project uses the Decorator design pattern conceptually through the @pytest.fixture decorator in our test suite for the data manager. The code can be found inside `tests/Model_tests/test_data_manager.py`.

The Problem: We needed a flexible way to add reusable setup data and configuration for multiple test functions without duplicating the same initialization code multiple times.

The Solution: The @pytest.fixture decorator solved this problem by dynamically attaching shared setup data to each test that requires it. This allowed us to assign test functions with extra responsibilities such as like providing a sample configuration without modifying the tests themselves.

**4: Observer**

This project uses the Observer design pattern throughout the `Views` folder to update the views whenever changes are made to the configuration file. Specific code can be found inside `Views/main_view.py`, particularly in the refresh method. Additional code can also be found inside `Controller/main_controller.py`.

The Problem: When the user added or modified labs, rooms, courses, ect, we needed the views to update automatically. It was difficult to manually refresh or update an already existing view every time data changed.

The Solution: With the Observer design pattern, we created a refresh method that is called whenever we add, modify, or remove items in the view. This method recreates the view with the updated data, ensuring the interface is always uptodate with the latest configuration data.

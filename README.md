# TheBlackHatters
Team Members:
- Liam Delaney
- Nicholas DiPace
- Bhagi Dhakal
- Fletcher Burton
- Nick Filemyr
- Basu Subedi
- Ben Richardson

# Course Constraint Scheduler Companion
This is a tool built for the Course Constraint Scheduler that allows you to create configuration files and run the scheduler completely in the command line.

## Installation Instructions
Must be running at least Python version 3.12
Must have latest version of UV

**Installation**
1. Clone the repository with `git clone <url>` to download the project. This will be your working directory.
2. Link the folder in Visual Studio Code and open terminal or just open a terminal in the directory. (Powershell if using Windows)<br>
PS. Powershell script execution will not work unless you either set the execution policy to bypass with `Set-ExecutionPolicy Bypass` or within your working terminal (must be run in admin) run `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process` to temporarily allow scripts. The latter is recommended for security reasons.
3. Run `uv sync` to download requirements and create virtual environment.
4. Run `uv run --python 3.12 -m CLI.main` to start the program.

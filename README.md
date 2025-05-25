# Student Report Form Generator (assessment_school.py)

## Description

This project, `assessment_school.py`, is an enhanced Python script designed to generate student report forms. It interactively collects student details (name, grade, and a performance rating), displays a formatted report, logs key information to a CSV file for record-keeping, and offers an option to save the individual report as a `.txt` file. The script is built with an object-oriented approach for better organization and maintainability.

## Features

* **Interactive Data Entry:** Prompts for student's name, grade, and a 1-5 performance rating with input validation.
* **Console Report Display:** Shows a clearly formatted student report directly in the console.
* **CSV Logging:** Automatically appends key details of each generated report (timestamp, name, grade, rating, description) to a `student_records.csv` file. Creates the file with headers if it doesn't exist.
* **Optional `.txt` File Saving:** Prompts the user to save the generated report to an individual text file (e.g., `Jane_Doe_report_20250525.txt`). Filenames are sanitized for safety.
* **Object-Oriented Design:** The underlying code is structured using classes for better organization and encapsulation of functionalities.

## Files in the Project / Generated

* `assessment_school.py`: The main Python script containing the program logic.
* `README.md`: This documentation file.
* `student_records.csv` (Generated): A CSV file where student report data is logged. Created/appended by the script.
* `*_report_YYYYMMDD.txt` (Generated): Individual student reports, optionally saved by the user (e.g., `Jane_Doe_report_20250525.txt`).

## Requirements

* Python 3.x (Standard library only, no external packages needed beyond what's included with Python)

## How to Run

1.  Ensure you have Python 3 installed on your system.
2.  Save the Python code into a file named `assessment_school.py`.
3.  Open a terminal or command prompt.
4.  Navigate to the directory where you saved the file.
5.  Run the script using the following command:

    ```bash
    python assessment_school.py
    ```

6.  The script will then:
    * Prompt you to enter the student's details (name, grade, performance rating).
    * Display the formatted student report on the console.
    * Automatically log the report details to `student_records.csv`.
    * Ask if you want to save the report to a `.txt` file.

## Example Usage

Here's what a typical interaction with the script might look like:
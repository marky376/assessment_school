# assessment_analysis.py
# Student Report Form - Ideal Object-Oriented Refactor

import datetime
import re
import csv
import os # For os.path.isfile and os.path.getsize

class Student:
    """
    Represents a student, encapsulating their details and performance information.
    """
    
    PERFORMANCE_DESCRIPTIONS: dict[int, str] = {
        1: "Needs significant improvement",
        2: "Below average",
        3: "Average",
        4: "Good",
        5: "Excellent"
    }
    
    def __init__(self, name: str, grade: str, performance_rating: int):
        """
        Initializes a Student object.

        Args:
            name (str): The student's name.
            grade (str): The student's grade (e.g., 'A', 'B').
            performance_rating (int): The student's performance rating (1-5).
        """
        self.name: str = name
        self.grade: str = grade
        self.performance_rating: int = performance_rating
    
    @property
    def performance_description(self) -> str:
        """Returns the textual description of the student's performance rating."""
        return self.PERFORMANCE_DESCRIPTIONS.get(self.performance_rating, "Unknown Rating")
    
    @classmethod
    def get_student_details_from_user(cls) -> 'Student':
        """
        Collects student details (name, grade, rating) via user input
        and returns a new Student object.
        Includes input validation for the performance rating.
        """
        name: str = input("Enter the student's name: ").strip()
        grade: str = input("Enter the student's grade (e.g., A, B, C): ").strip().upper()
        
        performance_rating: int = 0
        while True:
            try:
                performance_rating_input = input("Rate the student's performance (1-5): ")
                performance_rating = int(performance_rating_input)
                if 1 <= performance_rating <= 5:
                    break
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        return cls(name, grade, performance_rating)


class Report:
    """
    Handles the generation, display, and text file saving of a student's report.
    """
    
    def __init__(self, student: Student):
        """
        Initializes a Report object for a given student.

        Args:
            student (Student): The Student object for whom the report is generated.
        """
        self.student: Student = student
        self.report_content: str = self._generate_report_content()
    
    def _generate_report_content(self) -> str:
        """Generates the formatted multi-line report string."""
        # This format must be identical to the original script's output
        return f"""
    ===========================
    STUDENT REPORT FORM
    ===========================
    Name: {self.student.name}
    Grade: {self.student.grade}
    Performance Rating: {self.student.performance_rating} - {self.student.performance_description}
    ===========================
    """
    
    def display_on_console(self):
        """Prints the generated report to the console."""
        print(self.report_content)
    
    def save_to_textfile(self):
        """
        Asks the user if they want to save the report to a .txt file.
        If yes, saves the report using a sanitized filename and provides feedback.
        """
        while True:
            save_choice = input("Save report as a text file? (yes/no): ").strip().lower()
            if save_choice in ['yes', 'y', 'no', 'n']:
                break
            print("Please enter 'yes' or 'no' (or 'y'/'n').")
        
        if save_choice in ['yes', 'y']:
            safe_filename_name_part: str = Report._sanitize_filename_component(self.student.name)
            current_date_str: str = datetime.datetime.now().strftime("%Y%m%d")
            txt_filename: str = f"{safe_filename_name_part}_report_{current_date_str}.txt"
            
            try:
                with open(txt_filename, 'w', encoding='utf-8') as file:
                    file.write(self.report_content)
                print(f"Report saved as {txt_filename}!")
            except IOError as e:
                print(f"Sorry, couldn't save the text file. An I/O error occurred: {str(e)}")
            except Exception as e:
                print(f"Sorry, an unexpected error occurred while trying to save the text file: {str(e)}")
        else:
            print("Text report not saved.")
    
    @staticmethod
    def _sanitize_filename_component(name: str) -> str:
        """
        Sanitizes a name string to make it safe for use as a filename component.
        (Utility function, consistent with previous ideal rewrites)
        """
        name = name.strip() 
        if not name:       
            return "Unnamed_Student"
        name = re.sub(r'\s+', '_', name) # Replace sequences of whitespace with a single underscore
        name = re.sub(r'[^\w-]', '', name) # Remove non (alphanumeric or underscore or hyphen)
        if not name: 
            return "Unnamed_Student"
        return name


class CSVLogger:
    """
    Handles logging student report data to a CSV file.
    """
    
    CSV_FILENAME: str = "student_records.csv"
    FIELDS: list[str] = ["Timestamp", "Student Name", "Grade", "Performance Rating", "Performance Description"]
    
    @classmethod
    def log_entry(cls, student: Student):
        """
        Logs the provided student's details to the CSV file.
        Creates the file with headers if it doesn't exist or is empty.

        Args:
            student (Student): The Student object whose data will be logged.
        """
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_row: list = [
            timestamp, 
            student.name, 
            student.grade, 
            student.performance_rating, 
            student.performance_description
        ]
        
        try:
            header_needed = False
            if not os.path.isfile(cls.CSV_FILENAME):
                header_needed = True
            else:
                # File exists, check if it's empty to decide if header is needed
                if os.path.getsize(cls.CSV_FILENAME) == 0:
                    header_needed = True
                    
            with open(cls.CSV_FILENAME, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                if header_needed:
                    writer.writerow(cls.FIELDS)
                writer.writerow(data_row)
                # print("Data logged to CSV successfully.") # Optional success message
        except IOError as e:
            print(f"Error logging to CSV file (I/O): {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred while logging to CSV: {str(e)}")


def main():
    """
    Main function to orchestrate the student report generation, display,
    CSV logging, and .txt file saving process using OOP principles.
    """
    print("Welcome to the Student Report Form Generator!")
    
    # Get student details and create Student object
    student: Student = Student.get_student_details_from_user()
    
    # Create Report object, (report content is generated on init) and display it
    report_document: Report = Report(student)
    report_document.display_on_console()
    
    # Log student data to CSV using CSVLogger class method
    CSVLogger.log_entry(student)
    
    # Offer to save the report to a .txt file using Report's method
    report_document.save_to_textfile()


if __name__ == "__main__":
    main()

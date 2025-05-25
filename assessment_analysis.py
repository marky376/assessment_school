# assessment_school.py
# Student Report Form - Object-Oriented Refactoring with CSV Logging

import datetime
import re
import csv
import os

class Student:
    """Class to represent a student and their performance data."""
    
    PERFORMANCE_DESCRIPTIONS = {
        1: "Needs significant improvement",
        2: "Below average",
        3: "Average",
        4: "Good",
        5: "Excellent"
    }
    
    def __init__(self, name, grade, performance_rating):
        self.name = name
        self.grade = grade
        self.performance_rating = performance_rating
    
    @property
    def performance_description(self):
        """Returns the text description of the performance rating."""
        return self.PERFORMANCE_DESCRIPTIONS.get(self.performance_rating, "Unknown Rating")
    
    @classmethod
    def get_student_details_from_user(cls):
        """Collects student details from user input and returns a Student object."""
        name = input("Enter the student's name: ").strip()
        grade = input("Enter the student's grade (e.g., A, B, C): ").strip().upper()
        
        while True:
            try:
                performance_rating = int(input("Rate the student's performance (1-5): "))
                if 1 <= performance_rating <= 5:
                    break
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        return cls(name, grade, performance_rating)


class Report:
    """Class to handle report generation, display, and saving to text file."""
    
    def __init__(self, student):
        self.student = student
        self.report_content = self._generate_report_content()
    
    def _generate_report_content(self):
        """Generates the formatted report string."""
        return f"""
    ===========================
    STUDENT REPORT FORM
    ===========================
    Name: {self.student.name}
    Grade: {self.student.grade}
    Performance Rating: {self.student.performance_rating} - {self.student.performance_description}
    ===========================
    """
    
    def display(self):
        """Prints the report to the console."""
        print(self.report_content)
    
    def save_to_txt(self):
        """Asks the user if they want to save the report and saves it if requested."""
        while True:
            save_choice = input("Save report as a text file? (yes/no): ").strip().lower()
            if save_choice in ['yes', 'y', 'no', 'n']:
                break
            print("Please enter 'yes' or 'no' (or 'y'/'n').")
        
        if save_choice in ['yes', 'y']:
            safe_filename_name_part = self._sanitize_filename_component(self.student.name)
            current_date_str = datetime.datetime.now().strftime("%Y%m%d")
            txt_filename = f"{safe_filename_name_part}_report_{current_date_str}.txt"
            
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
    def _sanitize_filename_component(name):
        """
        Sanitizes a name string to make it safe for use as a filename component.
        """
        name = name.strip() 
        if not name:       
            return "Unnamed_Student"
        # Replace sequences of one or more whitespace characters with a single underscore
        name = re.sub(r'\s+', '_', name)
        # Remove any character that is not a word character (alphanumeric or underscore) or a hyphen
        name = re.sub(r'[^\w-]', '', name)
        if not name: # If name is empty after sanitization (e.g., was "!!!")
            return "Unnamed_Student"
        return name


class CSVLogger:
    """Class to handle logging student data to CSV file."""
    
    CSV_FILENAME = "student_records.csv"
    FIELDS = ["Timestamp", "Student Name", "Grade", "Performance Rating", "Performance Description"]
    
    @classmethod
    def log_student(cls, student):
        """Logs student report details to student_records.csv."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_row = [timestamp, student.name, student.grade, student.performance_rating, student.performance_description]
        
        try:
            header_needed = False
            if not os.path.isfile(cls.CSV_FILENAME): # Corrected from os.path.exists to os.path.isfile
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
                # Optional: print("Data logged to CSV successfully.")
        except IOError as e:
            print(f"Error logging to CSV file (I/O): {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred while logging to CSV: {str(e)}")


def main():
    """Main function to run the student report generator."""
    print("Welcome to the Student Report Form Generator!")
    
    # Get student details and create Student object
    student = Student.get_student_details_from_user()
    
    # Create and display the report
    report = Report(student)
    report.display()
    
    # Log student data to CSV
    CSVLogger.log_student(student)
    
    # Offer to save the report to a .txt file
    report.save_to_txt()


if __name__ == "__main__":
    main()
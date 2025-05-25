# assessment_analysis.py (or your chosen script name)
# This version incorporates the @DA model's OOP refactoring changes
# on top of the previous ideal rewrite (which had .txt saving and CSV logging).

import datetime
import re  # For filename sanitization
import csv # For CSV writing
import os  # For os.path.isfile and os.path.getsize

# --- Utility functions (assumed by @DA model to be existing/retained) ---
def sanitize_filename_component(name: str) -> str:
    """
    Sanitizes a name string to make it safe for use as a filename component.
    - Strips leading/trailing whitespace.
    - If the stripped name is empty, returns "Unnamed_Student".
    - Replaces sequences of whitespace characters with a single underscore.
    - Removes any characters that are not alphanumeric, underscores, or hyphens.
    - If the name becomes empty after full sanitization, it defaults to "Unnamed_Student".
    """
    name = name.strip() 
    if not name:       
        return "Unnamed_Student"
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'[^\w-]', '', name)
    if not name:
        return "Unnamed_Student"
    return name

def get_student_details(): # @DA's main calls this as a standalone function
    """Collects student details (name, grade, performance rating)."""
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
    
    return name, grade, performance_rating

# --- @DA Model's Class Definitions ---
class Student:
    """Represents a student with their details and performance information."""
    PERFORMANCE_MAP = {
        1: "Needs significant improvement",
        2: "Below average",
        3: "Average",
        4: "Good",
        5: "Excellent"
    }
    
    def __init__(self, name: str, grade: str, performance_rating: int):
        self.name = name
        self.grade = grade
        self.performance_rating = performance_rating
    
    def get_performance_description(self) -> str:
        """Returns the performance description based on the rating."""
        return self.PERFORMANCE_MAP.get(self.performance_rating, "Unknown Rating")

class Report:
    """Handles generating, displaying, and saving student reports."""
    def __init__(self, student: Student):
        self.student = student
        # Generate report string upon initialization
        self.report_string = self._generate_report_string() 
    
    def _generate_report_string(self) -> str:
        """Generates the formatted report string (internal helper)."""
        description = self.student.get_performance_description()
        # This format should be identical to the original generate_report function's output
        return f"""
    ===========================
    STUDENT REPORT FORM
    ===========================
    Name: {self.student.name}
    Grade: {self.student.grade}
    Performance Rating: {self.student.performance_rating} - {description}
    ===========================
    """
    
    def display(self):
        """Displays the report to the console."""
        print(self.report_string)
    
    def save_to_txt(self):
        """
        Asks the user if they want to save the report as .txt and saves it if requested.
        Uses the existing sanitization logic and filename format.
        """
        while True:
            save_choice = input("Save report as a text file? (yes/no): ").strip().lower()
            if save_choice in ['yes', 'y', 'no', 'n']:
                break
            print("Please enter 'yes' or 'no' (or 'y'/'n').")
        
        if save_choice in ['yes', 'y']:
            # Calls the standalone sanitize_filename_component function
            safe_filename_name_part = sanitize_filename_component(self.student.name)
            current_date_str = datetime.datetime.now().strftime("%Y%m%d") # Date format for .txt
            txt_filename = f"{safe_filename_name_part}_report_{current_date_str}.txt"
            
            try:
                with open(txt_filename, 'w', encoding='utf-8') as file:
                    file.write(self.report_string)
                print(f"Report saved as {txt_filename}!")
            except IOError as e: # Preserved error handling
                print(f"Sorry, couldn't save the text file. An I/O error occurred: {str(e)}")
            except Exception as e: 
                print(f"Sorry, an unexpected error occurred while trying to save the text file: {str(e)}")
        else:
            print("Text report not saved.")

class CSVLogger:
    """Handles logging student data to a CSV file."""
    CSV_FILENAME = "student_records.csv" # Class attribute for filename
    FIELDS = ["Timestamp", "Student Name", "Grade", "Performance Rating", "Performance Description"] # Class attribute for header
    
    def log_student(self, student: Student):
        """Logs the student's data to the CSV file, adding headers if needed."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        performance_desc = student.get_performance_description()
        data_row = [timestamp, student.name, student.grade, student.performance_rating, performance_desc]
        
        try:
            header_needed = False
            if not os.path.isfile(self.CSV_FILENAME):
                header_needed = True
            else:
                # File exists, check if it's empty to decide if header is needed
                # This improved header logic was from the ideal rewrite of CSV task
                if os.path.getsize(self.CSV_FILENAME) == 0:
                    header_needed = True
                    
            with open(self.CSV_FILENAME, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                if header_needed:
                    writer.writerow(self.FIELDS)
                writer.writerow(data_row)
                # Optional: print("Data logged to CSV successfully.")
        except IOError as e: # Preserved error handling
            print(f"Error logging to CSV file (I/O): {str(e)}")
        except Exception as e: 
            print(f"An unexpected error occurred while logging to CSV: {str(e)}")

# --- @DA Model's main() Function ---
def main():
    """Main function to run the student report generator."""
    print("Welcome to the Student Report Form Generator!")
    
    # Get student details (using standalone function)
    name, grade, performance_rating = get_student_details()
    student = Student(name, grade, performance_rating) # Create Student object
    
    # Create Report object, generate and display the report
    report_obj = Report(student) # Renamed 'report' to 'report_obj' to avoid conflict if old report variable was used
    report_obj.display()
    
    # Log student data to CSV using CSVLogger
    logger = CSVLogger()
    logger.log_student(student)
    
    # Offer to save the report to a .txt file using Report's save method
    report_obj.save_to_txt()

if __name__ == "__main__":
    main()
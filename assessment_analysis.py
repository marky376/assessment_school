# assessment_school.py
# Student Report Form - Ideal Rewrite with CSV Logging

import datetime
import re  # For filename sanitization (from previous .txt save feature)
import csv # For CSV writing
import os  # For os.path.isfile and os.path.getsize

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
    # Replace sequences of one or more whitespace characters with a single underscore
    name = re.sub(r'\s+', '_', name)
    # Remove any character that is not a word character (alphanumeric or underscore) or a hyphen
    name = re.sub(r'[^\w-]', '', name)
    if not name: # If name is empty after sanitization (e.g., was "!!!")
        return "Unnamed_Student"
    return name

def get_student_details():
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

def generate_report(name: str, grade: str, performance_rating: int) -> tuple[str, str]:
    """
    Generates a formatted student report string and the performance description text.
    Returns a tuple: (report_string, performance_description_text)
    """
    performance_description_map = {
        1: "Needs significant improvement",
        2: "Below average",
        3: "Average",
        4: "Good",
        5: "Excellent"
    }
    description_text = performance_description_map.get(performance_rating, "Unknown Rating")
    
    report_string = f"""
    ===========================
    STUDENT REPORT FORM
    ===========================
    Name: {name}
    Grade: {grade}
    Performance Rating: {performance_rating} - {description_text}
    ===========================
    """
    return report_string, description_text

def save_report_to_txt(student_name: str, report_content: str):
    """
    Asks the user if they want to save the report (as .txt) and saves it if requested.
    The student_name is sanitized before being used in the filename.
    (This function was from the previous ideal rewrite for .txt saving)
    """
    while True:
        save_choice = input("Save report as a text file? (yes/no): ").strip().lower()
        if save_choice in ['yes', 'y', 'no', 'n']:
            break
        print("Please enter 'yes' or 'no' (or 'y'/'n').")
    
    if save_choice in ['yes', 'y']:
        safe_filename_name_part = sanitize_filename_component(student_name)
        current_date_str = datetime.datetime.now().strftime("%Y%m%d") # Date format for .txt
        txt_filename = f"{safe_filename_name_part}_report_{current_date_str}.txt"
        
        try:
            with open(txt_filename, 'w', encoding='utf-8') as file:
                file.write(report_content)
            print(f"Report saved as {txt_filename}!")
        except IOError as e:
            print(f"Sorry, couldn't save the text file. An I/O error occurred: {str(e)}")
        except Exception as e: # Catch any other unexpected errors
            print(f"Sorry, an unexpected error occurred while trying to save the text file: {str(e)}")
    else:
        print("Text report not saved.")

def log_to_csv(name: str, grade: str, performance_rating: int, performance_desc: str):
    """
    Logs student report details to student_records.csv.
    Creates the file with headers if it doesn't exist or is empty, otherwise appends data.
    """
    csv_filename = "student_records.csv"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Specific format for CSV
    
    fields = ["Timestamp", "Student Name", "Grade", "Performance Rating", "Performance Description"]
    data_row = [timestamp, name, grade, performance_rating, performance_desc]
    
    try:
        header_needed = False
        if not os.path.isfile(csv_filename):
            header_needed = True
        else:
            # File exists, check if it's empty to decide if header is needed
            if os.path.getsize(csv_filename) == 0:
                header_needed = True
                
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if header_needed:
                writer.writerow(fields)
            writer.writerow(data_row)
            # Optional: print("Data logged to CSV successfully.")
    except IOError as e: # More specific for file issues
        print(f"Error logging to CSV file (I/O): {str(e)}")
    except Exception as e: # Catch any other unexpected errors
        print(f"An unexpected error occurred while logging to CSV: {str(e)}")

def main():
    """Main function to run the student report generator."""
    print("Welcome to the Student Report Form Generator!")
    
    # Get student details
    name, grade, performance_rating = get_student_details()
    
    # Generate the report string and get the performance description separately
    report_string, performance_description_for_log = generate_report(name, grade, performance_rating)
    
    # Print the report to the console
    print(report_string)
    
    # Log student data to CSV
    log_to_csv(name, grade, performance_rating, performance_description_for_log)
    
    # Offer to save the report to a .txt file (existing functionality)
    save_report_to_txt(name, report_string)

if __name__ == "__main__":
    main()
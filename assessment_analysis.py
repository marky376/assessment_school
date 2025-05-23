# assessment_analysis.py (or your chosen script name)
# This version incorporates the @DA model's changes for CSV logging
# on top of the previous ideal rewrite (which had .txt saving and sanitization).

import datetime
import re  # From previous ideal rewrite (for TXT filename sanitization)
import csv # Added by @DA model for CSV writing
import os  # Added by @DA model for file existence checks

def sanitize_filename_component(name: str) -> str:
    """
    Sanitizes a name string to make it safe for use as a filename component.
    - Strips leading/trailing whitespace.
    - If the stripped name is empty, returns "Unnamed_Student".
    - Replaces sequences of whitespace characters with a single underscore.
    - Removes any characters that are not alphanumeric, underscores, or hyphens.
    - If the name becomes empty after full sanitization, it defaults to "Unnamed_Student".
    (This function was part of your previous ideal rewrite)
    """
    name = name.strip() 
    if not name:       
        return "Unnamed_Student"
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'[^\w-]', '', name)
    if not name:
        return "Unnamed_Student"
    return name

def get_student_details():
    """Collects student details and performance rating."""
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

def generate_report(name, grade, performance_rating):
    """Generates a formatted student report."""
    # This performance_description map is part of the original script logic
    # The @DA model re-created a similar map inside its version of main()
    # specifically for the CSV logging part.
    performance_description_map_for_report = {
        1: "Needs significant improvement",
        2: "Below average",
        3: "Average",
        4: "Good",
        5: "Excellent"
    }
    
    report = f"""
    ===========================
    STUDENT REPORT FORM
    ===========================
    Name: {name}
    Grade: {grade}
    Performance Rating: {performance_rating} - {performance_description_map_for_report[performance_rating]}
    ===========================
    """
    return report

def save_report(student_name: str, report_content: str):
    """
    Asks the user if they want to save the report (as .txt) and saves it if requested.
    The student_name is sanitized before being used in the filename.
    (This function was part of your previous ideal rewrite for .txt saving)
    """
    while True:
        save_choice_txt = input("Save report as a text file? (yes/no): ").strip().lower() # Changed variable name slightly
        if save_choice_txt in ['yes', 'y', 'no', 'n']:
            break
        print("Please enter 'yes' or 'no' (or 'y'/'n').")
    
    if save_choice_txt in ['yes', 'y']:
        safe_filename_name_part = sanitize_filename_component(student_name)
        current_date_str = datetime.datetime.now().strftime("%Y%m%d") # Used YYYYMMDD for .txt
        txt_filename = f"{safe_filename_name_part}_report_{current_date_str}.txt"
        
        try:
            with open(txt_filename, 'w', encoding='utf-8') as file:
                file.write(report_content)
            print(f"Report saved as {txt_filename}!")
        except IOError as e:
            print(f"Sorry, couldn't save the text file. An I/O error occurred: {str(e)}")
        except Exception as e:
            print(f"Sorry, an unexpected error occurred while trying to save the text file: {str(e)}")
    else:
        print("Text report not saved.")

# This is the main() function as modified by the @DA Model for CSV logging
def main():
    """Main function to run the student report generator."""
    print("Welcome to the Student Report Form Generator!")
    
    # Get student details
    name, grade, performance_rating = get_student_details()
    
    # Generate the report
    report = generate_report(name, grade, performance_rating)
    
    # Print the report to the console
    print(report)
    
    # Log details to student_records.csv (added functionality by @DA model)
    performance_description_map_for_csv = { # @DA re-created this map here
        1: "Needs significant improvement",
        2: "Below average",
        3: "Average",
        4: "Good",
        5: "Excellent"
    }
    desc = performance_description_map_for_csv[performance_rating] # desc for CSV
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Timestamp for CSV
    row = [timestamp, name, grade, performance_rating, desc]
    csv_filename = "student_records.csv"
    try:
        file_exists = os.path.exists(csv_filename)
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["Timestamp", "Student Name", "Grade", "Performance Rating", "Performance Description"])
            writer.writerow(row)
    except Exception as e:
        print(f"Error writing to CSV: {str(e)}") # CSV specific error
    
    # Offer to save the report (this calls your existing .txt save function)
    save_report(name, report)

if __name__ == "__main__":
    main()
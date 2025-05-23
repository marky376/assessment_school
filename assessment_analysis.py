# assessment_analysis.py (or your chosen script name)
# This version incorporates @Sonnet's changes for CSV logging
# on top of the previous ideal rewrite (which had .txt saving and sanitization).

import datetime
import re  # From previous ideal rewrite
import csv # Added by @Sonnet
import os.path # Added by @Sonnet

def sanitize_filename_component(name: str) -> str:
    """
    Sanitizes a name string to make it safe for use as a filename component.
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
    performance_description_map_for_report = {
        1: "Needs significant improvement",
        2: "Below average",
        3: "Average",
        4: "Good",
        5: "Excellent"
    }
    
    report_str = f"""
    ===========================
    STUDENT REPORT FORM
    ===========================
    Name: {name}
    Grade: {grade}
    Performance Rating: {performance_rating} - {performance_description_map_for_report[performance_rating]}
    ===========================
    """
    return report_str # Ensure it returns the string

def save_report(student_name: str, report_content: str): # For TXT files
    """
    Asks the user if they want to save the report (as .txt) and saves it if requested.
    (This function was part of your previous ideal rewrite for .txt saving)
    """
    while True:
        save_choice_txt = input("Save report as a text file? (yes/no): ").strip().lower()
        if save_choice_txt in ['yes', 'y', 'no', 'n']:
            break
        print("Please enter 'yes' or 'no' (or 'y'/'n').")
    
    if save_choice_txt in ['yes', 'y']:
        safe_filename_name_part = sanitize_filename_component(student_name)
        current_date_str = datetime.datetime.now().strftime("%Y%m%d")
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

# @Sonnet's new function for CSV logging
def log_to_csv(name, grade, performance_rating, performance_description_text_for_csv):
    """
    Logs student report details to a CSV file.
    Creates the file with headers if it doesn't exist, otherwise appends data.
    """
    csv_filename = "student_records.csv"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    fields = ["Timestamp", "Student Name", "Grade", "Performance Rating", "Performance Description"]
    data_row = [timestamp, name, grade, performance_rating, performance_description_text_for_csv]
    
    try:
        file_exists = os.path.isfile(csv_filename) 
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(fields)
            writer.writerow(data_row)
    except Exception as e:
        print(f"Error logging to CSV file: {str(e)}")

# @Sonnet's modified main() function
def main():
    """Main function to run the student report generator."""
    print("Welcome to the Student Report Form Generator!")
    
    name, grade, performance_rating = get_student_details()
    
    # Sonnet gets performance description in main for CSV logging
    performance_description_map_in_main = {
        1: "Needs significant improvement",
        2: "Below average",
        3: "Average",
        4: "Good",
        5: "Excellent"
    }
    actual_performance_description = performance_description_map_in_main[performance_rating]
    
    report = generate_report(name, grade, performance_rating) # Generate report string
    print(report) # Print report to console
    
    # Call to new CSV log function
    log_to_csv(name, grade, performance_rating, actual_performance_description) 
    
    # Call to existing TXT save function (from your previous ideal rewrite)
    save_report(name, report) 

if __name__ == "__main__":
    main()
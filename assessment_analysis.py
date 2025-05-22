# assessment_school.py
# Student Report Form - Ideal Rewrite

import datetime
import re # Imported for filename sanitization

def sanitize_filename_component(name: str) -> str:
    """
    Sanitizes a name string to make it safe for use as a filename component.
    - Strips leading/trailing whitespace.
    - If the stripped name is empty, returns "Unnamed_Student".
    - Replaces sequences of whitespace characters (e.g., spaces, tabs) with a single underscore.
    - Removes any characters that are not alphanumeric (letters, numbers), underscores, or hyphens.
      This helps prevent path traversal and issues with OS-reserved characters.
    - If the name becomes empty after full sanitization (e.g., if it contained only special characters),
      it defaults to "Unnamed_Student".
    """
    name = name.strip() # Remove leading/trailing whitespace
    if not name:       # Handle if name was initially empty or only whitespace
        return "Unnamed_Student"

    # Replace sequences of one or more whitespace characters with a single underscore
    name = re.sub(r'\s+', '_', name)
    
    # Remove any character that is not a word character (alphanumeric or underscore) or a hyphen.
    # \w typically matches [a-zA-Z0-9_].
    name = re.sub(r'[^\w-]', '', name)
    
    # If after all sanitization the name is empty (e.g., it was "!@#$" or similar)
    if not name:
        return "Unnamed_Student"
        
    return name

def get_student_details():
    """Collects student details and performance rating."""
    name = input("Enter the student's name: ").strip() # Name is stripped here
    grade = input("Enter the student's grade (e.g., A, B, C): ").strip().upper()
    
    # Validate performance rating
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
    performance_description = {
        1: "Needs significant improvement",
        2: "Below average",
        3: "Average",
        4: "Good",
        5: "Excellent"
    }
    
    # Sanitize name for display if needed, though for display it's usually fine as is.
    # For this report, we'll use the name as entered.
    report = f"""
    ===========================
    STUDENT REPORT FORM
    ===========================
    Name: {name}
    Grade: {grade}
    Performance Rating: {performance_rating} - {performance_description[performance_rating]}
    ===========================
    """
    return report

def save_report(student_name: str, report_content: str):
    """
    Asks the user if they want to save the report and saves it if requested.
    The student_name is sanitized before being used in the filename.
    """
    while True:
        save_choice = input("Save report? (yes/no): ").strip().lower()
        if save_choice in ['yes', 'y', 'no', 'n']:
            break
        print("Please enter 'yes' or 'no' (or 'y'/'n').") # Clarified prompt slightly
    
    if save_choice in ['yes', 'y']:
        # Sanitize the student's name for safe use in a filename
        safe_filename_name_part = sanitize_filename_component(student_name)
        
        # Get current date for the filename
        current_date_str = datetime.datetime.now().strftime("%Y%m%d")
        filename = f"{safe_filename_name_part}_report_{current_date_str}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as file: # Added encoding for broader compatibility
                file.write(report_content)
            print(f"Report saved as {filename}!")
        except IOError as e: # More specific exception for file I/O issues
            print(f"Sorry, couldn't save the file. An I/O error occurred: {str(e)}")
        except Exception as e: # Catch any other unexpected errors during saving
            print(f"Sorry, an unexpected error occurred while trying to save the file: {str(e)}")
    else:
        print("Report not saved.")

def main():
    """Main function to run the student report generator."""
    print("Welcome to the Student Report Form Generator!")
    
    # Get student details
    name, grade, performance_rating = get_student_details()
    
    # Generate the report
    report = generate_report(name, grade, performance_rating)
    
    # Print the report to the console
    print(report)
    
    # Offer to save the report
    save_report(name, report)

if __name__ == "__main__":
    main()
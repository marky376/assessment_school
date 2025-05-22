# assessment_analysis.py
# Student Report Form
import datetime

def get_student_details():
    """Collects student details and performance rating."""
    name = input("Enter the student's name: ").strip()
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

def save_report(name, report):
    """Asks user if they want to save the report and saves it if requested."""
    while True:
        save_choice = input("Save report? (yes/no): ").strip().lower()
        if save_choice in ['yes', 'y', 'no', 'n']:
            break
        print("Please enter 'yes' or 'no'.")
    
    if save_choice in ['yes', 'y']:
        # Format the filename: replace spaces with underscores and add date
        today = datetime.datetime.now().strftime("%Y%m%d")
        filename = f"{name.replace(' ', '_')}_report_{today}.txt"
        
        try:
            with open(filename, 'w') as file:
                file.write(report)
            print(f"Report saved as {filename}!")
        except Exception as e:
            print(f"Sorry, couldn't save the file: {str(e)}")
    else:
        print("Report not saved.")

def main():
    print("Welcome to the Student Report Form Generator!")
    name, grade, performance_rating = get_student_details()
    report = generate_report(name, grade, performance_rating)
    print(report)
    save_report(name, report)

if __name__ == "__main__":
    main()
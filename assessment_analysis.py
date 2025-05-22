# assessment_analysis.py
import datetime  # Added import for date handling
# ... existing code ...

def main():
    print("Welcome to the Student Report Form Generator!")
    name, grade, performance_rating = get_student_details()
    report = generate_report(name, grade, performance_rating)
    print(report)
    
    # Added code to handle report saving
    while True:
        save_choice = input("Save report? (yes/no): ").strip().lower()
        if save_choice in ['yes', 'y']:
            # Generate filename: Replace spaces with underscores and add date
            name_for_file = name.replace(" ", "_")
            today = datetime.date.today().strftime("%Y%m%d")
            filename = f"{name_for_file}_report_{today}.txt"
            
            try:
                with open(filename, 'w') as file:
                    file.write(report)
                print(f"Report saved as {filename}!")
                break
            except Exception as e:
                print(f"Sorry, couldn't save the file due to an error: {str(e)}")
                break
        elif save_choice in ['no', 'n']:
            print("Report not saved.")
            break
        else:
            print("Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()
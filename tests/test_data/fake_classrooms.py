import csv
import random

# Define the headers
headers = [
    "Timestamp", "Email Address", "Preferred Title", "Name", "Cell Phone Number",
    "School", "School Phone Number", "School Extension Number",
    "Attach 3rd Party Compliance Form", "Teacher FAQ Agreement", "Robotics/After School Interest",
    "Number of Classes", "Days", "Preferred Day"
]

# Define class-specific headers
class_headers = []

for i in range(1, 7):
    for j in range(1, i+1):
        class_headers.append(f"Grade (Class {j} of {i})")
        class_headers.append(f"Start Time (Class {j} of {i})")
        class_headers.append(f"End Time (Class {j} of {i})")
        class_headers.append(f"Days (Class {j} of {i})")
        class_headers.append(f"Number of Students (Class {j} of {i})")

# Define the days of the week
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Define the grades
grades = ["5th", "6th", "7th", "8th"]

# Define the start and end times
start_time = ["8:00:00 AM", "9:30:00 AM", "10:00:00 AM", "11:30:00 AM", "1:00:00 PM", "2:30:00 PM"]
end_time = ["9:30:00 AM", "11:00:00 AM", "11:30:00 AM", "1:00:00 PM", "2:30:00 PM", "4:00:00 PM"]

# Create a list to store the generated data
data = []

def generate_fake_data(num_teachers):

    # Generate random data for each teacher
    for teacher_id in range(1, 16):
        num_classes = random.randint(1, 6)  # Random number of classes
        days = set([random.choice(days_of_week) for _ in range(num_classes)])

        # Create a row with common information
        row = [
            "8/4/2022 10:24",
            f"teacher{teacher_id}@email.com",
            random.choice(["Mr.", "Mrs.", "Miss", "Dr.", "Ms."]),
            f"Teacher {teacher_id}",
            str(random.randint(1000000000, 9999999999)),
            f"School {teacher_id}",
            str(random.randint(1000000000, 9999999999)),
            str(random.randint(100, 999)),
            random.choice(["Yes", "No"]),
            random.choice(["Yes", "No"]),
            random.choice(["Yes", "No"]),
            num_classes,
            ", ".join(days),
            random.choice(list(days))
        ]

        i = 0
        while i < len(class_headers):
            if (f"of {num_classes}")in class_headers[i]:
                row.append(random.choice(grades))
                row.append(random.choice(start_time))
                row.append(random.choice(end_time))
                row.append(random.choice(list(days)))
                row.append(str(random.randint(15, 30)))
            else:
                row.extend([""] * 5)
            i += 5

        # Append the row to the data
        data.append(row)

    # Write the data to a CSV file
    with open("fake_classroom_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers + class_headers * 6)  # Include class headers for each class
        writer.writerows(data)

    print("CSV file generated successfully!")

generate_fake_data(15)

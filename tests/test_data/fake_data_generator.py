import csv
import random
import string
from faker import Faker

fake = Faker()

school_options = ["A & S", "Engineering", "Peabody"]
year_options = ["First-Year", "Sophomore", "Junior", "Senior", "Graduate"]

def generate_fake_data(num_students):
    data = []
    for _ in range(num_students):

        first_name = fake.first_name()
        last_name = fake.last_name()
        middle_initial = random.choice(string.ascii_lowercase)
        email = f"{first_name.lower()}.{middle_initial}.{last_name.lower()}@vanderbilt.edu"
        phone_number = f"{random.randint(100, 999):03d}-{random.randint(100, 999):03d}-{random.randint(1000, 9999):04d}"

        row = [
            fake.date_time_this_year().strftime("%m/%d/%Y %H:%M"),
            email,
            "By checking this box, I certify that I have read and understood the FAQ",
            f"{first_name} {last_name}",
            first_name,
            last_name,
            phone_number,
            email,
            random.choice(school_options),
            random.choice(year_options),
            fake.job(),
            fake.random_element(elements=("Yes", "No")),
            fake.random_element(elements=("S", "M", "L", "XL")),
            fake.random_element(elements=("Yes", "No")),
            fake.random_element(elements=("Yes", "No")),
        ]
        for _ in range(39):
            row.append(random.choice(["", "M", "T", "W", "R", "F"]))
        row.append("I am interested in this program")
        row.append(fake.random_element(elements=("Yes", "No")))
        data.append(row)
    return data

def save_to_csv(data, filename):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Timestamp", "Email Address", "FAQ", "Dress Code Acknowledgment", "First Name", "Last Name",
            "Phone Number", "Email", "School", "Year", "Major", "Special Needs Students", "T-shirt size",
            "Team Leader", "Previous Experience (team leader)", "Previous Experience (Volunteer)",
            "Commitments [7:15-7:30 am]", "Commitments [7:30-7:45 am]", "Commitments [7:45-8:00 am]",
            "Commitments [8:00-8:15 am]", "Commitments [8:15-8:30 am]", "Commitments [8:30-8:45 am]",
            "Commitments [8:45-9:00 am]", "Commitments [9:00-9:15 am]", "Commitments [9:15-9:30 am]",
            "Commitments [9:30-9:45 am]", "Commitments [9:45-10:00 am]", "Commitments [10:00-10:15 am]",
            "Commitments [10:15-10:30 am]", "Commitments [10:30-10:45 am]", "Commitments [10:45-11:00 am]",
            "Commitments [11:00-11:15 am]", "Commitments [11:15-11:30 am]", "Commitments [11:30-11:45 am]",
            "Commitments [11:45-12:00 pm]", "Commitments [12:00-12:15 pm]", "Commitments [12:15-12:30 pm]",
            "Commitments [12:30-12:45 pm]", "Commitments [12:45-1:00 pm]", "Commitments [1:00-1:15 pm]",
            "Commitments [1:15-1:30 pm]", "Commitments [1:30-1:45 pm]", "Commitments [1:45-2:00 pm]",
            "Commitments [2:00-2:15 pm]", "Commitments [2:15-2:30 pm]", "Commitments [2:30-2:45 pm]",
            "Commitments [2:45-3:00 pm]", "Commitments [3:00-3:15 pm]", "Commitments [3:15-3:30 pm]",
            "Commitments [3:30-3:45 pm]", "After School",
            "This year VSVS is excited to implement lessons at Antioch Middle School to help launch their new makerspace."
            "This will likely require more time (up to an hour longer than usual). Please indicate if you are interested below:",
            "Confirmation"
        ])
        writer.writerows(data)

fake_data = generate_fake_data(300)
save_to_csv(fake_data, "fake_student_data.csv")
print("Fake data generated and saved as 'fake_student_data.csv'.")

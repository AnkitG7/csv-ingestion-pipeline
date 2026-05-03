import csv
import random

# Sample Indian names (you can expand this list)
names = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Krishna", "Ishaan", "Shaurya",
    "Aanya", "Diya", "Saanvi", "Ananya", "Riya", "Priya", "Neha", "Kavya", "Pooja", "Sneha",
    "Rahul", "Rohit", "Amit", "Vikram", "Karan", "Deepak", "Suresh", "Mahesh", "Rakesh", "Naresh",
    "Meena", "Sunita", "Anita", "Kiran", "Lakshmi", "Geeta", "Shalini", "Nisha", "Tanvi", "Simran",
    "Manish", "Nitin", "Alok", "Harsh", "Varun", "Yash", "Ritu", "Seema", "Jyoti", "Payal"
]


def generate_email(name, index):
    return f"{name.lower()}{index}@example.com"


def generate_age():
    return random.randint(18, 60)


def create_csv(n, filename="indian_data.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "email", "age"])  # header

        for i in range(1, n + 1):
            name = random.choice(names)
            email = generate_email(name, i)
            age = generate_age()
            writer.writerow([name, email, age])


if __name__ == "__main__":
    n = int(input("Enter number of rows: "))
    create_csv(n)
    print(f"{n} rows written to indian_data.csv")

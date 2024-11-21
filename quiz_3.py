import mysql.connector
import random
import json

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",  # Change to your MySQL username
    "password": "password",  # Change to your MySQL password
    "database": "quiz_app"
}

# Initialize database connection
def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

# Insert quiz questions into the database
def insert_questions():
    quiz_questions = {
        "Operating System": [
            ("What is a process?", ["A. A program in execution", "B. An inactive program", "C. A CPU", "D. A file"], "A"),
            # Add more questions...
        ],
        # Add other subjects...
    }

    conn = connect_db()
    cursor = conn.cursor()

    for subject, questions in quiz_questions.items():
        for question, options, answer in questions:
            cursor.execute("""
                INSERT INTO questions (subject, question, options, correct_answer)
                VALUES (%s, %s, %s, %s)
            """, (subject, question, json.dumps(options), answer))

    conn.commit()
    conn.close()

# Register a student
def register_student():
    conn = connect_db()
    cursor = conn.cursor()

    print("\n--- Registration ---")
    name = input("Enter your name: ")
    reg_id = input("Create a registration ID: ")
    password = input("Create a password: ")

    cursor.execute("SELECT * FROM users WHERE reg_id = %s", (reg_id,))
    if cursor.fetchone():
        print("Registration ID already exists. Please try again.")
        conn.close()
        return register_student()

    cursor.execute("INSERT INTO users (reg_id, name, password) VALUES (%s, %s, %s)", (reg_id, name, password))
    conn.commit()
    conn.close()
    print(f"Registration successful. Your registration ID is {reg_id}.")

# Log in a student
def login_student():
    conn = connect_db()
    cursor = conn.cursor()

    print("\n--- Login ---")
    reg_id = input("Enter your registration ID: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT * FROM users WHERE reg_id = %s AND password = %s", (reg_id, password))
    if cursor.fetchone():
        conn.close()
        print(f"Login successful. Welcome!")
        return reg_id
    else:
        conn.close()
        print("Invalid registration ID or password. Please try again.")
        return login_student()

# Take a quiz
def take_quiz(subject, reg_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions WHERE subject = %s", (subject,))
    questions = cursor.fetchall()

    selected_questions = random.sample(questions, 5)
    score = 0

    print(f"\n--- {subject} Quiz ---")
    for i, (qid, _, question, options, correct_answer) in enumerate(selected_questions, 1):
        options = json.loads(options)
        print(f"Q{i}: {question}")
        for option in options:
            print(option)
        user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        if user_answer == correct_answer:
            score += 1

    cursor.execute("INSERT INTO quiz_attempts (reg_id, subject, score) VALUES (%s, %s, %s)", (reg_id, subject, score))
    conn.commit()
    conn.close()
    print(f"\nYou scored {score}/5 in the {subject} quiz.")

# Choose a subject
def choose_subject():
    print("\n--- Choose Subject ---")
    print("1. Operating System")
    print("2. Database Management System")
    print("3. Computer Network")
    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        return "Operating System"
    elif choice == "2":
        return "Database Management System"
    elif choice == "3":
        return "Computer Network"
    else:
        print("Invalid choice. Please try again.")
        return choose_subject()

# Main function
def main():
    while True:
        print("\n--- Welcome to the Quiz Application ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            register_student()
        elif choice == "2":
            reg_id = login_student()
            while True:
                subject = choose_subject()
                take_quiz(subject, reg_id)
                reattempt = input("Do you want to reattempt the quiz? (yes/no): ").strip().lower()
                if reattempt != "yes":
                    break
        elif choice == "3":
            print("Thank you for using the Quiz Application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

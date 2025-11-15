# This script is designed to manage a contact database for making calls.
# It allows users to check for address conflicts, keep track of call status, 
# and add notes for each call made.
# It uses the pandas library to handle data and datetime for timestamps.

import pandas as pd  # Importing pandas for data manipulation
from datetime import datetime  # Importing datetime for handling date and time
import os  # Importing os for path handling

# Function to load the contact database from a file
def import_database(file_path):
    df = pd.read_csv(file_path, delimiter='\t')
    df.columns = df.columns.str.strip()
    df['Username'] = df['Username'].astype(str).str.strip()
    df['PhoneNumber'] = df['PhoneNumber'].astype(str).str.strip()
    df['Address'] = df['Address'].astype(str).str.strip()
    return df

# Function to display addresses for a given username
def display_addresses(df, username):
    username = username.strip()
    user_data = df[df['Username'] == username]

    if not user_data.empty:
        phone_number = user_data['PhoneNumber'].iloc[0]
        user_address = user_data['Address'].iloc[0]
        matches = df[df['PhoneNumber'] == phone_number]
        unique_addresses = matches['Address'].dropna().unique()

        print(f"\n📞 Calling {username} at address: {user_address}")
        print(f"📱 Phone Number: {phone_number}")

        if len(unique_addresses) > 1:
            different_addresses = ' | '.join(unique_addresses)
            print(f"⚠️ Address conflict detected. Other addresses associated with this number: {different_addresses}")
        else:
            print(f"✅ No conflicting addresses found for this phone number.")
    else:
        print("❌ Username not found in database")

# Function to keep track of who has already been called
def check_call_status(username, df, called_usernames, called_phone_numbers):
    username = username.strip()
    user_data = df[df['Username'] == username]

    if user_data.empty:
        return "❌ Username not found."

    phone_number = user_data['PhoneNumber'].iloc[0]

    if username in called_usernames:
        return "⚠️ This Username has already been called"
    elif phone_number in called_phone_numbers:
        return "⚠️ This Phone Number has already been called"
    else:
        called_usernames.add(username)
        called_phone_numbers.add(phone_number)
        return "✅ You're good to call"

# Function to prompt user for call notes
def prompt_for_notes():
    notes = input("Enter notes for this call: ")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{current_time} - {notes}"

# Main function
def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'export_20250404094645 - Copy.txt')

    try:
        df = import_database(file_path)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return
    except Exception as e:
        print(f"⚠️ Error reading file: {e}")
        return

    notes = []
    called_usernames = set()
    called_phone_numbers = set()

    while True:
        username = input("\nEnter the username (or type 'exit' to quit): ").strip()
        if username.lower() == 'exit':
            break

        display_addresses(df, username)
        status = check_call_status(username, df, called_usernames, called_phone_numbers)
        print(status)

        print("\nChoose an option:")
        print("1. Add notes for current call")
        print("2. Proceed to next call")
        print("3. End the program")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            note = prompt_for_notes()
            notes.append(f"{username}: {note}")
        elif choice == '2':
            continue
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

    # Save notes with timestamp if any
    if notes:
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'call_notes_{current_time}.txt'
        with open(filename, 'w') as file:
            for note in notes:
                file.write(note + '\n')
        print(f"📝 Notes saved to {filename}")

if __name__ == "__main__":
    main()

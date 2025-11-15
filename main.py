# This script is designed to manage a contact database for making calls.
# It allows users to check for address conflicts, keep track of call status, 
# and add notes for each call made.
# It uses the pandas library to handle data and datetime for timestamps.

# Import the pandas library to help read and work with spreadsheet-style data
import pandas as pd

# Function to load the contact database from a file
def import_database(file_path):
    # Read the file as a table (tab-separated format)
    df = pd.read_csv(file_path, delimiter='\t')
   
    # Clean up the column names (remove extra spaces)
    df.columns = df.columns.str.strip()
   
    # Clean up each column by removing extra spaces from text
    df['Username'] = df['Username'].astype(str).str.strip()
    df['PhoneNumber'] = df['PhoneNumber'].astype(str).str.strip()
    df['Address'] = df['Address'].astype(str).str.strip()
   
    # Return the cleaned data
    return df

# Function to show the address and check for any address conflicts
def display_addresses(df, username):
    # Remove spaces from the username entered by the user
    username = username.strip()

    # Look for rows in the data where the username matches
    user_data = df[df['Username'] == username]

    # If we found that user in the data
    if not user_data.empty:
        # Get their phone number and address
        phone_number = user_data['PhoneNumber'].iloc[0]
        user_address = user_data['Address'].iloc[0]

        # Find all people who share this phone number
        matches = df[df['PhoneNumber'] == phone_number]

        # Get a list of all different addresses associated with this number
        unique_addresses = matches['Address'].dropna().unique()

        # Show who we're calling and where
        print(f"\n📞 Calling {username} at address: {user_address}")
        print(f"📱 Phone Number: {phone_number}")

        # If there are multiple addresses for this number, show a warning
        if len(unique_addresses) > 1:
            different_addresses = ' | '.join(unique_addresses)
            print(f"⚠️ Address conflict detected. Other addresses associated with this number: {different_addresses}")
        else:
            print(f"✅ No conflicting addresses found for this phone number.")
    else:
        # If username wasn't found, show an error
        print("❌ Username not found in database")

# Function to keep track of who has already been called
def check_call_status(username, called_usernames):
    # If this person has already been called, return a warning message
    if username in called_usernames:
        return "This Address has already been called"
    else:
        # Otherwise, mark them as called and allow the call
        called_usernames.add(username)
        return "You're good to call"

# Function to ask the user for notes about the call
def prompt_for_notes():
    # Ask the user to type in a note
    notes = input("Enter notes for this call: ")
    return notes

# Main function where the program starts
def main():
    # File name of the contact database
    file_path = 'export_20250404094645 - Copy.txt'

    # Try to load the data from the file
    try:
        df = import_database(file_path)
    except FileNotFoundError:
        # If the file isn't found, show an error and stop
        print(f"❌ File not found: {file_path}")
        return
    except Exception as e:
        # If any other error occurs while reading the file, show it
        print(f"⚠️ Error reading file: {e}")
        return

    # Create an empty list to store call notes
    notes = []

    # Create an empty set to track who has already been called
    called_usernames = set()

    # Start an endless loop to keep asking for usernames to call
    while True:
        # Ask the user to enter a username (or 'exit' to quit)
        username = input("\nEnter the username (or type 'exit' to quit): ").strip()
        if username.lower() == 'exit':
            break  # Exit the loop and end the program

        # Show the address and conflicts for the entered username
        display_addresses(df, username)

        # Check whether this user has already been called
        status = check_call_status(username, called_usernames)
        print(status)

        # Show options for what to do next
        print("\nChoose an option:")
        print("1. Add notes for current call")
        print("2. Proceed to next call")
        print("3. End the program")

        # Get the user's choice
        choice = input("Enter your choice (1/2/3): ").strip()

        # If they choose to add a note
        if choice == '1':
            note = prompt_for_notes()
            # Save the note with the username
            notes.append(f"{username}: {note}")
        elif choice == '2':
            continue  # Go back and ask for another username
        elif choice == '3':
            break  # Exit the loop and save notes
        else:
            print("Invalid choice. Please try again.")

    # After the loop, if there are any notes, save them to a file
    if notes:
        with open('call_notes.txt', 'w') as file:
            for note in notes:
                file.write(note + '\n')
        print("📝 Notes saved to call_notes.txt")

# This tells Python to run the main function when the script starts
if __name__ == "__main__":
    main()

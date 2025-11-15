# Call-manager
# Overview
This script is designed to manage a contact database for making calls. It allows users to:
- Check for address conflicts
- Keep track of call status
- Add notes for each call made
  
It uses the pandas library to handle data and datetime for timestamps.

Functions
import_database(file_path)
- Purpose: Load the contact database from a file.
- Parameters: file_path (str) - Path to the contact database file.
- Returns: DataFrame - Cleaned contact database.
  
display_addresses(df, username)
- Purpose: Display addresses for a given username and check for address conflicts.
- Parameters:
    df (DataFrame) - Contact database.
    username (str) - Username to search for.
- Behavior:
    Displays the address and phone number associated with the username.
    Checks for conflicting addresses associated with the same phone number.
  
check_call_status(username, called_usernames)
- Purpose: Keep track of who has already been called.
- Parameters:
username (str) - Username to check.
    called_usernames (set) - Set of usernames that have already been called.
    Returns: str - Status message indicating whether the user has already been called.

prompt_for_notes()
- Purpose: Prompt the user for notes about the call.
- Returns: str - Notes with a timestamp.

main()
- Purpose: Main function where the program starts.
- Behavior:
    Loads the contact database.
    Continuously prompts the user for usernames to call.
    Displays addresses and checks for conflicts.
    Tracks call status and prompts for notes.
    Saves notes to a file.

Usage
1. Load the contact database: The script attempts to load the contact database from a specified file.
2. Enter usernames: The user is prompted to enter usernames to call.
3. Display addresses: The script displays the address and phone number associated with the entered username and checks for     address conflicts.
4. Check call status: The script checks whether the user has already been called.
5. Add notes: The user can add notes for the current call.
6. Save notes: After exiting the loop, the script saves the notes to a file.

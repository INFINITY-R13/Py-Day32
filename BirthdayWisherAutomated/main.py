# ---------------------------- SETUP INSTRUCTIONS ------------------------------- #
# To run this script, you need to configure the following:
#
# 1. UPDATE YOUR CREDENTIALS:
#    - Change MY_EMAIL to your email address.
#    - IMPORTANT: For security, use an "App Password" instead of your regular email password.
#      - For Gmail: Go to your Google Account -> Security -> 2-Step Verification -> App Passwords.
#      - Generate a new App Password and use it for MY_PASSWORD.
#    - A better practice is to store these as environment variables instead of plain text.
#
# 2. CONFIGURE YOUR EMAIL PROVIDER:
#    - Update SMTP_ADDRESS to match your email provider's SMTP server address.
#      (e.g., "smtp.gmail.com" for Gmail, "smtp.mail.yahoo.com" for Yahoo).
#
# 3. PREPARE THE BIRTHDAY DATA:
#    - Ensure your 'birthdays.csv' file is in the same directory.
#    - The CSV must have columns named: name, email, year, month, day.
#    - Add a birthday for today's date to test the script successfully.

# ---------------------------- IMPORT LIBRARIES ------------------------------- #

# smtplib is Python's library for sending emails using the Simple Mail Transfer Protocol (SMTP).
import smtplib
# datetime is used to get the current date.
from datetime import datetime
# pandas is used for reading and handling data from the CSV file efficiently.
import pandas
# random is used to select a random letter template.
import random

# ---------------------------- CONFIGURATION ------------------------------- #

# Your email credentials and SMTP server address.
# WARNING: Do not hardcode your actual password. Use an App Password.
MY_EMAIL = "your_email@gmail.com"
MY_PASSWORD = "your_app_password"  # Use an App Password, not your regular password!
SMTP_ADDRESS = "smtp.gmail.com"

# ---------------------------- CORE LOGIC ------------------------------- #

# 1. Get today's month and day.
# Get the current date and time from the system.
today = datetime.now()
# Create a tuple (month, day) for today's date. This format will be used to
# check against the birthdays in our data. e.g., (10, 3) for October 3rd.
today_tuple = (today.month, today.day)

# 2. Read the birthday data from the CSV file.
# pandas.read_csv() reads the specified file into a DataFrame, a table-like data structure.
# We include error handling in case the file is not found.
try:
    data = pandas.read_csv("birthdays.csv")
except FileNotFoundError:
    print("Error: 'birthdays.csv' not found. Please make sure the file is in the correct directory.")
    # Exit the script if the data file is missing.
    exit()


# 3. Create a dictionary of birthdays for easy lookup.
# We use a dictionary comprehension to transform the DataFrame into a more useful format.
# {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}
# - data.iterrows() loops through each row of the DataFrame.
# - For each row:
#   - A tuple of (month, day) is created to be the dictionary KEY.
#   - The entire row (data_row) is stored as the dictionary VALUE.
# This allows us to look up a birthday instantly using a (month, day) tuple.
# Example entry: {(10, 3): name: infinity, email: infinity@email.com, ...}
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}

# 4. Check if today's date matches any birthday in the dictionary.
# This is a highly efficient check. We simply see if today's (month, day) tuple exists as a key.
if today_tuple in birthdays_dict:
    # If there's a match, retrieve the full data row for the person whose birthday it is.
    birthday_person = birthdays_dict[today_tuple]
    
    # 5. Select a random letter template.
    # Construct the file path for a random letter from the 'letter_templates' directory.
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
    
    # 6. Read and personalize the letter content.
    # The 'with' statement ensures the file is automatically closed after reading.
    with open(file_path) as letter_file:
        # Read the entire content of the template file into a string.
        contents = letter_file.read()
        # Replace the placeholder [NAME] with the actual name of the birthday person.
        # The .replace() method returns a new string with the replacement made.
        contents = contents.replace("[NAME]", birthday_person["name"])

    # 7. Send the birthday email.
    # Use a 'with' block to automatically manage the connection to the SMTP server.
    with smtplib.SMTP(SMTP_ADDRESS) as connection:
        # Secure the connection using Transport Layer Security (TLS).
        # This encrypts the email content, including your login credentials.
        connection.starttls()
        
        # Log in to your email account.
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        
        # Send the email.
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthday_person["email"],
            # The message must be formatted with "Subject:" followed by two newlines (\n\n).
            # This separates the subject line from the email body.
            msg=f"Subject:Happy Birthday!\n\n{contents}"
        )
    print(f"Birthday email successfully sent to {birthday_person['name']}!")
from datetime import datetime #imports the current date and time
import pandas as pd    #importing pandas to read the csv file
import smtplib #python lib to send mail via python
from email.message import EmailMessage #creates the content of mail to be sent

def send_bday_emails():
    EMAIL = "your_email@gmail.com" #USER email
    APP_PASSWORD = "your_app_password" #16 character app password

    today = datetime.now().strftime("%m-%d")
    current_year = datetime.now().strftime("%Y")

    # Read the birthday list
    birthdays = pd.read_csv("birthday.csv") #reads the csv file

    # Read log if exists
    try:
        with open("sent_log.txt", "r") as f:
            sent_log = f.read()#reads the latest mail log
    except FileNotFoundError:
        sent_log = ""#if there is no mail log

    for _, row in birthdays.iterrows():
        bday = datetime.strptime(row["birthday"], "%Y-%m-%d").strftime("%m-%d")
        recipient = row["email"]
        name = row["name"]
        log_id = f"{current_year}-{today}-{recipient}"#log id to make sure the mail is not repeated 

        if bday == today and log_id not in sent_log:#if the mail id is not in the csv file then that means the is going to be sent for the first time
            try:
                message = EmailMessage()
                message["Subject"] = "🎉 Happy Birthday!"
                message["From"] = EMAIL
                message["To"] = recipient
                message.set_content(f"Dear {name},\n\nWishing you a very Happy Birthday! 🥳\n\nBest wishes,\nYour Friend")

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(EMAIL, APP_PASSWORD)
                    smtp.send_message(message)

                # Write to log
                with open("sent_log.txt", "a") as f:
                    f.write(log_id + "\n")

            except Exception as e:
                print(f"Failed to send email to {name}: {e}")

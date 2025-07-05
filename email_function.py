from datetime import datetime
import pandas as pd
import smtplib
from email.message import EmailMessage

def send_bday_emails():
    EMAIL = "your_email@gmail.com"
    APP_PASSWORD = "your_app_password"

    today = datetime.now().strftime("%m-%d")
    current_year = datetime.now().strftime("%Y")

    # Read the birthday list
    birthdays = pd.read_csv("birthday.csv")

    # Read log if exists
    try:
        with open("sent_log.txt", "r") as f:
            sent_log = f.read()
    except FileNotFoundError:
        sent_log = ""

    for _, row in birthdays.iterrows():
        bday = datetime.strptime(row["birthday"], "%Y-%m-%d").strftime("%m-%d")
        recipient = row["email"]
        name = row["name"]
        log_id = f"{current_year}-{today}-{recipient}"

        if bday == today and log_id not in sent_log:
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

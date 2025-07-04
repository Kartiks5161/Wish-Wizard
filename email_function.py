# First You Will Need To Import THe Libraries:
import pandas #open source data analysis library
from datetime import datetime #accesses the date and time from your computer
import smtplib #simple mail transfer protocl library
from email.message import EmailMessage #email message builder allowing to create and send an email from .py file
from plyer import notification #allows .py to access of the device

def send_bday_emails():
    # Your Email And The App Password:
    EMAIL="Your_Email@gmail.com"
    APP_PASSWORD="16 character app password" #From Google 2FA

    # Now We Need To Load The Data From The Birthday File:
    the_dates=pandas.read_csv("birthday.csv") #this gets the dates and time from the birthday file 
    today=datetime.now().strftime("%m-%d") #this gets current the time and date

    # Now We Need To Check If Today's Date Matches Any Of The Dates in The .csv File
    for _, row in the_dates.iterrows():
        bday = datetime.strptime(row["birthday"], "%Y-%m-%d").strftime("%m-%d") #this takes the date time in the year month day format in the csv file to a readable month date format in datetime

        if bday==today:#incase it is someone's birthday today
            #we need to start composing an email for them
            message = EmailMessage()
            message["Subject"] = "🎉 Happy Birthday!"
            message["From"] = EMAIL
            message["To"] = row["email"]
            message.set_content(f"Dear {row['name']},\n\nWishing you a very Happy Birthday! 🥳\n\nHave a great day!\n\n— Your Dear Friend")

            # Now as The message is completed we need to send it to the person:
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(EMAIL, APP_PASSWORD)
                    smtp.send_message(message)

            #now we also need to notify ourselves that the said email was sent
                notify_msg = EmailMessage()
                notify_msg["Subject"] = f"✅ Birthday Email Sent to {row['name']}"
                notify_msg["From"] = EMAIL
                notify_msg["To"] = EMAIL  # sending to self
                notify_msg.set_content(f"🎂 Birthday email sent to {row['name']} at {row['email']} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(EMAIL, APP_PASSWORD)
                    smtp.send_message(notify_msg)

                with open("sent_log.txt", "a") as f:
                    f.write(f"{datetime.now()} - Sent birthday email to {row['name']} at {row['email']}\n")
            
            except Exception as e:
                print(f"Failed to send email to {row['name']}: {e}")

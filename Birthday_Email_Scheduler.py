import schedule
import time

from email_function import send_bday_emails

def work():
    send_bday_emails()

schedule.every().day.at("08:00").do(work)
# schedule.every(1).minutes.do(work) #if want to send test emails every 1 minute


while True:
    schedule.run_pending()
    time.sleep(60)

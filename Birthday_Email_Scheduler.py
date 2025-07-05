import schedule
import time

from email_function import send_bday_emails

# def work():
#     send_bday_emails()

schedule.every(60).minutes.do(send_bday_emails)#runs the function every 60 minutes from the computer start up
# schedule.every(1).minutes.do(work) 


while True:
    schedule.run_pending()
    time.sleep(60)
